#!/usr/bin/env python3

import sys
import time
from collections import defaultdict
from datetime import datetime
from operator import itemgetter

try:
    import discord
    from discord.ext.commands import Bot
    import dotenv
except:
    print(
        f"Please run `{sys.executable} pip install -r requirements.txt` to install requirements.",
        file=sys.stderr,
    )
    sys.exit(1)

dotenv_file = dotenv.find_dotenv()
config = {} if dotenv_file == "" else dotenv.dotenv_values(dotenv_file)

if "token" not in config or "prefix" not in config:
    print(f"Please run `config.py` to configure the bot.", file=sys.stderr)
    sys.exit(1)

bot = Bot(command_prefix=config["prefix"])


def get_guild_list():
    with open(".guilds", "a+"):
        pass
    with open(".guilds", "r") as f:
        return set(int(x) for x in f.readlines())


def save_guild_list(guilds):
    with open(".guilds", "w+") as f:
        for guild in guilds:
            f.write(str(guild) + "\n")


guilds = get_guild_list()
print(f"Enabled Guilds: {guilds}")


@bot.event
async def on_ready():
    print("Ready for action")


@bot.command()
async def enable(ctx):
    """
    Enable LRU on this server
    """
    if not ctx.guild:
        await ctx.reply("This command doesn't work in DMs!")
        return
    print(f"Enabling {ctx.guild.id}")
    if ctx.guild.id in guilds:
        await ctx.reply("LRU is already enabled on this server!")
    else:
        await ctx.reply("Enabling LRU for this server")
        guilds.add(ctx.guild.id)
        save_guild_list(guilds)


@bot.command()
async def disable(ctx):
    """
    Disable LRU on this server
    """
    if not ctx.guild:
        await ctx.reply("This command doesn't work in DMs!")
        return
    print(f"Disabling {ctx.guild.id}")
    if ctx.guild.id in guilds:
        await ctx.reply("Disabling LRU for this server")
        guilds.remove(ctx.guild.id)
        save_guild_list(guilds)
    else:
        await ctx.reply("LRU isn't enabled on this server!")


@bot.command()
async def sort(ctx):
    """
    Sort channels within categories and categories themselves in LRU order
    """
    if not ctx.guild:
        await ctx.reply("This command doesn't work in DMs!")
        return
    print(f"Sorting {ctx.guild.id}")
    await ctx.reply("Sorting channels...")

    categories = defaultdict(lambda: [])

    for channel in ctx.guild.text_channels:
        print(f"Adding channel: {channel}")
        last_msg = None
        if channel.last_message_id:
            try:
                last_msg = await channel.fetch_message(channel.last_message_id)
            except:
                pass

        categories[channel.category].append(
            (channel, (last_msg.created_at if last_msg else datetime.fromtimestamp(0)))
        )

    for catlist in categories.values():
        print(f"Sorting category...")
        catlist.sort(key=itemgetter(1), reverse=True)
        for i in range(len(catlist)):
            print(f"Moving {catlist[i][0]} to {i}")
            await catlist[i][0].edit(position=i)

    print(f"Sorting categories...")
    catsort = sorted(
        [cat for cat in categories if cat],
        key=lambda cat: categories[cat][0][1],
        reverse=True,
    )
    for i in range(len(catsort)):
        print(f"Moving {catsort[i]} to {i}")
        await catsort[i].edit(position=i)

    print(f"Done sorting {ctx.guild.id}")
    await ctx.reply("Done sorting!")


@bot.event
async def on_message(message):
    if message.guild.id in guilds:
        if message.channel.position != 0:
            await message.channel.edit(position=0)
        if message.channel.category and message.channel.category.position != 0:
            await message.channel.category.edit(position=0)

    await bot.process_commands(message)


bot.run(config["token"])
