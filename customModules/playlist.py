from customModules.linkedlist import Node, SLinkedList
from customModules.song import Song
class Playlist:
    def __init__(self):
        self.playlist = SLinkedList()
        self.loopsong = False
    
    def get_current_song(self):
        return self.playlist.head

    def get_latest_song(self):
        return self.playlist.tail

    def add_to_playlist(self, song):
        self.playlist.AddEnd(song)
    
    #remove from playlist
    def remove_from_playlist(self, song):
        self.playlist.RemoveNode(song)

    #next song from playlist
    def next_from_playlist(self):
        if (self.playlist.NextNode() is not None):
            self.playlist.NextNode()

    def fetch_next_song(self):
        return self.playlist.head.next

    #jump songs in playlist
    def jump_from_playlist(self, index):
        if (index < 1):
            raise Exception("Index must be more than 1") #because list queue starts from number 1

        index -= 1 #because index starts from 0
        self.playlist.JumpNode(index)
    
    #insert songs in between
    def insert_between_playlist(self, index, song):
        if (index < 1):
            raise Exception("Index must be more than 1") #because list queue starts from number 1
        
        index-=1
        self.playlist.Inbetween(index, song)

    #loop current song
    def loop_in_playlist(self, song):
        self.playlist.AddStart(song)

    #count songs in playlist
    def count_in_playlist(self):
        return self.playlist.GetCount()

    #empty the playlist
    def empty_playlist(self):
        self.playlist = SLinkedList()

    #save the playlist

    