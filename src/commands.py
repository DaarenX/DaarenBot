from discord.ext import commands
import discord
import json
import math
import random
import urllib
from src.quotes import quotes
import time

client = commands.Bot(command_prefix='!', description="DaarenBottest yeehaw", owner_id=142930856565014528)


@client.event
async def on_ready():
    print("Login Successful!")
    game = discord.Game("Shaco")
    await client.change_presence(activity=game)
    client.whopper = False
    client.lazer = None


#
# Das ist kein good practice eigentlich aber kann man nix machen xd
#

@client.listen()
async def on_message(ctx):
    if ctx.content.lower() == "what is daaren doing?":
        if await playSound(ctx, "jojo"):
            await ctx.channel.send("I'm doin your mom <:dio:686982719552487433>")

    elif ctx.content == "Daaren":
        await ctx.channel.send("that's me lol")

    elif ctx.content.lower().startswith("suck my dick") and not client.whopper:
        if await playSound(ctx, "whoppertm"):
            await whoppertm(ctx)
            client.whopper = True

    elif ctx.content.lower() == "za warudo":
        await playSound(ctx, "zawarudo")
        await ctx.channel.send("BRRRRRRRRRRRRRR")

    elif ctx.content.lower() == "hey can we go on land?":
        client.lazer = ctx.author.id
        if await playSound(ctx, "no"):
            await ctx.channel.send("*no~*")

    elif ctx.content.lower() == "why?" and client.lazer == ctx.author.id:
        if await playSound(ctx, "lazer"):
            await ctx.channel.send("*the sun is a deadly lazor~*")
            client.lazer = None


# ADMIN THINGS

@client.command(hidden=True)
@commands.is_owner()
async def close(ctx):
    await ctx.channel.send(":thumbsup:")
    await client.logout()


@client.command(hidden=True)
@commands.is_owner()
async def reset(ctx):
    client.whopper = False


@client.command(hidden=True)
@commands.is_owner()
async def restart(ctx):
    await ctx.message.add_reaction('✅')
    await client.close()
    print("Logout Succesful!\n restarting...")


# FUN THINGS


@client.command()
async def cow(ctx):
    if await playSound(ctx, "cow"):
        await ctx.channel.send("https://tenor.com/view/dancing-polish-cow-at4am-gif-18638816")


@client.command(aliases=["africa", "toto_africa"])
async def toto(ctx):
    await playSound(ctx, "totoafrica")


@client.command()
async def damedane(ctx):
    await playSound(ctx, "damedane")


@client.command(cog="fun", description="Picture of a Doggo")
async def dog(ctx):
    await ctx.channel.send(json.loads(urllib.request.urlopen("https://random.dog/woof.json").read())['url'])


@client.command(description="Prints [length] amount of pie", signature="[length]")
async def pi(ctx, length: int = 1):
    for i in range(length):
        obj = json.loads(urllib.request.urlopen(
            "https://api.pi.delivery/v1/pi?start=%d&numberOfDigits=998" % ((i * 1996) + 1)).read())
        output = str(obj['content'])
        if i == 0:
            output = "3." + output
        obj = json.loads(urllib.request.urlopen(
            "https://api.pi.delivery/v1/pi?start=%d&numberOfDigits=998" % (i * 998 + 998 + 1)).read())
        output = "`" + output + str(obj['content']) + "`"
        await ctx.channel.send(output)


@client.command()
async def jigg(ctx):
    await ctx.channel.send("stawp")


# UTILITIES


@client.command()
async def help2(ctx):
    embed = discord.Embed(title="Commands :clap:", colour=discord.Colour(0xff00ff),
                          url="https://www.youtube.com/watch?v=RGVBtKtGfds",
                          description="[<:twitter:677135936269844480>](https://twitter.com/daarendotwav)  ["
                                      "<:twitch:677137740428738560>](https://www.twitch.tv/daarenx)  ["
                                      "<:youtube:677137756383608832>]("
                                      "https://www.youtube.com/user/KillxCrafter/featured)  ["
                                      "<:steam:677137700884840499>](https://steamcommunity.com/id/Daaaaren/)  ["
                                      "<:instagram:677137688645730344>](https://www.instagram.com/daaren.wav/)")

    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1150347609602764800/iXcuHXev_400x400.jpg")

    quote = random.choice(quotes)

    embed.set_footer(text="DaarenBottest | %s" % quote,
                     icon_url="https://pbs.twimg.com/profile_images/1150347609602764800/iXcuHXev_400x400.jpg")

    embed.add_field(name="!pi", value="2000 digits of pi because why not", inline=False)
    embed.add_field(name="!longpi <amount>", value="posts <amount>*2000 digits of pi (max.5 times)", inline=False)
    embed.add_field(name="!toto", value="toto africa", inline=True)
    embed.add_field(name="!jigg", value="hehe", inline=True)
    embed.add_field(name="!dog", value="picture of a dog", inline=True)
    embed.add_field(name="!cow", value="gif of a cow", inline=True)
    embed.add_field(name="!invite", value="my invite link", inline=True)
    embed.add_field(name="!help", value="this lol", inline=True)
    await ctx.channel.send(embed=embed)


@client.command()
async def invite(ctx):
    await ctx.channel.send(json.load(open("src/config.json"))['invite'])


@client.command()
async def ping(ctx):
    await ctx.send(math.floor(client.latency * 1000))


@client.command(aliases=["dc"])
async def disconnect(ctx):
    voicechannel = ctx.guild.voice_client
    if voicechannel is None:
        return
    else:
        await voicechannel.disconnect()


# HELPER COMMANDS

async def playSound(ctx, filename):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        voicechannel = ctx.guild.voice_client
        if voicechannel is None:
            voicechannel = await channel.connect()
        voicechannel.play(
            discord.FFmpegPCMAudio(executable="C:/FFmpeg/bin/ffmpeg.exe", source='src/sounds/%s.mp3' % filename))
        return True
    return False


async def whoppertm(ctx):
    startTime = time.time()
    for i in json.load(open("src/suckmydick.json")):
        nextTime = startTime + float(i["time"])
        while nextTime > time.time():
            pass
        await ctx.channel.send(i["text"])
    client.whopper = False