from time import time, sleep 
from copy import deepcopy
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class Node:
    def __init__(self, stacks=None, ring_count=3, stack_count=3, initial_stack_index=0):
        # List to store child nodes
        self.children = []
        # Variable, to store parent node (note: the root nodes parent is "None")
        self.parent = None
        # Current state for this nodes Stacks/Poles/Columns
        self.stacks = stacks
        # Storing the total number of rings for later use
        self.ring_count = ring_count
        
        # We use this to initialize the root stacks
        # This is only executed for the root node, as self.stacks is None
        if self.stacks is None:
            # Create a List of Empty Lists of length stack_count
            # E.g. if stack_count = 3
            # self.stacks will be [[],[],[]]
            self.stacks = [[] for i in range(stack_count)]
            for i in range(self.ring_count):
                # This will loop over the total number of specified rings, adding each
                # ring to the top of the stack at the index initial_stack_index
                self.stacks[initial_stack_index].append(i)
    
    def create_child(self, stacks):
        # Create a child Node object using the input stacks
        child = Node(stacks, ring_count=self.ring_count)
        # Store the current node as the parent of the child node
        child.parent = self
        # Store the child node in the children list of the current node
        self.children.append(child)

    def move_ring(self, from_stack, to_stack):
        # We need to check,
        # - if the stack we are moving FROM is empty:
        # - "len(self.stacks[from_stack])" will be False if the stack is empty
        #
        # - if the stack we are TO from is empty:
        # - This is for if we select a initial_stack_index != 0
        # - If we don't check this, it will throw an error if we try to "pop" off an empty list
        #
        # - and if the disc we are moving (self.stacks[from_stack][0]) is
        # smaller than the disc at the move location (self.stacks[to_stack][0])
        if len(self.stacks[from_stack]) and (not self.stacks[to_stack] or self.stacks[to_stack][0] > self.stacks[from_stack][0]):
            # We use deepcopy to create a stack_copy we can modify without changing the original
            stacks_copy = deepcopy(self.stacks)
            # We place the disc on the TOP of the specified stack, also removing it from the original stack with "pop"
            # Note: "Insert" puts at FRONT of list
            # and "Append" puts at END of list
            stacks_copy[to_stack].insert(0, stacks_copy[from_stack].pop(0))
            # Create the child, using the newly moved stack
            self.create_child(stacks_copy)

    def expand_node(self):
        # To expand out node, we must check all possible movements
        number_of_stacks = len(self.stacks)
        
        for i in range(number_of_stacks):
            for j in range(number_of_stacks):
                # This will attempt to move the top disc of all stacks to all other stacks
                # Our move function will decide whether this move is possible or not
                self.move_ring(i, j)

    def is_correct(self):
        # In order for our node to be correct,
        # we know that all discs must be arranged in the final stack,
        # and they must be in the correct order 0->5
        for i in range(self.ring_count):
            # Loop from 0->ring_count
            try:
                # If the disc in the ith position of the last stack = i from our loop
                if self.stacks[len(self.stacks)-1][i] == i:
                    # we do nothing and continue checking
                    pass
            except:
                # An exception will be triggered if self.stacks[len(self.stacks)-1][i] doesn't exist
                # This means that the there is no disc in the ith position of the last stack.
                # In this case we know that we havn't found the objective and can return False.
                # i.e. if i=5 and the last_stack = [0,1,2,3,4]
                # when we check last_stack[i] it will enter this exception as that index doesn't exist.
                return False
        # If we reach this point, we know that we have found the objective!
        return True

    def print_stacks(self, delay_increment=0.03):
        # These two imports are based on your environment
        
        # This function is just a utility to display the stacks in a easy to read way
        max_height = self.ring_count
        for ring_height in range(max_height, 0, -1):
            for stack_index in range(len(self.stacks)):
                if len(self.stacks[stack_index]) >= ring_height:
                    print(self.stacks[stack_index][-ring_height], end="")
                else:
                    print(" ", end="")
            print("")
        print("*-*")
        sleep(delay_increment)
        # Select one of these based on your environment
        # Leave these commented out if you want to view all node configurations
        # system('clear') # This will clear a terminal/command prompt output
        # clear_output(wait=True) # This will clear a Jupyter Notebooks output

class Search:
    def depth_first_search(self, root):
        # List to contain open nodes
        open_list = []
        # Set to contain visited nodes
        visited = set()
        # Add root node as open
        open_list.append(root)
        # Add root node as a visited state
        visited.add(tuple(map(tuple, root.stacks)))
        while(True):
            # Get next node to search from the top of the list of open nodes
            current_node = open_list.pop(0)
            # Check if the current node is the goal state
            if current_node.is_correct():
                # If we have found the goal state, store the path to the current state
                path_to_solution = self.path_trace(current_node)
                return path_to_solution, len(visited)
            # If current node is not the goal state, then find its neighbouring nodes
            current_node.expand_node()
            # Loop through all nodes neighbouring the current node
            for current_child in current_node.children:
                # If neighbouring child hasn't previously been visited
                if (not tuple(map(tuple, current_child.stacks)) in visited):
                    # Add neighbouring child to list of open nodes
                    # Using the "Insert" Function puts the current child to the front of the open_list
                    # This will make it Depth First Search
                    open_list.insert(0, current_child)
                    # Add current child to set of visited nodes
                    visited.add(tuple(map(tuple, current_child.stacks)))

    def path_trace(self, node):
        # Store the input node
        current = node
        # Create a list named path, this will store all nodes in the path
        path = []
        # Append the initial node to the path list
        path.append(current)
        # Loop while our current node isn't the root node (as our root node's parent is "None")
        while current.parent != None:
            # Set current node to the parent of the previous node
            current = current.parent
            # Append the current node to the path list
            path.append(current)
        # Return the final path from root node to goal node
        return path

if __name__ == "__main__":
    # Initialize our puzzle, we specify 6 rings, 3 stacks
    # and that we want the rings to be generated on stack 0
    root = Node(ring_count=6, stack_count=3, initial_stack_index=0)
    search = Search()
    
    # Capture the search start time
    time_start = time()
    # Execute the search and store the returned variables
    path_to_solution, visited_nodes_count = search.depth_first_search(root)
    # Capture the search end time
    time_end = time()
    
    # Reverse our stored path so that we can view it in correct order
    path_to_solution.reverse()
    
    # Display the stacks at each node in our solution
    for node in path_to_solution:
        # Modify the delay_increment in this function call to increase/decrease
        # the speed at which each node is displayed
        node.print_stacks(delay_increment=0.01)
    # Print out our results
    print("Total Nodes Visited During Search:", visited_nodes_count)
    print("Final Path Node Count :", len(path_to_solution)-1)
    print("Total Elapsed Search Time : {:.5f} s".format(time_end-time_start))