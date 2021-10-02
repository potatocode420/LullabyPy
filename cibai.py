from customModules.linkedlist import SLinkedList, Node

newlist = SLinkedList()
newlist.AddEnd("a")
newlist.AddEnd("b")
newlist.AddEnd("c")
newlist.AddEnd("d")

newlist.InsertBefore(2,"e")


#newlist.RemoveNode("b")

#print("Tail prev:" + newlist.tail.prev.data)
print("Tail: "+newlist.tail.data)
print("Tail prev: "+newlist.tail.prev.data)

newlist.PrintList()
print(newlist.GetCount())
