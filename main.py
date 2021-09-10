from discord.ext import commands
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from asyncio import sleep
import requests
import pandas as pd

def get_passwords():
    df = pd.read_csv(r"C:\Users\emill\Desktop/secrets.csv")
    api_key = df["apikey"][0]
    token = df["token"][0]
    channel = df["channel"][0]
    return api_key,token,channel


def get_url(videoname,api_key):
    videoname.replace(' ','&')
    x=requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={videoname}&key={api_key}").json()
    print(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={videoname}&key={api_key}")
    vidid=x['items'][0]['id']['videoId']
    url='https://www.youtube.com/watch?v='+ vidid
    print(url)
    return url


def start():
    api_key,token,channel = get_passwords()
    client = commands.Bot(command_prefix='.')
    total = 0


    @client.event
    async def on_message(message):
        if "-stop" in message.content:
            print(message.content)
            for vc in client.voice_clients:
                if vc.guild == message.guild:
                    await vc.disconnect()

        if "-p" in message.content:
            print(message.content)
            vca = client.get_channel(channel)
            vc = await vca.connect()
            url = get_url(message.content.replace("-p",""),api_key)
            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                              'options': '-vn'}
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            while vc.is_playing():
                await sleep(1)

    client.run(token)

start()