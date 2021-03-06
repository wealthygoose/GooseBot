import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands, tasks
from itertools import cycle
from keepalive import keep_alive

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
status = cycle(['Quack!', 'Honk!'])

@bot.event
async def on_ready():
    change_status.start()
    print("Bot is ready and online!")

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send('Quack! ' + ', '.join(dice))

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    quotes = [
        f"Quack! Honk! {member.mention} has made it! Give them a warm, cozy hug <3 :')",
        f"QUACK! {member.mention}... I hope you brought some popcorn to share... ;)",
        f"{member.mention}! Welcome to the gang. We should hang out sometime! Honk! :)",
        f"Lookin' good {member.mention}. Lookin' good. Honk! <3",
        f"Hi, {member.mention}! When are we going to play Chivalry 2? Quack! :)",
        f"{member.mention} in da building! How's the weather lookin' like there? Honk! :D"
    ]

    response = random.choice(quotes)
    await channel.send(response)

@bot.command(name='quack')
async def quack(ctx):
    response = "Quack! Quack! :) <3"
    await ctx.send(response)

@bot.command(name='honk')
async def honk(ctx):
    response = "HOOOOOOONNNNNNNNK! >:)"
    await ctx.send(response)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    quotes = []
    if "Quack!" in message.content:
        quotes = [
            "Quackity! Quackity! Quack! Quack! <3",
            "Hehe. Quack!",
            "*Goose Bot dances*",
            "Did I hear a quack? QUACK!!!!"
        ]
    elif "Honk!" in message.content:
        quotes = [
          "Honk! Honk! HOOONNNNNNNK!!",
          "Hoonnnk! <3",
          "Honk? Honk.",
          "Honk. Honk, Honk, Honk. HONK!",
          "*Goose Bot does a headstand*",
          "*Goose Bot honks the truck*",
          "*Goose Bot winks and shakes the feathers*"
        ]

    if quotes: #checks if list is not empty
      response = random.choice(quotes)
      await message.channel.send(response)

    await bot.process_commands(message)

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

@bot.event
async def on_member_remove(member):
    await bot.channel.send("Someone has left the clan... Honk.. :'(")

@tasks.loop(seconds=10)
async def change_status():
  await bot.change_presence(activity=discord.Game(next(status)))

keep_alive() #pings server
bot.run(TOKEN)