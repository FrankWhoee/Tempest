![](tempest.png)
# Tempest
Makes discord events mentionable. Automatically creates roles when a Scheduled Event is created, and assigns people to that role when they sign up as Interested.

### TODO
1. Removing role when event expires. Needs remove_role in discord.py, which is not yet implemented.

## Prerequisites
* Install [python](https://wiki.python.org/moin/BeginnersGuide/Download)
* Install [pip](https://pip.pypa.io/en/stable/installation/)
* Install [virtualenv](https://pypi.org/project/virtualenv/)
* Install [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Installation

1. Clone repository: `git clone https://github.com/FrankWhoee/Tempest.git`
2. `cd Tempest`
3. Create a virtual env: `python3 -m venv venv`
4. `git submodule init`
4. `git submodule update`
4. Activate venv: `source venv/bin/activate`
5. Install packages: `pip install -r requirements.txt`
7. Create a [Discord bot](https://discordpy.readthedocs.io/en/stable/discord.html)
8. `echo "DISCORD=YOURDISCORDBOTTOKEN" > .env`
9. `python3 main.py`
## Usage
1. Invite the bot to a server
    1. Use this link to invite the bot. Replace YOURCLIENTID with your discord bot's client ID: `https://discord.com/api/oauth2/authorize?client_id=YOURCLIENTID&permissions=10737495040&scope=bot` 
7. You're done!
