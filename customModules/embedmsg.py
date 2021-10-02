import discord
class EmbedMessage:
    def __init__(self):
        self.message = "Bot created for non commercial purposes."
        self.colour = 0x00ff00
    
    def print_queue(self, song):
        index = 1
        songlist = ""

        if song is not None:
            embedVar = discord.Embed(title="Current song", description=song.data.title, color=self.colour)

            song = song.next
            if song is not None:
                while song:
                    songlist += f"{index}. {song.data.title} duration: {song.data.duration}\n"
                    song = song.next
                    index +=1
            else:
                songlist = "No songs in queue"
            embedVar.add_field(name="Music Queue", value=songlist)
        else:
            embedVar = discord.Embed(title="Current song", description="No songs playing", color=self.colour)
        return embedVar

    def print_current_song(self, currentsong):
        if currentsong is not None:
            embedVar = discord.Embed(title="Now playing", description=currentsong, color=self.colour)
        else:
            embedVar = discord.Embed(title="Now playing", description="No current song", color=self.colour)
        return embedVar

    def print_add_song(self, currentsong):
        embedVar = discord.Embed(title="Added to queue", description=currentsong, color=self.colour)
        return embedVar

    def print_remove_song(self, removedsong):
        embedVar = discord.Embed(title="Removed from queue", description=removedsong, color=self.colour)
        return embedVar

    def print_help(self, helpcommands, ctx:discord.Client):
        embedVar = discord.Embed(title="Help List", description="Commands for Lullaby", color=self.colour)
        embedVar.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        index=1

        for helpcommand in helpcommands:
            embedVar.add_field(name="** **", value=f"**{helpcommand['command']}** {helpcommand['description']}", inline=False)
            index+=1
        return embedVar