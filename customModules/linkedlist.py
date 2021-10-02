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

    #Add nodes at the start
    #perhaps i don't really need this, considering how you cannot reverse the song queue
    # def AtStart(self, newdata):
    #     NewNode = Node(newdata)
    #     NewNode.next = self.head
    #     self.head = NewNode

    #Add a head node
    def NextNode(self):
        if(self.head is not None):
            self.head = self.head.next
            return
        self.tail = None

    #Add nodes at the end
    def AddEnd(self, newdata):
        NewNode = Node(newdata)
        if self.head is None:
            self.head = self.tail = NewNode
            return

        NewNode.prev = self.tail
        self.tail.next = NewNode
        self.tail = self.tail.next

    #Add nodes at selected index
    def InsertBefore(self, index, new_node):  
        temp = self.head

        NewNode = Node(new_node)

        count = 0
        if self.head is None:
            self.head = self.tail = NewNode
            return

        #Find the correct index if playlist not empty
        while temp:
            #We check for the prev because the new song will not go beyond the tail
            # if temp == self.tail:
            #     temp2 = temp.prev
            #     self.tail.next = temp2
            #     return

            if count == index:
                temp.next = NewNode
                temp = temp.next
                # NewNode.prev = temp.prev
                # NewNode.next = temp
                # temp = NewNode
                return  
            count+=1
            temp = temp.next

        #Add to the end if index not found
        self.tail.next = NewNode
        temp = self.tail
        self.tail = self.tail.next
        self.tail.prev = temp
    
    def RemoveNode(self, index):
        if self.head == None:
            raise Exception("List is empty")

        count = 0
        temp = self.head

        if index == 0:
            self.head = temp.next
            return

        #Find the correct index if playlist not empty
        while temp is not None:
            if temp == self.tail:
                self.tail = prev
                return temp

            if count == index:  
                prev.next = temp.next
                return temp
            count+=1
            prev = temp
            temp = temp.next

        raise Exception("Data not found in list")

    def JumpNode(self, index):
        if self.head == None:
            raise Exception("List is empty")
            
        count = 0
        temp = self.head

        while temp:
            if count == index:
                self.head = temp
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

