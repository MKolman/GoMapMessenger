import traceback
import datetime

from src.discord import Webhook

import SECRETS
from src.imager import make_image, upload_image, UploadError


def send(all_results):
    try:
        sett = SECRETS.CHAT['discord']
        for result in all_results:
            make_image(result)
            try:
                img_link = upload_image(sett['img_upload_url'])
            except UploadError as e:
                exc = traceback.format_exc()
                print(exc)
                txt = "{}: An error while uploading image:\n{}\n{}".format(
                    datetime.datetime.now().isoformat(), str(e),
                    e.extra_data.content)
                msg = Webhook(
                    sett['error_webhook'],
                    msg=txt,
                )
                msg.post()
                img_link = None and "https://i.imgur.com/ZdjcRWW.png"
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
                msg = Webhook(url, msg=result['message']+tags, image=img_link)
                msg.post()
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
