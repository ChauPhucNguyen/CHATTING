import discord
import openai
import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()  
TOKEN = os.getenv('0ed35ba18d34efec232b013b80c19ff0af5da6b1e0bd8f28df296fb59dd47da5')  
GPT_KEY = os.getenv('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')  

openai.api_key = GPT_KEY  

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$chat'):
        prompt = message.content[6:].strip()  
        response = openai.Completion.create(
            engine='davinci',  
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        await message.channel.send(response.choices[0].text)
    
    if message.content.startswith('!search'):
        query = message.content[8:].strip()  
        url = f'https://www.google.com/search?q={query}&num=5'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.select('.tF2Cxc')
    if not results:
        await message.channel.send(f"Sorry, I couldn't find any results for {query}")
        return
    for result in results:
        result_text = result.select_one('.DKV0Md').text
        response = openai.Completion.create(
            engine='davinci',  
            prompt=result_text,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        await message.channel.send(f"{result_text}\n\n{response.choices[0].text}")

client.run(TOKEN)  
