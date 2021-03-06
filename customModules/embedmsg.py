import discord
class EmbedMessage:
    def __init__(self):
        self.message = "Bot created for non commercial purposes."
        self.colour = 0x00ff00

    def print_empty_playlist(self):
        embedVar = discord.Embed(title="No songs available in queue", description="Add some songs using -play", color=self.colour)
        return embedVar
    
    def print_playlist_moving(self, song, count):
        index = 1
        songlist = ""

        #Section to show current
        if song is not None:
            embedVar = discord.Embed(title="Current song", description=song.data.title, color=self.colour)
        else:
            embedVar = discord.Embed(title="Current song", description="No songs playing", color=self.colour)

        #Section to show upcoming songs
        if index >= count:
            songlist = "No songs in queue"
            embedVar.add_field(name="Music Queue", value=songlist)
        else:
            while index < count:
                song = song.next
                songlist += f"{index}. {song.data.title} duration: {song.data.duration}\n"
                index +=1
            embedVar.add_field(name="Music Queue", value=songlist)
        return embedVar

    def print_playlist_unmoving(self, playlist):
        index = 1
        songlist = ""
        song = playlist.playlist.GetNode(0)

        #Section to show current
        if song is not None:
            while index <= playlist.count_in_playlist():
                #highlights the current song
                if (song == playlist.current):
                    songlist += f"```fix\n{index}. {song.data.title} duration: {song.data.duration}```\n"
                else:
                    songlist += f"{index}. {song.data.title} duration: {song.data.duration}\n"
                song = song.next
                index +=1
            embedVar = discord.Embed(title="Music Playlist", description=songlist, color=self.colour)
        else:
            embedVar = discord.Embed(title="Music playlist", description="No songs in playlist", color=self.colour)
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

    def print_playlist_type(self, type):
        embedVar = discord.Embed(title="\u200b", description=f"Current playlist type is {type}", color=self.colour)
        return embedVar

    def print_loop_type(self, type):
        embedVar = discord.Embed(title="\u200b", description=f"Current loop type is {type}", color=self.colour)
        return embedVar

    def print_lyrics(self, title, author, lyrics, thumbnail):
        print(thumbnail)
        embedVar = discord.Embed(title=title, description=lyrics, color=self.colour)
        embedVar.set_thumbnail(url=thumbnail)
        embedVar.set_author(name=author)
        return embedVar
