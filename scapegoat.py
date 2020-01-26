import math
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None

class Scapegoat:
    def __init__(self,a):
        self.a = a
        self.root = None
        self.size = 0
        self.maxSize = 0

    def insert(self, key):
        node = Node(key)
        #Base Case - Nothing in the tree
        if self.root == None:
            self.root = node
            return
        #Search to find the node's correct place
        currentNode = self.root
        while currentNode != None:
            potentialParent = currentNode
            if node.key < currentNode.key:
                currentNode = currentNode.left
            else:
                currentNode = currentNode.right
        #Assign parents and siblings to the new node
        node.parent = potentialParent
        if node.key < node.parent.key:
            node.parent.left = node
        else:
            node.parent.right = node
        node.left = None
        node.right = None
        self.size += 1
        scapegoat = self.findScapegoat(node)
        if scapegoat == None:
            return
        tmp = self.rebalance(scapegoat)

        #Assign the correct pointers to and from scapegoat
        scapegoat.left = tmp.left
        scapegoat.right = tmp.right
        scapegoat.key = tmp.key
        scapegoat.left.parent = scapegoat
        scapegoat.right.parent = scapegoat

    def findScapegoat(self, node):
        if node == self.root:
            return None
        while self.isBalancedAtNode(node) == True:
            if node == self.root:
                return None
            node = node.parent
        return node

    def isBalancedAtNode(self, node):
        if abs(self.sizeOfSubtree(node.left) - self.sizeOfSubtree(node.right)) <= 1:
            return True
        return False

    def sizeOfSubtree(self, node):
        if node == None:
            return 0
        return 1 + self.sizeOfSubtree(node.left) + self.sizeOfSubtree(node.right)

    def rebalance(self, root):
        def flatten(node, nodes):
            if node == None:
                return
            flatten(node.left, nodes)
            nodes.append(node)
            flatten(node.right, nodes)

        def buildTreeFromSortedList(nodes, start, end):
            if start > end:
                return None
            mid = int(math.ceil(start + (end - start) / 2.0))
            node = Node(nodes[mid].key)
            node.left = buildTreeFromSortedList(nodes, start, mid-1)
            node.right = buildTreeFromSortedList(nodes, mid+1, end)
            return node

        nodes = []
        flatten(root, nodes)
        return buildTreeFromSortedList(nodes, 0, len(nodes)-1)
    
    def delete(self,delete_me):
        node = self.root
        parent = None
        is_left_child = True
        # find the node, keep track of the parent, and side of the tree
        while node.key != delete_me:
            parent = node
            if delete_me > node.key:
                node = node.right
                is_left_child = False
            else:
                node = node.left
                is_left_child = True

        successor = None
        # case 1: Node to be delete has no children
        if node.left == None and node.right == None:
            pass
        # case 2: Node has only a right child
        elif node.left == None:
            successor = node.right
        # case 3: Node has only a left child
        elif node.right == None:
            successor = node.left
        # case 4: Node has right and left child
        else:
            # find successor
            successor = self.minimum(node.right)
            # the successor is the node's right child -- easy fix
            if successor == node.right:
                successor.left = node.left
            # complicated case
            else:
                print("finding successor")
                successor.left = node.left
                tmp = successor.right
                successor.right = node.right
                node.right.left = tmp

        # Replace the node
        if parent == None:
            self.root = successor
        elif is_left_child:
            parent.left = successor
        else:
            parent.right = successor
        self.size -= 1
        if self.size < self.a * self.maxSize:
            print( "Rebuilding the whole tree")
            self.root = self.myRebuildTree(self.root, self.size)
            self.maxSize = self.size
        
        
    def preOrder(self, x):
        if x != None:
            print(x.key)
            self.preOrder(x.left)
            self.preOrder(x.right)

    def printTree(self):
        return self.preOrder(self.root)
        
    
q=Scapegoat(9)   
q.insert(5) 
q.insert(6)
q.insert(7)
q.insert(8)
q.delete(7)
q.insert(3)
print(q.printTree())
