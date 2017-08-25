import json
from datetime import datetime

import requests as req

from pokemon import pokedex
import SECRETS


def filter_old_raids(raids, filename='raid_status.json'):
    """ Function that filters out all the raids that have already been sent
    :params:
        raids: all currentltly fetched raids
        filename: name of the file where previous raids are stored
    :returns:
        All the raids in `raids` not found in  `filename`. If `filename` does
        not yet exists it is created (with current raid data) and an empty array
        is returned."""
    new_raids = []
    try:
        # If the file exists load data from it
        with open(filename) as f:
            raid_data = json.load(f)
            for raid in raids:
                # Only add raids not found
                if raid["gym_id"] not in raid_data or \
                        raid["time"] != raid_data[raid["gym_id"]]:
                    new_raids.append(raid)

            # Add newly foung raids in the raid_data
            for raid in new_raids:
                raid_data[raid["gym_id"]] = raid["time"]
    except FileNotFoundError:
        print("Found no previous raid data. Creating now.")
        # If the file does not exist save the raid data
        raid_data = {raid_data[raid["gym_id"]]: raid["time"] for raid in raids}

    # Re-save the new raid_data
    with open(filename, "w") as f:
        json.dump(raid_data, f)

    return new_raids


def get_all_raids(min_lvl=5):
    resp = req.get("https://mapdata2.gomap.eu/mnew.php", params={
        "mid": "0",  # Get full scan
        "ex": "[" + (",".join(map(str, range(1, 251)))) + "]",
        "w": SECRETS.LOCATION_W,
        "e": SECRETS.LOCATION_E,
        "n": SECRETS.LOCATION_N,
        "s": SECRETS.LOCATION_S,
        "gid": "0"})
    data = resp.json()
    gyms = data["gyms"]
    result = []
    for gym in gyms:
        if "rpid" in gym and gym["lvl"] >= min_lvl:
            result.append({
                "lvl": gym["lvl"],
                "pokemon": pokedex[gym["rpid"]],
                "gym_name": gym["name"],
                "gym_id": str(gym["gym_id"]),
                "until": datetime.fromtimestamp(gym["re"]),
                "time": gym["re"],
                "team": gym["team_id"],
                "gym": gym,
                "location": "https://www.google.si/maps/place/{},{}".format(
                            gym["latitude"], gym["longitude"]),
            })
            result[-1]["message"] = make_message(result[-1])
    return filter_old_raids(result)


def make_message(raid):
    teams = {0: "None", 1: "Mystic", 2: "Valor", 3: "Instinct"}
    return f"""New lvl {raid['lvl']} raid
Raid Boss: {raid['pokemon']['name'].upper()}
Gym: {raid['gym_name']} ({teams[raid['team']]})
Until: {raid['until'].time()}
Location: {raid['location']}
👍 if you are interested"""
