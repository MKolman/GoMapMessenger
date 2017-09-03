import SECRETS
import requests
import json


def gym_update(gyms, filename="gym_owners.json"):
    # print(gyms)
    gym_owners = dict(shame=dict())
    try:
        with open(filename, "r") as f:
            gym_owners = json.load(f)
    except FileNotFoundError as e:
        print("Creating new gym owners file")
    for gym in gyms:
        owner = {
            "time": float("inf"),
            "name": "",
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
        elif gym_owners[gym_id]["time"] != owner["time"] and owner["team"] != 0:
            prev = gym_owners[gym_id]
            print("GYMS: Owner change for {}: from {} to {}".format(
                  gym_id, prev, owner))
            if prev["team"] != owner["team"] and owner["time"] - prev["time"] < 500*60:
                print("GYMS: ", owner, "is a bad boy")
                if owner['name'] not in gym_owners['shame']:
                    gym_owners['shame'][owner["name"]] = []
                gym_owners['shame'][owner["name"]].append(prev)
            gym_owners[gym_id] = owner

    if SECRETS.GYM_JSON:
        re = requests.put(SECRETS.GYM_JSON, json=gym_owners["shame"])
        if not re.ok:
            print(re.json())
    with open(filename, "w") as f:
        json.dump(gym_owners, f)


if __name__ == "__main__":
    from tmp_data import gyms
    gym_update(gyms)
