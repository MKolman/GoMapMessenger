# GoMapMessenger
A bot that uses GoMap.eu data to send it into Facebook messenger chats.

This was only tested with linux and python3.5/python3.6.

# Installation
Clone the repository and enter the directory
`git clone https://github.com/MKolman/GoMapMessenger.git`
`cd GoMapMessenger`

Setup the virtual environment.
`virtualenv venv -p $(which python3)`
`source venv/bin/activate`
`pip install -r requirements.txt`

Setup your account
`cp SECRETS.py.example SECRETS.py`
and edit `SECRETS.py` to reflect your needs.

You can now run
`python main.py`
to fetch new data from GoMap and send it to you.

## Crontab
You can use crontab to run this script evert 5 minutes for you. First do
`crontab -e`
and add the line
`*/5 * * * * cd /path/to/GoMapMessenger/ && . venv/bin/activate && python main.py >> crontab.log 2>> crontab.err`


