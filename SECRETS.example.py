from fbchat import ThreadType
# FB credentials
USERNAME = "<FB username>"
PASSWORD = "<FB password>"

# Scanning bounding box
LOCATION_W = "14.240820017805705"   # West most longitude
LOCATION_E = "14.759138020524377"   # East most longitude
LOCATION_N = "46.22983200641623"    # North most latitude
LOCATION_S = "45.870103364048745"   # South most latitude


CHAT = {"thread_id": "<Group chat ID>", "thread_type": ThreadType.GROUP}
ADMIN = {"thread_id": "<Admin user ID>", "thread_type": ThreadType.USER}

TIMEZONE = "Europe/Ljubljana"

# All the pokemon you want to be informed about (by their pokedex number)
POKEMON = [
    147, 148, 149,  # Dratini
    246, 247, 248,  # Larvitar
    179, 180, 181,  # Mareep
    143, 242, 131,  # Snorlax, Blissey, Lapras
    113, 176, 229,  # Chansey, Togetic, Houndoom
      3,   6,   9,  # Venosaur, Blastoise, Charizard
    154, 157, 160,  # Meganium, Typhlosion, Feraligatr
     65,  68,  76,  # Alakazam, Machamp, Golem
    130, 237, 241,  # Gyarados, Hitmontop, Miltank
    201,  94,  # Unown, Gengar
    115,  83, 128,  # Kangaskhan, Farfetch'd, Tauros
    214, 222,  # Heracross Corsola
]

# Something like https://api.myjson.com/bins/2f4k
GYM_JSON = None

RAIDS = {
    "lvl": 5,  # Show all raids of lvl 5 and up
    "additional": [3, 248],  # Additionally show Venusaur and Tyranitar raids
}
