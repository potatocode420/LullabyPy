from abc import ABC, abstractmethod

from discord import player
from customModules.embedmsg import EmbedMessage

#STRATEGY INTERFACE
class PlaylistStrategy(ABC):
    def __init__(self, playlist):
        self.playlist = playlist
    @abstractmethod
    def next_from_playlist(self, ctx):
        pass

    @abstractmethod 
    def print_playlist(self):
        pass

    @abstractmethod
    def previous_from_playlist(self, ctx):
        pass

#CONCRETE STRATEGIES
class ConcretePlaylistStrategyMoving(PlaylistStrategy):
    #next song from playlist
    def next_from_playlist(self, ctx):
        playlist = self.playlist
        if playlist.loop == "ONE":
            print("loop")
            playlist.playlist.head.data = playlist.musicsource.from_url(playlist.current.data.url)
            playlist.play_song(ctx)

        elif playlist.loop == "ALL":
            #Replaces the song because discordpy cannot play the same url twice
            #we add the a new version of the song played
            song = self.playlist.musicsource.from_url(playlist.current.data.title)
            playlist.add_to_playlist(song)
            playlist.playlist.RemoveFirst()
            #play next song
            playlist.play_song(ctx)

        elif playlist.current is not None:
            print("next song")
            playlist.playlist.RemoveFirst()
            playlist.play_song(ctx)

    #Methods for playlist utils
    def print_playlist(self):
        playlist = self.playlist
        message = EmbedMessage().print_playlist_moving(playlist.current, playlist.count_in_playlist())
        return message

    def previous_from_playlist(self, ctx):
        return

class ConcretePlaylistStrategyUnmoving(PlaylistStrategy):
    def __init__(self, playlist):
        super().__init__(playlist)
        self.index = 0
    #next song from playlist
    def next_from_playlist(self, ctx):
        playlist = self.playlist

        #Since this is a playlist, people will assume that going next at the end will lead back to the first song
        #thus, we will replace every song node data each time its been played
        playlist.current.data = playlist.musicsource.from_url(playlist.current.data.url)

        if playlist.loop == "ONE":
            print("loop")
            playlist.playlist.current.data = playlist.musicsource.from_url(playlist.current.data.url)
            playlist.play_song(ctx, self.index)

        elif playlist.loop == "ALL":
            self.index +=1
            print("loop all index: "+str(self.index))
            if (self.index >= playlist.count_in_playlist()): #reset index if reach the end
                self.index = 0
            playlist.play_song(ctx, self.index)
            print(self.index)

        elif playlist.current is not None:
            print("next song unmoving")
            self.index +=1
            if (self.index >= playlist.count_in_playlist()): #stops playing if reach the end
                return
            playlist.play_song(ctx, self.index)


    def print_playlist(self):
        playlist = self.playlist
        message = EmbedMessage().print_playlist_unmoving(playlist)
        return message

    def previous_from_playlist(self, ctx):
        #Move to previous node
        #self.play_song(ctx)
        return