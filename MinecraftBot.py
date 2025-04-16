import os
import discord
import urllib.request
import json
from discord.ext import commands
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
address = os.getenv("SERVER_IP") 
listenerToken = os.getenv("LISTENER_TOKEN") 

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)
intents.message_content = True

def server_status():
    #details of server
    print("verificando el estado del servidor")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'} 
    response = requests.get(f"https://api.mcsrvstat.us/2/{address}", headers=headers)
    data = response.json()  
    print(data)
    online = data['online']
    
    if online:
        online_players = data['players']['online']
        max_players = data['players']['max']
        version = data['version']
        motd = data['motd']['clean'][0].strip()
        
        try:
            player_names = data['players']['list']
        except:
            player_names = "No hay jugadores en el servidor 😞"

        return True, motd, online_players, max_players, version, player_names
    else:
        return False,None,None,None,None,'servidor no accesible'


@bot.event
async def on_ready():
    print(f'{bot.user} se ha conectado a discord!')

@bot.command(name='hi', description='Hola Amigo')
async def hi(ctx):
    await ctx.send(f'Hola Amigo {ctx.author.name}!')

@bot.command(name='status', description='Muestra el estado del servidor')
async def status(ctx):
    await ctx.send('verificando el estado del servidor')

    #getting info from server
    try:
        online, motd, online_players, max_players, version, player_names = server_status()
    except Exception as e:
        print("Failed to find server: {0}".format(e))
    if online:
        await ctx.send("✅ Servidor en línea")
 
        if player_names == "No hay jugadores en el servidor 😞":
            players = player_names
        else:
            players = ' '.join(str(e) for e in player_names)

        # Create the initial embed object
        embed=discord.Embed(title="La Forja De los Dioses!", description=f"Hola {ctx.author.name}, ✅ Servidor en linea!", color=0x109319)

        # Add author, thumbnail, fields, and footer to the embed
        embed.set_author(name="Minecraft Server", icon_url="https://static.wikia.nocookie.net/minecraft/images/f/fe/GrassNew.png/revision/latest/scale-to-width-down/340")

        embed.set_thumbnail(url="https://static.wikia.nocookie.net/minecraft/images/f/fe/GrassNew.png/revision/latest/scale-to-width-down/340")

        # Add the fields
        embed.add_field(name="MOTD", value=motd, inline=False)
        embed.add_field(name="Players", value=f"{online_players}/{max_players}", inline=True)
        embed.add_field(name="Online Players", value=players, inline=True)
        embed.add_field(name="Version", value=version, inline=False)

        # Get the time and add as footer
        now = datetime.now()
        current_time = now.strftime("%a %d %b %H:%M")
        embed.set_footer(text=f"{current_time}")

        # Send the embed to the discord channel
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ Servidor fuera de línea o no accesible")


@bot.command( name='start', description='Intenta prender el server de manera remota')
async def start(ctx):

    online, motd, online_players, max_players, version, player_names = server_status()
    if online:
        await ctx.send("✅ Servidor ya se encuentra prendido")
    else:
        try:
            res = requests.post(
                "http://b989-152-201-241-31.ngrok-free.app/run",
                headers={"Authorization": "listenerToken"},
            )

            if res.status_code == 200:
                await ctx.send("✅ Prendiendo Servidor!!")
            else:
                await ctx.send(f"❌ Failed. Status code: {res.status_code}")
        except Exception as e:
            await ctx.send(f"❌ Error: {e}")

bot.run(token)


