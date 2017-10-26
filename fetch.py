import json
from datetime import datetime

import requests as req

from pokemon import pokedex
from gyms import gym_update
import SECRETS


def filter_old_results(results, filename=None):
    """ Function that filters out all the results that have already been sent
    :params:
        results: all currentltly fetched results
        filename: name of the file where previous results are stored
    :returns:
        All the results in `results` not found in  `filename`. If `filename` does
        not yet exists it is created (with current result data) and an empty array
        is returned."""
    if filename is None:
        filename = 'result_status.json'
    new_results = []
    try:
        # If the file exists load data from it
        with open(filename) as f:
            result_data = json.load(f)
            for result in results:
                # Only add results not found
                if result["loc_id"] not in result_data or \
                        result["time"] != result_data[result["loc_id"]]:
                    new_results.append(result)

            # Add newly found results in the result_data
            for result in new_results:
                result_data[result["loc_id"]] = result["time"]
    except FileNotFoundError:
        print("Found no previous result data. Creating now.")
        # If the file does not exist save the result data
        result_data = {result["loc_id"]: result["time"] for result in results}

    # Re-save the new result_data
    with open(filename, "w") as f:
        json.dump(result_data, f)

    return new_results


def get_all_results():
    resp = req.get("https://mapdata2.gomap.eu/mnew.php", params={
        "mid": "0",  # Get full scan
        "ex": "[" + (",".join([str(i) for i in range(1, 387) if i not in SECRETS.POKEMON])) + "]",
        "w": SECRETS.LOCATION_W,
        "e": SECRETS.LOCATION_E,
        "n": SECRETS.LOCATION_N,
        "s": SECRETS.LOCATION_S,
        "gid": "0"})
    try:
        data = resp.json()
    except Exception as e:
        print(resp.content)
        raise
    result = []
    gym_update(data["gyms"])
    for gym in data["gyms"]:
        if "rpid" in gym and (gym["lvl"] >= SECRETS.RAIDS["lvl"] or
                              gym["rpid"] in SECRETS.RAIDS["additional"]):
            result.append({
                "type": "raid",
                "lvl": gym["lvl"],
                "pokemon": pokedex[gym["rpid"]],
                "pokemon_id": gym["rpid"],
                "gym_name": gym["name"],
                "loc_id": str(gym["gym_id"]),
                "until": datetime.fromtimestamp(gym["re"]),
                "time": gym["re"],
                "team": gym["team_id"],
                "gym": gym,
                "location": "https://www.google.si/maps/place/{},{}".format(
                            gym["latitude"], gym["longitude"]),
                "lat": gym["latitude"],
                "lon": gym["longitude"],
            })
            result[-1]["message"] = make_message(result[-1])
        elif "lvl" in gym and gym["lvl"] >= SECRETS.RAIDS["lvl"]:
            result.append({
                "type": "raid",
                "lvl": gym["lvl"],
                "pokemon": {"name": "T{} egg".format(gym["lvl"])},
                "pokemon_id": "T{}".format(gym["lvl"]),
                "gym_name": gym["name"],
                "loc_id": str(gym["gym_id"]),
                "until": datetime.fromtimestamp(gym["rb"]),
                "time": gym["rb"],
                "team": gym["team_id"],
                "gym": gym,
                "location": "https://www.google.si/maps/place/{},{}".format(
                            gym["latitude"], gym["longitude"]),
                "lat": gym["latitude"],
                "lon": gym["longitude"],
            })
            result[-1]["message"] = make_message(result[-1])

    for poke in data["pokemons"]:
        print(poke)
        result.append({
            "type": "spawn",
            "name": pokedex[poke["pokemon_id"]]["name"],
            "pokemon_id": poke["pokemon_id"],
            "loc_id": "{}_{}".format(poke["latitude"], poke["longitude"]),
            "time": poke["disappear_time"],
            "until": datetime.fromtimestamp(poke["disappear_time"]),
            "location": "https://www.google.si/maps/place/{},{}".format(
                        poke["latitude"], poke["longitude"]),
            "lat": poke["latitude"],
            "lon": poke["longitude"],
            "team": 0,
        })
        result[-1]["message"] = make_message(result[-1])

    return filter_old_results(result)


def make_message(result):
    teams = {0: "None", 1: "Mystic", 2: "Valor", 3: "Instinct"}
    if result["type"] == "raid":
        return ("{pokemon_name} raid pri {gym_name} ({team_name} +2 žogi) do"
                " {clock}\nGoogle maps: {location}").format(
            pokemon_name=result['pokemon']['name'],
            clock=result['until'].time(),
            team_name=teams[result['team']],
            **result)
    elif result["type"] == "spawn":
        return "{name} v divjini do {clock}\nGoogle maps: {location}".format(
            clock=result['until'].time(),
            **result)
