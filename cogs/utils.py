from sys import path
import discord
from discord.ext import commands, tasks

import os
import json

from customModules.embedmsg import EmbedMessage

class Utils(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(error)
        await ctx.send(error)
        await ctx.send("Get more information on commands using !help")

    @commands.command()
    async def help(self, ctx):
        #path_to_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets\\help.json  ')
        path_to_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets/help.json') #for heroku
        f = open(path_to_file,"r")
        jsondata = json.load(f)
        message = EmbedMessage().print_help(jsondata["help"], ctx)
        await ctx.send(embed = message)
        f.close()
        return

def setup(client):
    client.add_cog(Utils(client))
