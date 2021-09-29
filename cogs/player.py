import discord
from discord import client
from discord import player
from discord.ext import commands
from discord.ext.commands import errors
from discord.ext.commands.core import before_invoke, command
from customModules import playlist
import os

from customModules.musicsource import MusicSource
from customModules.linkedlist import Node, SLinkedList
from customModules.embedmsg import EmbedMessage
from customModules.playlist import Playlist

import asyncio

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
    def __init__(self, bot : commands.Bot, server : Server):
        self.bot = bot
        self.musicsource = MusicSource()
        self.server = server
        self.playlist = server.get_server(discord.client.Guild)

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
            song = self.musicsource.from_url(url)
        try:
            await ctx.send(embed=EmbedMessage().print_add_song(song.title))
            self.playlist[ctx.message.guild.id].add_to_playlist(song)
        except Exception as e:
            print(e)
            await ctx.send("Unable to find song")
        else:
            if not ctx.voice_client.is_playing():
                self.playlist[ctx.message.guild.id].play_song(ctx)

    @commands.command()
    async def loop(self, ctx):
        if self.playlist[ctx.message.guild.id]["current"] is not None:
            self.playlist[ctx.message.guild.id]["playlist"].loopsong = not self.playlist[ctx.message.guild.id]["playlist"].loopsong
            if self.playlist[ctx.message.guild.id]["playlist"].loopsong:
                await ctx.send(f"Loop enabled for {self.playlist[ctx.message.guild.id]['current'].data.title}")
            else: 
                await ctx.send("Loop disabled")
        else:
            await ctx.send("No current song to loop")
    
    @commands.command()
    async def skip(self, ctx):
        if self.playlist[ctx.message.guild.id]["playlist"].count_in_playlist() >= 1:    
            self.playlist[ctx.message.guild.id]["playlist"].loopsong = False
            ctx.voice_client.pause()
            await ctx.send(embed=EmbedMessage().print_current_song(self.playlist[ctx.message.guild.id]["playlist"].get_current_song().data.title))
            asyncio.run_coroutine_threadsafe(self.play_song(ctx), self.bot.loop)
            print("skip successful")
            return
        await ctx.send("No more songs in queue")

    @commands.command()
    async def stop(self, ctx):
        self.playlist[ctx.message.guild.id]["playlist"].empty_playlist()
        self.playlist[ctx.message.guild.id]["current"] = None
        await ctx.voice_client.disconnect()

    @commands.command()
    async def queue(self, ctx):
        if self.playlist[ctx.message.guild.id]["current"] is not None:
            message = EmbedMessage().print_queue(self.playlist[ctx.message.guild.id]["playlist"].get_current_song(), self.playlist[ctx.message.guild.id]["current"].data)
        else:
            message = EmbedMessage().print_queue(self.playlist[ctx.message.guild.id]["playlist"].get_current_song(), None)
        await ctx.send(embed=message)

    @commands.command()
    async def insert(self, ctx, index, *, url):
        try: 
            async with ctx.typing():
                index = int(index)
                song = await self.musicsource.from_url(url)
                self.playlist[ctx.message.guild.id]["playlist"].insert_between_playlist(index, song)
                await ctx.send(embed=EmbedMessage().print_add_song(song.title))
                return
        except Exception as e:
            print(e)
        utils = self.bot.get_cog("Utils")
        if utils is not None:
            await utils.on_command_error(ctx, "Please enter a proper index. Example: !insert <index> <url>")
        return

    @commands.command()
    async def jump(self, ctx, index):
        try:
            index = int(index)
            self.playlist[ctx.message.guild.id]["playlist"].jump_from_playlist(index)
            await ctx.send(embed=EmbedMessage().print_add_song(self.playlist[ctx.message.guild.id]["playlist"].get_current_song().data.title))
            asyncio.run_coroutine_threadsafe(self.play_song(ctx), self.bot.loop)
            return
        except Exception as e:
            print(e)
        utils = self.bot.get_cog("Utils")
        if utils is not None:
            await utils.on_command_error(ctx, "Please enter a proper index. Example: !jump <index>")
        return

    @commands.command()
    async def np(self, ctx):
        if (self.playlist[ctx.message.guild.id]["current"] is not None):
            await ctx.send(embed=EmbedMessage().print_current_song(self.playlist[ctx.message.guild.id]["current"].data.title))
        else:
            await ctx.send(embed=EmbedMessage().print_current_song(None))


    @play.before_invoke
    @pause.before_invoke
    @stop.before_invoke
    @skip.before_invoke
    @loop.before_invoke
    @insert.before_invoke
    @queue.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
                self.playlist = self.server.get_server(ctx.message.guild)
                return

            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        
        if ctx.author.voice.channel is None:
            raise commands.CommandError("Author not same channel as voice client.")
        #else:
        #    if (self.playlist[ctx.message.guild].count_in_playlist() == 0):
        #        self.playlist = self.server.get_server(ctx.message.guild)

def setup(client):
    client.add_cog(Player(client, Server()))
