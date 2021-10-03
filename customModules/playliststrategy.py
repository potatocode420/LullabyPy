import time
from abc import ABC, abstractmethod

#STRATEGY INTERFACE
class Strategy(ABC):
    def __init__(self, playlist):
        self.playlist = playlist
    @abstractmethod
    def next_from_playlist(self, ctx):
        pass

    @abstractmethod
    def previous_from_playlist(self, ctx):
        pass

#CONCRETE STRATEGIES
class ConcretePlaylistStrategyMoving(Strategy):
    #next song from playlist
    def next_from_playlist(self, ctx):
        playlist = self.playlist
        if playlist.loopsong:
            print("loop")
            playlist.playlist.head.data = playlist.musicsource.from_url(playlist.current.data.url)
            time.sleep(0.5)
            playlist.play_song(ctx)
            return

        if (playlist.current is not None):
            print("next song")
            playlist.playlist.NextNode() #goes to next node, deleting the current
            playlist.play_song(ctx)

    def previous_from_playlist(self, ctx):
        return

class ConcretePlaylistStrategyUnmoving(Strategy):
    #next song from playlist
    def next_from_playlist(self, ctx, loop):
        playlist = self.playlist
        if playlist.loopsong:
            print("loop")
            playlist.playlist.head.data = playlist.musicsource.from_url(playlist.current.data.url)
            time.sleep(0.5)
            playlist.play_song(ctx)
            return

        if (playlist.current is not None):
            print("next song")
            playlist.playlist.MoveNextNode() #goes to next node, deleting the current
            playlist.play_song(ctx)

    def previous_from_playlist(self, ctx):
        #Move to previous node
        #self.play_song(ctx)
        return