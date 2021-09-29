from os import remove


class Node:
   def __init__(self, data=None, position=0):
      self.data = data
      self.next = None
      self.prev = None
      self.position = position

class SLinkedList:
    def __init__(self):
      self.head = None
      self.tail = None

    #Add nodes at the start
    #perhaps i don't really need this, considering how you cannot reverse the song queue
    # def AtStart(self, newdata):
    #     NewNode = Node(newdata)
    #     NewNode.next = self.head
    #     self.head = NewNode

    #Add a head node
    def NextNode(self):
        if(self.head is not None):
            self.head.prev = None
            self.head = self.head.next

    #Add nodes at the end
    def AddEnd(self, newdata):
        NewNode = Node(newdata)
        if self.head is None:
            self.head = self.tail = NewNode
            return
        self.tail.next = NewNode
        self.tail = self.tail.next
        self.reset_position()

    #Add nodes in between
    def Inbetween(self, index, new_node):  
        NewNode = Node(new_node)
        count = 0
        temp = self.head
        if self.head is None:
            self.head = self.tail = NewNode
            self.reset_position()
            return

        #Find the correct index if playlist not empty
        while temp:
            #Add to end if index is at the end of list
            if temp == self.tail:
                self.tail.next = NewNode
                self.tail = self.tail.next
                self.reset_position()
                return

            if count == index:
                NewNode.next = temp.next
                temp.next = NewNode
                self.reset_position()
                return  
            count+=1
            temp = temp.next

        #Add to the end if index not found
        self.tail.next = NewNode
        self.tail = self.tail.next
        self.reset_position()

    def AddStart(self, newdata):
        NewNode = Node(newdata)
        if self.head is None:
            self.head = self.tail = NewNode
            return
        NewNode.next = self.head
        self.head = NewNode
    
    def RemoveNode(self, removedata):
        if self.head == None:
            raise Exception("List is empty")

        if self.head.data == removedata:
            self.head = self.head.next
            self.reset_position()
            return
        
        if self.tail.data == removedata:
            self.tail = self.tail.prev
            self.reset_position()
        
        previous_node = self.head
        for node in self:
            if node.data == removedata:
                previous_node.next = node.next
                self.reset_position()
                return
            previous_node = node

        raise Exception("Data not found in list")

    def JumpNode(self, index):
        if self.head == None:
            raise Exception("List is empty")
            
        count = 0
        temp = self.head

        while temp:
            if count == index:
                self.head = temp
                self.reset_position()
                return  
            count+=1
            temp = temp.next

        raise Exception("Index does not exist in list")    

    #Print the linked list
    def PrintList(self):
        printval = self.head
        while printval is not None:
            print (printval.data)
            printval = printval.next
    
    #Get count of linked list
    def GetCount(self):
        temp = self.head
        count = 0
        while (temp):
            count+=1
            temp = temp.next
        return count

    #Correct the positions of nodes
    def reset_position(self):
        position = 0
        temp = self.head
        while (temp):
            temp.position = position
            position+=1
            temp = temp.next

