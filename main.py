import traceback

import os
import time

from fbchat import Client

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
    try:
        print("Logging in...")
        ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like "\
             "Gecko) Chrome/51.0.2704.106 Safari/537.36"
        client = Client(SECRETS.USERNAME, SECRETS.PASSWORD, user_agent=ua)
    except Exception as e:
        print("Could not login!")
        print(traceback.format_exc())
        return False
    try:
        for result in all_results:
            print(result["message"])
            make_image(result)
            # client.sendMessage(result["message"], **SECRETS.CHAT)
            client.sendLocalImage("./img/tmp_raid.png", result["message"], **SECRETS.CHAT)
    except Exception as e:
        exc = traceback.format_exc()
        print("GoMap Messenger failed")
        print(exc)
        client.sendMessage("GoMap Messenger sender failed. Sorry.", **SECRETS.ADMIN)
        client.sendMessage(exc, **SECRETS.ADMIN)


if __name__ == "__main__":
    os.environ['TZ'] = SECRETS.TIMEZONE
    time.tzset()
    send_all()
