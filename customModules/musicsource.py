import asyncio
import discord
import asyncio
import youtube_dl
import youtube_search
import json
from objectModules.song import Song

class MusicSource(discord.PCMVolumeTransformer):
    def __init__(self, volume=0.5):
        self.ytdl = youtube_dl.YoutubeDL({
        'format': 'bestaudio/best',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
    })

    def search(self, arg):
        yt = youtube_search.YoutubeSearch(arg, max_results=1).to_json()
        try:
            yt_id = str(json.loads(yt)['videos'][0]['id'])
            yt_url = 'https://www.youtube.com/watch?v='+yt_id
            print("Results found")
        except:
            print("No results found")
            return None
        
        return yt_url

    def from_url(self, url, stream=True, loop=False):
        data = self.ytdl.extract_info(url, download=False)
        if data:
            if 'entries' in data:
                data = data['entries'][0]
                filename = data['formats'][0]['url'] if stream else self.ytdl.prepare_filename(data)
            else:
                filename = data['url']
        else:
            print("No entries found")
            return None

        play = discord.FFmpegPCMAudio(filename, **{
            'options': "-vn",
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        })
        song = Song(play, data["title"], data["duration"], url)

        return song

