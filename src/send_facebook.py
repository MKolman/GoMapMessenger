import traceback

from fbchat import Client

from src.imager import make_image
import SECRETS


def send(all_results):
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
            if result['type'] == 'spawn' and \
                    result["pokemon_id"] not in SECRETS.POKEMON and \
                    result["iv"] not in ["45"]:
                continue
            print(result["message"])
            make_image(result)
            client.sendLocalImage("./img/tmp_raid.png", result["message"], **sett['chat'])
    except Exception as e:
        exc = traceback.format_exc()
        print("GoMap Messenger failed")
        print(exc)
        client.sendMessage("GoMap Messenger sender failed. Sorry.", **sett['admin'])
        client.sendMessage(exc, **sett['admin'])
