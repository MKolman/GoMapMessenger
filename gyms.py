import json
from datetime import timedelta, date

import requests

import SECRETS


def is_purge(dt):
    """
    Check if it is the third saturday in the month.
    """
    is_saturday = dt.weekday() == 5
    is_third = (dt - timedelta(14)).month != (dt-timedelta(21)).month
    return is_saturday and is_third


def gym_update(gyms, filename="gym_owners.json"):
    # print(gyms)
    gym_owners = dict(shame=dict())
    try:
        with open(filename, "r") as f:
            gym_owners = json.load(f)
    except FileNotFoundError as e:
        print("Creating new gym owners file")

    purge = is_purge(date.today())
    for gym in gyms:
        owner = {
            "time": float("inf"),
            "name": None,
            "team": gym["team_id"],
            "gym_name": gym["name"]
        }
        gym_id = str(gym["gym_id"])
        for memb in gym["memb"]:
            if owner["time"] > memb["time_deploy"]:
                owner["time"] = memb["time_deploy"]
                owner["name"] = memb["tn"]
        if owner["time"] == float("inf"):
            owner["time"] = 0
        if gym_id not in gym_owners:
            print(owner)
            gym_owners[gym_id] = owner
        elif gym_owners[gym_id]["time"] < owner["time"] and owner["team"] != 0 \
                and owner["name"] is not None and \
                gym_owners[gym_id]["team"] != owner["team"]:
            prev = gym_owners[gym_id]
            if not purge and owner["time"] - prev["time"] < 500*60:
                print("GYMS: ", owner, "is a bad boy", prev)
                if owner['name'] not in gym_owners['shame']:
                    gym_owners['shame'][owner["name"]] = []
                gym_owners['shame'][owner["name"]].append(prev)
                gym_owners['shame'][owner["name"]][-1]["defeat_time"] = owner["time"]
                gym_owners['shame'][owner["name"]][-1]["defeat_team"] = owner["team"]
            gym_owners[gym_id] = owner

    if SECRETS.GYM_JSON:
        re = requests.put(SECRETS.GYM_JSON, json=gym_owners["shame"])
        if not re.ok:
            print(re.json())
    with open(filename, "w") as f:
        json.dump(gym_owners, f)


if __name__ == "__main__":
    # from tmp_data import gyms
    # gym_update(gyms)
    assert is_purge(date(2017, 10, 14)) is False
    assert is_purge(date(2017, 10, 20)) is False
    assert is_purge(date(2017, 10, 21)) is True
    assert is_purge(date(2017, 10, 22)) is False
    assert is_purge(date(2017, 10, 28)) is False

    assert is_purge(date(2017, 11, 11)) is False
    assert is_purge(date(2017, 11, 17)) is False
    assert is_purge(date(2017, 11, 18)) is True
    assert is_purge(date(2017, 11, 19)) is False
    assert is_purge(date(2017, 11, 25)) is False
