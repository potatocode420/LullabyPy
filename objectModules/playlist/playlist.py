import time
from customModules.linkedlist import Node, SLinkedList
from customModules.musicsource import MusicSource
from customModules.playliststrategy import PlaylistStrategy
from objectModules.song import Song

class Playlist:
    def __init__(self, strategy:PlaylistStrategy):
        self.playlist = SLinkedList()
        self.loopsong = False
        self.current = self.playlist.head
        self.musicsource = MusicSource()
        self.type = "MOVING"
        self.strategy = strategy(self)

    #Method to control playlist behaviour
    def set_strategy(self, strategy):
        self.strategy = strategy(self)

    ###Functions to control playlist actions

    #get current song and goes to the next
    def play_song(self, ctx):
        if self.playlist.head is not None:
            try:
                self.current = self.playlist.head
                ctx.voice_client.play(self.current.data.play, after=lambda e: self.next_from_playlist(ctx))
            except Exception as e:
                print("Error in play_song: "+str(e))

        else:
            self.current = None

    def skip_song(self, ctx):
        self.loopsong = False
        ctx.voice_client.pause()
        self.next_from_playlist(ctx)

    def get_latest_song(self):
        return self.playlist.tail

    def add_to_playlist(self, song):
        if song is not None:
            self.playlist.AddEnd(song)
    
    #remove from playlist
    def remove_from_playlist(self, index):
        if (index < 1):
            raise Exception("Index must be more than 1 or more") #cannot jump to current song
        index+=1 #current song is considered part of the index, so we increment 1 to skip over it
        song = self.playlist.RemoveNode(index).data
        song = Song(song.play, song.title, song.duration, song.url)
        return song

    #next song from playlist
    def next_from_playlist(self, ctx):
        self.strategy.next_from_playlist(ctx)
        time.sleep(0.5)

    #jump songs in playlist
    def jump_from_playlist(self, ctx, index):
        if (index < 1):
            raise Exception("Index must be more than 1") #cannot jump to current song

        index+=1 #current song is considered part of the index, so we increment 1 to skip over it
        self.loopsong = False
        self.playlist.JumpNode(index)
        ctx.voice_client.pause()
        self.play_song(ctx)
    
    #insert songs in between
    def insert_between_playlist(self, index, song):
        if (index < 1):
            raise Exception("Index must be more than 1") #because list queue starts from number 1
        
        index+=1 #current song is considered part of the index, so we increment 1 to skip over it

        self.playlist.InsertAtIndex(index, song)

    #count songs in playlist
    def count_in_playlist(self):
        return self.playlist.GetCount()

    #empty the playlist
    def empty_playlist(self):
        self.playlist = SLinkedList()
        self.current = self.playlist.head

    #change playlist type
    def toggle_playlist_type(self):
        if self.type == "UNMOVING":
            self.type = "MOVING"
        else:
            self.type = "UNMOVING"
        return self.type
    