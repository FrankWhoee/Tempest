![](tempest.png)
# Tempest
Discord subscription to google calendars.

## Prerequisites
* Install [python](https://wiki.python.org/moin/BeginnersGuide/Download)
* Install [pip](https://pip.pypa.io/en/stable/installation/)
* Install [virtualenv](https://pypi.org/project/virtualenv/)
* Install [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Installation

1. Clone repository: `git clone https://github.com/FrankWhoee/Tempest.git`
2. `cd Tempest`
3. Create a virtual env: `python3 -m venv venv`
4. Activate venv: `source venv/bin/activate`
5. Install packages: `pip install -r requirements.txt`
6. Create OAuth Client ID
    1. Login to [cloud.google.com](cloud.google.com)
    2. Click left menu bar
    3. APIs & Services > Credentials
    4. Click `+ CREATE CREDENTIALS`
    5. Select `OAuth client ID`
    6. Select `Desktop app` for `Application Type`
    7. Choose any name. We will use `Tempest`
    8. Click `Create`
    9. Click `DOWNLOAD JSON` from the pop up
    10. Move the downloaded JSON to the `Tempest` folder and rename it as `credentials.json`
    11. Close the pop up
    12. Click `OAuth consent screen` on the left bar
    13. Click `EDIT APP`
    14. Click `SAVE AND CONTINUE` twice
    15. Add yourself as a Test user by clicking `+ ADD USERS`
        1. Enter your gmail
    16. Click `SAVE AND CONTINUE`
7. Create a [Discord bot](https://discordpy.readthedocs.io/en/stable/discord.html)
8. `echo "DISCORD=YOURDISCORDBOTTOKEN" > .env`
9. `python3 main.py`
10. The first time that you run it, it will go to your browser to ask for permission to access your account. This will create a token.json file. If you would like to run this bot on a server with no GUI, just get the token.json file on a computer with a GUI and then move both credentials.json and token.json to the desired server.

## Usage
1. Invite the bot to a server
    1. Use this link to invite the bot. Replace YOURCLIENTID with your discord bot's client ID: `https://discord.com/api/oauth2/authorize?client_id=YOURCLIENTID&permissions=10737495040&scope=bot` 
3. Go to `Settings and Sharing` for the calendar you would like to use.
4. Scroll down to `Integrate Calendar`
5. Copy the Calendar ID
6. Send `-register CALENDARID` to the channel where you want peopel to subscribe to your calendar
7. You're done!
