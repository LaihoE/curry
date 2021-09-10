from discord.ext import commands
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from asyncio import sleep


def download_video(videoname):
    videoname.replace(' ','&')
    apikey=''
    x=requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={videoname}&key={apikey}").json()
    print(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={videoname}&key={apikey}")
    vidid=x['items'][0]['id']['videoId']
    url='https://www.youtube.com/watch?v='+ vidid
    print(url)
    return url


def instaspeak():
    token = ''
    client = commands.Bot(command_prefix='.')
    total = 0
    @client.event
    async def on_ready():
        vca = client.get_channel()
        vc = await vca.connect()

    @client.event
    async def on_message(message):
        # CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO "HELLO".
        if message.content == "cow sleeping":
            await message.channel.send("sory slep well")
            for vc in client.voice_clients:
                if vc.guild == message.guild:
                    await vc.disconnect()

        if "-stop" in message.content:
            print(message.content)
            for vc in client.voice_clients:
                if vc.guild == message.guild:
                    await vc.disconnect()


        if "-p" in message.content:
            print(message.content)
            for vc in client.voice_clients:
                if vc.guild == message.guild:
                    await vc.disconnect()

            if total ==0:
                vca = client.get_channel()
                vc = await vca.connect()

            url = download_video(message.content.replace("-p",""))
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

instaspeak()
