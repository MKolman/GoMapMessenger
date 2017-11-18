from fbchat import ThreadType

VERSION = "2.4"

# ============= GOMAP SETTINGS =============
# Scanning bounding box
LOCATION_W = "14.240820017805705"   # West most longitude
LOCATION_E = "14.759138020524377"   # East most longitude
LOCATION_N = "46.22983200641623"    # North most latitude
LOCATION_S = "45.870103364048745"   # South most latitude

# All the pokemon you want to be informed about (by their pokedex number)
POKEMON = [
    147, 148, 149,  # Dratini family
    246, 247, 248,  # Larvitar family
    179, 180, 181,  # Mareep family
    143, 242, 131,  # Snorlax, Blissey, Lapras
    113, 176, 229,  # Chansey, Togetic, Houndoom
      3,   6,   9,  # Venosaur, Blastoise, Charizard
    154, 157, 160,  # Meganium, Typhlosion, Feraligatr
     65,  68,  76,  # Alakazam, Machamp, Golem
    130, 237, 241,  # Gyarados, Hitmontop, Miltank
    201,  94,  # Unown, Gengar
    115,  83, 128,  # Kangaskhan, Farfetch'd, Tauros
    214, 222,  # Heracross, Corsola
]

# Which raids do you want to report
RAIDS = {
    "lvl": 5,  # Show all raids of lvl 5 and up
    "additional": [3, 248],  # Additionally show Venusaur and Tyranitar raids
}


# ============ CHAT SETTINGS ==============
# Explicit timezone so the script works on servers in UTC
TIMEZONE = "Europe/Ljubljana"


CHAT = {
    # Facebook messenger settings
    "messenger": {
        # Set this to True to enable FB messenger
        "ACTIVATE": False,
        # Enter your facebook username and password
        "username": "<FB username>",
        "password": "<FB password>",
        # The main chat (you can get the id from the URL)
        "chat": {
            "thread_id": "<Group chat ID>",
            "thread_type": ThreadType.GROUP
        },
        # You can use either another group, the same group or a user
        "admin": {
            "thread_id": "<Admin user ID>",
            "thread_type": ThreadType.USER
        },
        # You can set a browser user agent to fake the browser you are using
        # You can see your user agent here:
        # https://www.whoishostingthis.com/tools/user-agent/
        "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "\
                      "(KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
    },

    # Discord webhook
    "discord": {
        # Set this to True to enable Discord reporting
        "ACTIVATE": False,
        # Channel for pokemon sightings
        "pokemon_webhook": "<webhook url>",
        # Channel for raids
        "raid_webhook": "<webhook url>",
        # Channel for high IV pokemon
        "highiv_webhook": "<webhook url>",
        # Channel for errors
        "error_webhook": "<webhook url>",
        # Where will you serve the image to be uploaded
        "img_upload_url": "<http://your.domain.com/path/to/map.png>",

        # To which pokemon should extra tags be added?
        "special_ranks": {
            # For example add a 'starter tag'
            (3, 6, 9): {  # List your pokemon here
                "name": "Starter",  # Not used
                "role_id": "<role_id>",  # It must be a role that anyone can @mention
            },
            # Add Unown tag for unown
            (201,): {  # List your pokemon here
                "name": "Unown",
                "role_id": "<role_id>",  # Get role_id in discord with '\@role'
            }
        }
    }
}


# ============ WALL OF SHAME ================
# Something like https://api.myjson.com/bins/2f4k
GYM_JSON = None
