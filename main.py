import traceback

import os
import time

import pyimgur
from fbchat import Client
from discord import Webhook

from fetch import get_all_results
from imager import make_image
import SECRETS


def send_all():
    """ Send all new raids from username to the designated chat in case of error
    inform the admin.
    """
    all_results = get_all_results()
    if len(all_results) == 0:
        print("No new results right now.")
        return

    if SECRETS.CHAT['messenger']['ACTIVATE']:
        sett = SECRETS.CHAT['messenger']
        try:
            print("Logging in...")
            ua = sett['user_agent']
            client = Client(sett['username'], sett['password'], user_agent=ua)
        except Exception as e:
            print("Could not login!")
            print(traceback.format_exc())
            return False
        try:
            for result in all_results:
                print(result["message"])
                make_image(result)
                client.sendLocalImage("./img/tmp_raid.png", result["message"], **sett['chat'])
        except Exception as e:
            exc = traceback.format_exc()
            print("GoMap Messenger failed")
            print(exc)
            client.sendMessage("GoMap Messenger sender failed. Sorry.", **sett['admin'])
            client.sendMessage(exc, **sett['admin'])

    elif SECRETS.CHAT['discord']['ACTIVATE']:
        sett = SECRETS.CHAT['discord']
        imgur = pyimgur.Imgur(sett['imgur_client_id'])
        for result in all_results:
            make_image(result)
            img = imgur.upload_image("./img/tmp_raid.png")
            if result['type'] == 'raid':
                msg = Webhook(sett['raid_webhook'], msg=result['message'], image=img.link)
            else:
                msg = Webhook(sett['pokemon_webhook'], msg=result['message'], image=img.link)
            msg.post()


if __name__ == "__main__":
    if not hasattr(SECRETS, "VERSION") or SECRETS.VERSION != "2.0":
        print("You have to update your SECRETS.py to match those in SECRETS.example.py")
        exit()
    os.environ['TZ'] = SECRETS.TIMEZONE
    if hasattr(time, "tzset"):
        time.tzset()
    send_all()
