# GoMapMessenger
A bot that sends pokemon raid and rare pokemon data into Facebook messenger chats.

This was only tested with linux and python3.5/python3.6.

# Linux
## Installation
Clone the repository and enter the directory

`git clone https://github.com/MKolman/GoMapMessenger.git`

`cd GoMapMessenger`

Setup the virtual environment.

`virtualenv venv -p $(which python3)`

`source venv/bin/activate`

`pip install -r requirements.txt`

Setup your account

`cp SECRETS.example.py SECRETS.py`

and edit `SECRETS.py` to reflect your needs.

You can now run

`python main.py`

to fetch new data from GoMap and send it to you.

### Crontab
You can use crontab to run this script evert 5 minutes for you. First do

`crontab -e`

and add the line

`*/5 * * * * cd /path/to/GoMapMessenger/ && . venv/bin/activate && python main.py >> crontab.log 2>> crontab.err`



# Windows

## Instalation
Download and install `python 3.6` from https://www.python.org/downloads/. Make sure to
select "Add Python3.6 to PATH".

Download this repo from https://github.com/MKolman/GoMapMessenger/archive/master.zip and unzip it.

Enter `GoMapMessenger-master` folder and run `Install.bat`.

Open `SECRETS.py` (in anything other than notepad) and edit it with your
Facebook messenger data.

You can then try running `main.py`. If successfull a `result_status.json` file
should be created on first run.

You can now call main.py any time you wish to fetch new data and send it to you.

### Schtasks
Schtasks is apparently a windows equivalent to Cron. If you figure out how to
enable it for this program please contact me.

https://technet.microsoft.com/en-us/library/cc725744.aspx


