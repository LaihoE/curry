import time
import os
import glob
from discord.ext import commands
from discord import FFmpegPCMAudio
import youtube_dl
from youtube_dl import YoutubeDL
from asyncio import sleep
import requests
import pandas as pd
from bass_boost import booster
import os
import nightcore


def get_passwords():
    df = pd.read_csv(r"secrets/secrets.csv")
    api_key = df["apikey"][0]
    token = df["token"][0]
    channel = df["channel"][0]
    return api_key, token, channel


def get_url(videoname,api_key):
    videoname.replace(' ','&')
    x=requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={videoname}&key={api_key}").json()
    print(x)
    print(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={videoname}&key={api_key}")
    vidid=x['items'][0]['id']['videoId']
    url='https://www.youtube.com/watch?v='+ vidid
    print(url)
    return url


def start():
    api_key,token,channel = get_passwords()
    client = commands.Bot(command_prefix='.')


    @client.event
    async def on_message(message):
        if "-stop" in message.content:
            print(message.content)
            for vc in client.voice_clients:
                if vc.guild == message.guild:
                    await vc.disconnect()

        # Normal play
        if "-p" in message.content:
            print(message.content)

            for vc in client.voice_clients:
                if vc.guild == message.guild:
                    await vc.disconnect()

            vca = client.get_channel(channel)
            vc = await vca.connect()
            url = get_url(message.content.replace("-p",""),api_key)
            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                              'options': '-vn'}
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', None)

                # Messages and deleting them
            await message.channel.send(f"Currently playing: {video_title}")
            vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            while vc.is_playing():
                await sleep(1)

        # Bass boosted
        if "-bp" in message.content:
            for vc in client.voice_clients:
                if vc.guild == message.guild:
                    await vc.disconnect()

            vca = client.get_channel(channel)
            vc = await vca.connect()
            query = message.content.replace("-bp", "")
            query = query.split("boost")[0]

            url = get_url(query, api_key)
            #url = "https://www.youtube.com/watch?v=B-RR9wsa12Q&ab_channel=ArneAlligator-AarneAlligaattori"
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'C:/Users/emill/PycharmProjects/curry/mp3/%(title)s-%(id)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            }

            # DELETES FILES IN MP3 AND BASS BOOSTED
            files = glob.glob('C:/Users/emill/PycharmProjects/curry/bass_boosted/*')
            for f in files:
                os.remove(f)
            files = glob.glob('C:/Users/emill/PycharmProjects/curry/mp3/*')
            for f in files:
                os.remove(f)

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            if "boost=" in message.content:
                db= message.content.split("=")[1]
                booster(int(db),int(db))
            files = os.listdir(r"C:\Users\emill\PycharmProjects\curry\bass_boosted")

            vc.play(FFmpegPCMAudio(f'C:/Users/emill/PycharmProjects/curry/bass_boosted/{files[0]}'))
            while vc.is_playing():
                await sleep(1)

        if "-nc" in message.content:
            for vc in client.voice_clients:
                if vc.guild == message.guild:
                    await vc.disconnect()

            vca = client.get_channel(channel)
            vc = await vca.connect()
            query = message.content.replace("-bp", "")
            query = query.split("boost")[0]

            url = get_url(query, api_key)
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'C:/Users/emill/PycharmProjects/curry/mp3nc/%(title)s-%(id)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            }

            files = glob.glob('C:/Users/emill/PycharmProjects/curry/nc/*')
            for f in files:
                os.remove(f)
            files = glob.glob('C:/Users/emill/PycharmProjects/curry/mp3nc/*')
            for f in files:
                os.remove(f)

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            files_mp3 = os.listdir(r"C:\Users\emill\PycharmProjects\curry\mp3nc")
            os.rename(f"C:/Users/emill/PycharmProjects/curry/mp3nc/{files_mp3[0]}","C:/Users/emill/PycharmProjects/curry/mp3nc/input.mp3")
            files_mp3 = os.listdir(r"C:\Users\emill\PycharmProjects\curry\mp3nc")
            os.system(f"nightcore C:/Users/emill/PycharmProjects/curry/mp3nc/{files_mp3[0]} +4 > C:/Users/emill/PycharmProjects/curry/nc/out.mp3")
            files = os.listdir(r"C:\Users\emill\PycharmProjects\curry\nc")
            vc.play(FFmpegPCMAudio(f'C:/Users/emill/PycharmProjects/curry/nc/{files[0]}'))
            while vc.is_playing():
                await sleep(1)

    client.run(token)

start()