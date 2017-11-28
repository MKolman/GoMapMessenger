import traceback
import datetime

import requests
from src.discord import Webhook

import SECRETS
from src.imager import make_image


def send(all_results):
    try:
        sett = SECRETS.CHAT['discord']
        for result in all_results:
            # Make img
            make_image(result)

            urls = [sett['raid_webhook']]
            tags = ""
            if result['type'] == 'spawn':
                urls = []
                if result["pokemon_id"] in SECRETS.POKEMON:
                    urls.append(sett['pokemon_webhook'])
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
                data = {
                    'username': result['pokemon']['name'],
                    'avatar_url': 'https://gomap.eu/static/icons/{}.png'.format(result['pokemon_id']),
                    'content': result['message'] + tags,
                }
                file = {'file': open('img/tmp_raid.png')}
                result = requests.post(url, data=data, file=file)
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
