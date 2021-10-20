from json.decoder import JSONDecodeError
import discord
from discord.ext import commands
from customModules.embedmsg import EmbedMessage
from objectModules.playlist.playlist import Playlist
from customModules.playliststrategy import ConcretePlaylistStrategyMoving, ConcretePlaylistStrategyUnmoving

import json
import os

class Server: 
    def __init__(self):
        self.playlist = {}

    def get_server(self, server : discord.client.Guild):
        if (server is None):
            return self

        if (self.playlist.get(server.id) is None):
            self.playlist[server.id] = Playlist()
        return self.playlist                                                                                                                                                                                                                                                                    
    
class Player(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.playlist = {}
        self.saved_playlist = {}
    
    @commands.command()
    async def help(self, ctx):
        #path_to_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets\\help.json  ')
        path_to_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets/help.json') #for heroku
        f = open(path_to_file,"r")
        jsondata = json.load(f)
        message = EmbedMessage().print_help(jsondata["help"], ctx)
        await ctx.send(embed = message)
        f.close()

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
        else:
            await ctx.send("Currently no audio is playing.")

    @commands.command()
    async def resume(self, ctx):
        if not ctx.voice_client.is_playing():
            ctx.voice_client.resume()
        else:
            await ctx.send("Audio is already playing.")

    @commands.command()
    async def play(self, ctx, *, url):
        async with ctx.typing():
            song = self.playlist[ctx.message.guild.id].musicsource.from_url(url)
        if song is None:
            await ctx.send("Unable to find song")
            return
        await ctx.send(embed=EmbedMessage().print_add_song(song.title))
        self.playlist[ctx.message.guild.id].add_to_playlist(song)
        print("Added song")
        #await asyncio.sleep(1)
        if not ctx.voice_client.is_playing():
            self.playlist[ctx.message.guild.id].play_song(ctx)

        #try the run in executor

    @commands.group()
    async def loop(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=EmbedMessage().print_loop_type(self.playlist[ctx.message.guild.id].loop))

    @loop.group()
    async def all(self, ctx):
        self.playlist[ctx.message.guild.id].set_loop_type("ALL")
        await ctx.send(f"Loop type is now {self.playlist[ctx.message.guild.id].loop}")

    @loop.group()
    async def one(self, ctx):
        self.playlist[ctx.message.guild.id].set_loop_type("ONE")
        await ctx.send(f"Loop type is now {self.playlist[ctx.message.guild.id].loop}")

    @loop.group()
    async def none(self, ctx):
        self.playlist[ctx.message.guild.id].set_loop_type("NONE")
        await ctx.send(f"Loop type is now {self.playlist[ctx.message.guild.id].loop}")
    
    @commands.command()
    async def skip(self, ctx):
        if self.playlist[ctx.message.guild.id].count_in_playlist() > 1:
            self.playlist[ctx.message.guild.id].skip_song(ctx)
            await ctx.send(embed=EmbedMessage().print_current_song(self.playlist[ctx.message.guild.id].current.data.title))
            print("skip successful")
            return
        await ctx.send("No more songs in queue")

    @commands.command()
    async def stop(self, ctx):
        self.playlist[ctx.message.guild.id].empty_playlist()
        await ctx.voice_client.disconnect()

    @commands.command()
    async def queue(self, ctx):
        async with ctx.typing():
            if self.playlist[ctx.message.guild.id].current is not None:
                message = self.playlist[ctx.message.guild.id].print_playlist()
            else:
                message = EmbedMessage().print_empty_playlist()
        await ctx.send(embed=message)

    @commands.command()
    async def insert(self, ctx, index, *, url):
        async with ctx.typing():
            song = self.playlist[ctx.message.guild.id].musicsource.from_url(url)
        if song is None:
            await ctx.send("Unable to find song")
            return
        index = int(index)
        self.playlist[ctx.message.guild.id].insert_between_playlist(index, song)
        await ctx.send(embed=EmbedMessage().print_add_song(song.title))
    
    @commands.command()
    async def remove(self, ctx, index):
        index = int(index)
        song = self.playlist[ctx.message.guild.id].remove_from_playlist(index)
        await ctx.send(embed=EmbedMessage().print_remove_song(song.title))

    @commands.command()
    async def jump(self, ctx, index):
        index = int(index)
        try:
            self.playlist[ctx.message.guild.id].jump_from_playlist(ctx, index)
        except Exception as e:
            await self.on_command_error(ctx, e)
        await ctx.send(embed=EmbedMessage().print_current_song(self.playlist[ctx.message.guild.id].current.data.title))

    @commands.command()
    async def np(self, ctx):
        if (self.playlist[ctx.message.guild.id].current is not None):
            await ctx.send(embed=EmbedMessage().print_current_song(self.playlist[ctx.message.guild.id].current.data.title))
        else:
            await ctx.send(embed=EmbedMessage().print_current_song(None))
    
    @commands.group()
    async def playlist(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=EmbedMessage().print_playlist_type(self.playlist[ctx.message.guild.id].type))

    @playlist.group()
    async def moving(self, ctx):
        type = self.playlist[ctx.message.guild.id].type
        if type == "UNMOVING":
            type = self.playlist[ctx.message.guild.id].toggle_playlist_type()
            self.playlist[ctx.message.guild.id].set_strategy(ConcretePlaylistStrategyMoving)
            self.playlist[ctx.message.guild.id].set_loop_type() #Reset the loop type
            await ctx.send(embed=EmbedMessage().print_playlist_type(self.playlist[ctx.message.guild.id].type))
        else:
            await ctx.send(f"Playlist type is already {type}")
    
    @playlist.group()
    async def unmoving(self, ctx):
        type = self.playlist[ctx.message.guild.id].type
        if type == "MOVING":
            type = self.playlist[ctx.message.guild.id].toggle_playlist_type()
            self.playlist[ctx.message.guild.id].set_strategy(ConcretePlaylistStrategyUnmoving)
            self.playlist[ctx.message.guild.id].set_loop_type() #Reset the loop type
            await ctx.send(embed=EmbedMessage().print_playlist_type(self.playlist[ctx.message.guild.id].type))
        else:
            await ctx.send(f"Playlist type is already {type}")

    #for this command, we only need to save playlist type and songs.
    @commands.command()
    async def save(self, ctx):
        self.saved_playlist[ctx.message.guild.id] = {}
        self.saved_playlist[ctx.message.guild.id]["playlist"] = []
        for song in self.playlist[ctx.message.guild.id].playlist:
            print(song.data.title)
            self.saved_playlist[ctx.message.guild.id]["playlist"].append(song.data.title)
            self.saved_playlist[ctx.message.guild.id]["type"] = self.playlist[ctx.message.guild.id].type #type of playlist
        await ctx.send("Current playlist saved!")

    @commands.command()
    async def loadsaved(self, ctx):
        if self.saved_playlist.get(ctx.message.guild.id) is not None:
            async with ctx.typing():
                await ctx.send("Loading playlist...")
                #load playlist here
                for song in self.saved_playlist[ctx.message.guild.id]["playlist"]:
                    song = self.playlist[ctx.message.guild.id].musicsource.from_url(song)
                    self.playlist[ctx.message.guild.id].add_to_playlist(song)
                if self.saved_playlist[ctx.message.guild.id]["type"] == "MOVING":
                    self.playlist[ctx.message.guild.id].set_strategy(ConcretePlaylistStrategyMoving) 
                else:
                     self.playlist[ctx.message.guild.id].set_strategy(ConcretePlaylistStrategyUnmoving)
                await ctx.send("Loaded")
            ctx.voice_client.pause()
            self.playlist[ctx.message.guild.id].play_song(ctx)
            await self.queue(ctx)
        else:
            await ctx.send("No saved playlist")

    @play.before_invoke
    @pause.before_invoke
    @stop.before_invoke
    @skip.before_invoke
    @loop.before_invoke
    @insert.before_invoke
    @queue.before_invoke
    @playlist.before_invoke
    @loop.before_invoke
    @loadsaved.before_invoke
    async def ensure_voice(self, ctx):
        if self.playlist.get(ctx.message.guild.id) is None:
            self.playlist[ctx.message.guild.id] = Playlist(ConcretePlaylistStrategyMoving)

        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
                return
            else:
                await ctx.send("You are not connected to a voice channel")
                raise commands.CommandError("Author not connected to a voice channel.")
        
        if ctx.author.voice.channel is None:
            await ctx.send("Author not same channel as voice client.")
            raise commands.CommandError("Author not same channel as voice client.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("No permissions to do that")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("No command found")
            await ctx.send("Get more information on commands using !help")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Invalid arguments for command.")
            await ctx.send("Get more information on commands using !help")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("Invalid arguments for command.")
            await ctx.send("Get more information on commands using !help")
        else:
            await ctx.send("Failed to run command")
            await ctx.send("Get more information on commands using !help")
        print(str(type(error))+" "+str(error))

def setup(client):
    client.add_cog(Player(client))
