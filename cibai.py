from customModules.linkedlist import SLinkedList, Node
import unittest

class TestLinkedList(unittest.TestCase):
    def test_add(self):
        newlist = SLinkedList()
        newlist.AddEnd("a")
        newlist.AddEnd("b")
        newlist.AddEnd("c")
        self.assertEqual(newlist.tail.data, "c")

    def test_count(self):
        newlist = SLinkedList()
        newlist.AddEnd("a")
        self.assertEqual(newlist.GetCount(), 1)
        newlist.AddEnd("b")
        newlist.AddEnd("c")
        self.assertEqual(newlist.GetCount(), 3)

    def test_insert_between(self):
        newlist = SLinkedList()
        newlist.AddEnd("a")
        newlist.AddEnd("b")
        newlist.AddEnd("c")
        newlist.InsertAtIndex(2,"d")
        #Test for new insertion value
        self.assertEqual(newlist.PrintList(),"a d b c")
        #Test for new insertion value next
        self.assertEqual(newlist.GetNode(1).next.data,"b")
        #Test for new insertion value prev
        self.assertEqual(newlist.GetNode(1).prev.data,"a")
    
    def test_insert_start(self):
        newlist = SLinkedList()
        newlist.AddEnd("a")
        newlist.AddEnd("b")
        newlist.AddEnd("c")
        newlist.InsertAtIndex(0,"d")
        #Test for new insertion value
        self.assertEqual(newlist.PrintList(),"d a b c")
        #Test for new head
        self.assertEqual(newlist.head.data,"d")
        #Test for new head next and prev
        self.assertEqual(newlist.GetNode(3).next.data,"d")
        self.assertEqual(newlist.GetNode(3).prev.data,"b")

    def test_insert_end(self):
        newlist = SLinkedList()
        newlist.AddEnd("a")
        newlist.AddEnd("b")
        newlist.AddEnd("c")
        newlist.InsertAtIndex(10,"d")
        #Test for new insertion value
        self.assertEqual(newlist.PrintList(),"a b c d")
        #Test for new insertion value next
        self.assertEqual(newlist.GetNode(3).next.data,"a")
        #Test for new insertion value prev
        self.assertEqual(newlist.GetNode(3).prev.data,"c")

    def test_next_node(self):
        newlist = SLinkedList()
        newlist.AddEnd("a")
        newlist.AddEnd("b")
        newlist.AddEnd("c")
        newlist.NextNode()
        newlist.NextNode()
        #test for current head
        self.assertEqual(newlist.head.data, "c")
        #test for next head
        self.assertEqual(newlist.head.next.data, "a")
        #test for prev
        self.assertEqual(newlist.head.prev.data, "b")

    def test_remove_node(self):
        newlist = SLinkedList()
        newlist.AddEnd("a")
        newlist.AddEnd("b")
        newlist.AddEnd("c")
        newlist.RemoveNode(2)

        #test for new node order after removal
        self.assertEqual(newlist.PrintList(),"a c")
        #test for head and tail
        self.assertEqual(newlist.head.data, "a")
        self.assertEqual(newlist.tail.data, "c")
        #test for next and prev
        self.assertEqual(newlist.GetNode(1).next.data, "a")
        self.assertEqual(newlist.GetNode(1).prev.data, "a")
        #test get single node
        newlist.RemoveNode(2)
        self.assertEqual(newlist.GetNode(10).next.data, "a")
        #test for none after removing all
        newlist.RemoveNode(1)
        self.assertEqual(newlist.head, None)

    def test_remove_first_all(self):
        newlist = SLinkedList()
        newlist.AddEnd("a")
        newlist.AddEnd("b")
        newlist.AddEnd("c")
        newlist.RemoveFirst()
        self.assertEqual(newlist.PrintList(), "b c")
        newlist.RemoveFirst()
        self.assertEqual(newlist.PrintList(), "c")
        newlist.RemoveFirst()
        self.assertEqual(newlist.PrintList(), None)

    def test_remove_last_all(self):
        newlist = SLinkedList()
        newlist.AddEnd("a")
        newlist.AddEnd("b")
        newlist.AddEnd("c")
        newlist.RemoveLast()
        self.assertEqual(newlist.PrintList(), "a b")
        newlist.RemoveLast()
        self.assertEqual(newlist.PrintList(), "a")
        newlist.RemoveLast()
        self.assertEqual(newlist.PrintList(), None)


    def test_remove_node_tail_head(self):
        newlist = SLinkedList()
        newlist.AddEnd("a")
        newlist.AddEnd("b")
        newlist.AddEnd("c")
        newlist.AddEnd("d")

        #test head  
        newlist.RemoveNode(1)
        self.assertEqual(newlist.PrintList(), "b c d")
        self.assertEqual(newlist.head.data, "b")
        #test tail
        newlist.RemoveNode(3)
        self.assertEqual(newlist.PrintList(), "b c")
        self.assertEqual(newlist.tail.data, "c")
    
    def test_add_remove_linking(self):
        newlist = SLinkedList()
        newlist.AddEnd("a")
        newlist.AddEnd("b")
        newlist.AddEnd("c")
        newlist.RemoveNode(2)
        newlist.AddEnd("d")

        #test for new node order
        self.assertEqual(newlist.PrintList(),"a c d")
        #test for next head
        self.assertEqual(newlist.GetNode(2).next.data, "a")
        #test for next prev
        self.assertEqual(newlist.GetNode(2).prev.data, "c")
        #test tail
        self.assertEqual(newlist.tail.data, "d")

    def test_jump_list(self):
        newlist = SLinkedList()
        newlist.AddEnd("a")
        newlist.AddEnd("b")
        newlist.AddEnd("c")
        newlist.AddEnd("d")
        newlist.AddEnd("e")

        newlist.JumpNode(3)
        #Test for current remaining nodes
        self.assertEqual(newlist.PrintList(),"c d e")
        #Test for new head node
        self.assertEqual(newlist.head.data,"c")
        #Test for previous and next nodes
        self.assertEqual(newlist.head.next.data,"d")
        self.assertEqual(newlist.head.prev.data,"e")
        


unittest.main()
