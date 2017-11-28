import os
import time

from src import send_facebook
from src import send_discord
from src.fetch import get_all_results
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
        send_facebook.send(all_results)
    if SECRETS.CHAT['discord']['ACTIVATE']:
        send_discord.send(all_results)


if __name__ == "__main__":
    if not hasattr(SECRETS, "VERSION") or SECRETS.VERSION != "2.5":
        print("You have to update your SECRETS.py to match ")
        print("to match the structure of SECRETS.example.py")
        exit()
    os.environ['TZ'] = SECRETS.TIMEZONE
    if hasattr(time, "tzset"):
        time.tzset()
    send_all()
