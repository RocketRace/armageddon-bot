
<p align=center>
  <img src="https://i.imgur.com/lnZjE7y.png"></img>
</p>

*Have you ever wanted to delete a server, but felt like it was too boring to simply delete it?* **Well, look no further!**

Armageddon-bot allows you to follow through with all your chaotic needs, with *four* different options for inciting cataclysm and utter chaos on your server! 

This project was designed and built as part of [Discord Community Hack Week 2019](https://blog.discordapp.com/discord-community-hack-week-build-and-create-alongside-us-6b2a7b7bba33?gi=acd20353d3).

# DISCLAIMER

# This bot will have permanent effects on your server. Use at your own discretion.

**All commands are only accessible by users with the Administrator permission. All commands will ask you for confirmation before making any permanent changes.**

# Setup

1. Python 3.6+ is required. The `discord.py[voice]` module v1.2 is required (get it [here](https://discordpy.readthedocs.io/en/latest/intro.html#installing)).

2. Place a `config.json` file into the main folder. A template is shown in `example-config.json`.

3. Run `bot.py` to launch your bot.

4. Enjoy yourself, you sadist.

# Commands, i.e., Glorious Armageddon

Armageddon-bot is designed to cause cataclysm, catastrophe, carnage - on any server it is used in. Armageddon-bot comes built-in with four different flavors of apocalypse, with varying degrees of destruction:

| Command | Armageddon-meter | Description |
| ------- | ---------------- | ----------- |
| `the` | **LOW** | Perhaps the strangest armageddon of them all. Turns absolutely everything and everyone in the server into "the". Channels, roles, nicknames, emoji. Even changes the guild icon! |
| `zombie` | **MEDIUM** | A zombie apocalypse: The icon of all apocalypses! Raises masses of zombies from the ground, which will flood text channels. Infects users, crippling their ability to perform any actions. |
| `snap` | **HIGH** | "Perfectly balanced, as all things should be." Deletes half the whole server in the snap of a finger. Half of all channels, users, roles, everything. *It's only right.* |
| `nuclear` | **VERY HIGH** | Calls down swarms of nuclear missiles to bombard the server. This will destroy every channel and every member caught in the blasts. The following nuclear fallout will purge the weakest members, and slowly everything else will decay away. In the end, nothing remains. Nothing but the bitter dust of your choices. |

# What if I don't want my server to be ruined, and only enjoy the *beautiful* cinematics associated with each command?

In that case, you're in the wrong bot repo! However, it is possible to minimize the damage. To do so, take some of the following steps:

* **Take backups of your server.** (Yes, this is real!) There are a surprising amount of public or self-hostable bots out there with the sole purpose of creating and restoring snapshots of your guild at certain points in time. There are some limitations as to what can be backed up (e.g. message history and users are hard to restore), but generally speaking these bots will do wonders.

* **Place the bot role lower.** The bot can't interact with members or roles if their position is above or equal to its own. *This will not, however, prevent it from interacting with channels, emoji, or server settings.*

* **Don't use the bot in a server you don't want to be busted!** This one should be common sense!

--------

*Thanks to the Discord team for hosting this event; it's been a blast!*

Zombie clipart retrieved from http://www.clipartsuggest.com/clip-art-zombies-apocalypse-cliparts/.
