from discord.ext import commands
import discord
import json
import math
import random
from urllib.request import urlopen
from src.quotes import quotes
import time
from gtts import gTTS

with open("src/config.json") as configfile:
    config = json.load(configfile)


client = commands.Bot(command_prefix='!', description="DaarenBot", owner_id=config['owner_id'])


@client.event
async def on_ready():
    print("Login Successful!")
    game = discord.Game("Shaco")
    await client.change_presence(activity=game)
    client.isPlayingSubtitles = False
    client.lastLazerUser = None


@client.listen()
async def on_message(ctx):
    if ctx.content.lower() == "what is daaren doing?":
        if await playSound(ctx, "jojo"):
            await ctx.channel.send("I'm doin your mom <:dio:686982719552487433>")

    elif ctx.content == "Daaren":
        await ctx.channel.send("that's me lol")

    elif ctx.content.lower().startswith("suck my dick") and not client.isPlayingSubtitles:
        if await playSound(ctx, "whoppertm"):
            await subtitles(ctx)
            client.isPlayingSubtitles = True

    elif ctx.content.lower() == "za warudo":
        await playSound(ctx, "zawarudo")
        await ctx.channel.send("BRRRRRRRRRRRRRR")

    elif ctx.content.lower() == "hey can we go on land?":
        client.lastLazerUser = ctx.author.id
        if await playSound(ctx, "no"):
            await ctx.channel.send("*no~*")

    elif ctx.content.lower() == "why?" and client.lastLazerUser == ctx.author.id:
        if await playSound(ctx, "lazer"):
            await ctx.channel.send("*the sun is a deadly lazor~*")
            client.lastLazerUser = None


# ADMIN THINGS

@client.command(hidden=True)
@commands.is_owner()
async def close(ctx):  # This is currently the same as restart because why not
    await ctx.message.add_reaction('✅')
    await client.logout()
    print("Logout Successful")


@client.command(hidden=True)
@commands.is_owner()
async def reset():
    client.isPlayingSubtitles = False


@client.command(hidden=True)
@commands.is_owner()
async def restart(ctx):
    await ctx.message.add_reaction('✅')
    await client.close()
    print("Logout Successful!\n restarting...")


# FUN THINGS


@client.command()
async def cow(ctx):
    if await playSound(ctx, "cow"):
        await ctx.message.add_reaction('🐮')
        await ctx.channel.send("https://tenor.com/view/dancing-polish-cow-at4am-gif-18638816")


@client.command(aliases=["africa", "toto_africa"])
async def toto(ctx):
    await playSound(ctx, "totoafrica")


@client.command()
async def damedane(ctx):
    await playSound(ctx, "damedane")


@client.command(cog="fun", description="Picture of a Doggo")
async def dog(ctx):
    await ctx.message.add_reaction('🐶')
    await ctx.channel.send(json.loads(urlopen("https://random.dog/woof.json").read())['url'])


@client.command(description="Prints [length] amount of pie")
async def pi(ctx, length: int = 1):
    for i in range(length):
        obj = json.loads(urlopen(f"https://api.pi.delivery/v1/pi?start={(i * 1996) + 1}&numberOfDigits=998").read())
        output = str(obj['content'])
        if i == 0:
            output = "3." + output
        obj = json.loads(urlopen(f"https://api.pi.delivery/v1/pi?start={i * 998 + 998 + 1}&numberOfDigits=998").read())
        output = "`" + output + str(obj['content']) + "`"
        await ctx.channel.send(output)


@client.command()
async def jigg(ctx):
    await ctx.channel.send("stawp")


@client.command()
async def tts(ctx, message, language='de'):
    teats = gTTS(text=message, lang=language)
    teats.save('src/sounds/tts.mp3')
    await playSound(ctx, "tts")


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

    embed.set_footer(text=f"DaarenBot | {quote}",
                     icon_url="https://pbs.twimg.com/profile_images/1150347609602764800/iXcuHXev_400x400.jpg")

    embed.add_field(name="!pi", value="<amount>*2000 digits of pi because why not", inline=False)
    embed.add_field(name="!toto", value="toto africa", inline=True)
    embed.add_field(name="!jigg", value="hehe", inline=True)
    embed.add_field(name="!dog", value="picture of a dog", inline=True)
    embed.add_field(name="!cow", value="gif of a cow", inline=True)
    embed.add_field(name="!invite", value="my invite link", inline=True)
    embed.add_field(name="!help", value="this lol", inline=True)
    await ctx.channel.send(embed=embed)


@client.command()
async def invite(ctx):
    await ctx.channel.send(config['invite'])


@client.command()
async def ping(ctx):
    await ctx.send(math.floor(client.latency * 1000))


@client.command(aliases=["dc"])
async def disconnect(ctx):
    voicechannel = ctx.guild.voice_client
    if voicechannel is None:
        return
    else:
        await ctx.message.add_reaction('✅')
        await voicechannel.disconnect()


# HELPER COMMANDS

async def playSound(ctx, filename):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        voicechannel = ctx.guild.voice_client
        if voicechannel is None:
            voicechannel = await channel.connect()
        voicechannel.play(discord.FFmpegPCMAudio(executable=config['ffmpeg'], source=f'src/sounds/{filename}.mp3'))
        return True
    return False


async def subtitles(ctx):
    startTime = time.time()
    for i in json.load(open("src/subtitles.json")):
        nextTime = startTime + float(i["time"])
        while nextTime > time.time():
            pass
        await ctx.channel.send(i["text"])
    client.isPlayingSubtitles = False
