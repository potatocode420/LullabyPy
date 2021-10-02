#in hindsight, I probably could just turned playlist.py into a linkedlist without making this structure. But it was good revision =)
class Node:
   def __init__(self, data=None):
      self.data = data
      self.next = None
      self.prev = None

class SLinkedList:
    def __init__(self):
      self.head = None
      self.tail = None

    #Go to next node, destroys current one
    def NextNode(self):
        if(self.head is not None):
            #delete remaining node
            #this prevents playlist-wide looping
            if self.head == self.head.next:
                self.head = self.tail = None
                return
            self.head = self.tail.next = self.head.next
            self.head.prev = self.tail
            return
        #Set head and tail to none
        self.tail = self.head = None
    
    #Goes to next node without destroying the current one
    def MoveNextNode(self):
        if(self.head is not None):
            self.head = self.head.next
            return
        #Set head and tail to none
        self.tail = self.head = None

    #Go to next node, does not destroy current one
    #not sure about this, for my unmoving playlist, I might use the original next, but add a backup node before it gets destroyed since 
    #I can't reuse the same nodes anyway (the play will not work, fuck)

    #Add nodes at the start
    def AddStart(self, newdata):
        NewNode = Node(newdata)
        if self.head is None:
            NewNode.next = NewNode.prev = NewNode
            self.head = self.tail = NewNode
            return

        NewNode.next = self.head
        NewNode.prev = self.tail
        self.tail.next = self.head.prev = NewNode
        self.head = self.head.prev

    #Add nodes at the end
    def AddEnd(self, newdata):
        NewNode = Node(newdata)
        if self.head is None:
            NewNode.next = NewNode.prev = NewNode
            self.head = self.tail = NewNode
            return

        #Head will be the next node
        NewNode.next = self.head
        #Current tail will be previous node
        NewNode.prev = self.tail
        #Previous of head and next of tail will be the new node
        self.head.prev = self.tail.next = NewNode
        #Set new current tail
        self.tail = self.tail.next

    #Add nodes at selected index
    #This is trippy but it works such that it finds the node that is 2 nodes before the target node, then adds a node after it
    #This function assumes anything less than index 1 is index 1
    def InsertAtIndex(self, index, new_node):  
        temp = self.head

        NewNode = Node(new_node)

        #because we want to insert at its exact position, count starts with 1
        count = 1

        if self.head is None:
            self.head = self.tail = NewNode
            return
        
        if index == 0:
            self.AddStart(NewNode.data)
            return
        
        #Add to end if index not found
        if index > self.GetCount():
            self.AddEnd(NewNode.data)
            return

        #Loop temp to the current node
        #-1 to the index because we want to get the node before it
        while count < index-1:
            temp = temp.next
            count+=1

        #Next node of new node is next of current node
        NewNode.next = temp.next
        #Previous node of new node is previous of current node
        NewNode.prev = temp
        #Next node of current node is the new node
        temp.next = NewNode
        return  
    
    def RemoveFirst(self):
        temp = self.head
        prev = self.head.prev
        if self.head is None:
            raise Exception("List is empty")
        
        if temp.next == temp:
            self.head = self.tail = None
            return
        
        prev.next = temp.next
        self.head = prev.next

    def RemoveLast(self):
        temp = self.tail
        prev = self.tail.prev
        if self.head is None:
            raise Exception("List is empty")
        
        if temp.next == temp:
            self.head = self.tail = None
            return
        
        prev.next = temp.next
        self.tail = prev
        self.head = prev.next
    
    def RemoveNode(self, index):
        if self.head == None:
            raise Exception("List is empty")

        #We want to get the exact index to be deleted
        count = 1
        temp = self.head
        prev = self.head.prev

        if index > self.GetCount():
            raise Exception("Data not found in list")
        
        while count < index:
            prev = temp
            temp = temp.next
            count+=1

        if temp == self.head:
            prev.next = temp.next
            #set new head and next tail node
            self.RemoveFirst()
        elif temp == self.tail:
            #set new tail and prev head node
            self.RemoveLast()
        else:
            prev.next = temp.next
            (prev.next).prev = temp.prev
        return temp

    def JumpNode(self, index):
        if self.head == None:
            raise Exception("List is empty")
            
        count = 1
        temp = self.head

        if index > self.GetCount():
            raise Exception("Index does not exist in list") 

        while count < index:
            temp = temp.next
            count+=1

        self.head = temp
        self.head.prev = self.tail
        self.tail.next = self.head  

    #Get the node
    def GetNode(self, index):
        count = 0
        temp = self.head
        if index >= self.GetCount():
            return self.tail
        while count < index:
            temp = temp.next
            count+=1
        return temp

    #Print the linked list
    def PrintList(self):
        temp = self.head
        nodesinlist = ""
        while (temp.next != self.head):
            nodesinlist += temp.data + " "
            temp = temp.next
        nodesinlist += temp.data
        return nodesinlist
    
    #Get count of linked list
    def GetCount(self):
        temp = self.head
        #Count starts from one because increment for head is missing in loop
        count = 1
        while (temp.next != self.head):
            count+=1
            temp = temp.next
        return count