from urlextract import URLExtract
from dotenv import load_dotenv
import discord
from discord.ext import commands
import requests
import json
import os

extractor = URLExtract()


def url_finder(msg):
    ext = extractor.find_urls(msg)
    if ext != []:
        return ext[0]
    return 0

def check_phishing(link):
    url = "https://phishing-url-risk-api.p.rapidapi.com/url/"

    querystring = {"url":link}

    headers = {
        "x-rapidapi-key": "e561b7f4e8msh53615b41e10226ap1951e5jsn0e544755e251",
        "x-rapidapi-host": "phishing-url-risk-api.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())
    
    api_response = json.loads(response.text)[0]
    if api_response.get('Ai_model_phishing_risk_class') == "Risky Url":
        return 'The link is a phishing link'
    return 'The link is probably safe'

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_message(message):
    user = message.author
    if message.content == "!hey":
        await message.channel.send(f"Hey {user.mention}!")
    try:
        if url_finder(message.content) != 0:
            print(message.content)
            await message.channel.send(check_phishing(url_finder(message.content)), reference = message)
    except:
        print('Error')

bot.run(TOKEN)