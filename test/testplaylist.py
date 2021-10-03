import unittest
from objectModules.playlist.playlist import Playlist

class TestLinkedList(unittest.TestCase):
    def test_add(self):
        newlist = Playlist()
        newlist.AddEnd("a")
        newlist.AddEnd("b")
        newlist.AddEnd("c")
        self.assertEqual(newlist.tail.data, "c")

unittest.main()