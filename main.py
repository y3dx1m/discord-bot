import discord
import os
from groq import Groq
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home():
    return "봇이 살아있어요!"
def run():
    app.run(host='0.0.0.0', port=8080)
Thread(target=run).start()

groq_client = Groq(api_key=os.environ['GROQ_API_KEY'])
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} 로그인 완료!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if client.user in message.mentions:
        question = message.content.replace(f'<@{client.user.id}>', '').strip()
        try:
            response = groq_client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "user", "content": question}]
            )
            await message.reply(response.choices[0].message.content)
        except Exception as e:
            print(f"에러 발생: {e}")
            await message.reply("죄송해요, 응답 생성 중 오류가 발생했어요 😢")

client.run(os.environ['DISCORD_TOKEN'])
