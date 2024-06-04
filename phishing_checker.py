from urlextract import URLExtract
from dotenv import load_dotenv
import discord
from discord.ext import commands
import requests
import os
import xmltodict

extractor = URLExtract()

def url_finder(msg):
    ext = extractor.find_urls(msg)
    if ext:
        return ext[0]
    return None

async def check_phishing(link):
    url = f"http://checkurl.phishtank.com/checkurl/index.php?url={link}"
    headers = {
        "User-Agent": "phishtank/phumpus"
    }
    response = requests.post(url, headers=headers)
    parsed_response = xmltodict.parse(response.content)

    print(parsed_response['response']['results'])

    try:
        if parsed_response['response']['results']['url0']['verified'] == "false":
            return "The link is in the Phishtank database but not verified yet. Please be cautious!"
        elif parsed_response['response']['results']['url0']['valid'] == "true":
            return "The link is phishing"
        elif parsed_response['response']['results']['url0']['valid'] == "false":
            return "The link is safe!"
    except:
        return "The link is safe! (or at least not in the Phishtank database)"

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
    
    link = url_finder(message.content)
    if link:
        try:
            response = await check_phishing(link)  # Ensure to await the async function
            await message.channel.send(response, reference=message)
        except Exception as e:
            print(f"Error: {e}")

bot.run(TOKEN)
