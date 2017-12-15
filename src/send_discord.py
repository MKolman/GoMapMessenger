import traceback
import datetime
import json

import requests
from src.discord import Webhook

import SECRETS
from src.imager import make_image


def send(all_results):
    try:
        pokemon_links = json.load(open("data/images.json"))
        sett = SECRETS.CHAT['discord']
        for result in all_results:
            # Make img
            make_image(result)

            urls = [sett['raid_webhook']]
            tags = ""
            if result['type'] == 'spawn':
                urls = []
                for key, pokemon in SECRETS.POKEMON.items():
                    if result["pokemon_id"] in pokemon:
                        urls.append(sett['pokemon_webhook'][key])
                if result["iv"].isdigit() and int(result["iv"]) >= 43:
                    urls.append(sett['highiv_webhook'])

                for pkm, val in sett["special_ranks"].items():
                    if result["pokemon_id"] in pkm:
                        tags += " <@&{}>".format(val["role_id"])

            for name, role_id in result['districts']:
                tags += " <@&{}>".format(role_id)
            if tags:
                tags = "\n" + tags
            for url in urls:
                avatar = pokemon_links.get(str(result['pokemon_id']), "")
                data = {
                    'username': result['pokemon']['name'],
                    'avatar_url': avatar,
                    'content': result['message'] + tags,
                }
                file = {'file': open('img/tmp_raid.png', 'rb')}
                res = requests.post(url, data=data, files=file)
    except Exception as e:
        exc = traceback.format_exc()
        print(exc)
        txt = "{}: An error while sending results:\n{}".format(
            datetime.datetime.now().isoformat(), exc)
        msg = Webhook(
            sett['error_webhook'],
            msg=txt,
        )
        msg.post()
