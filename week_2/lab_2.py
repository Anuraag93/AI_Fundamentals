from time import time
class Node:
    # Initialization function, run at class creation
    def __init__(self, puzzle):
        # List to store child nodes
        self.children = []
        # Variable, to store parent node (note: the root nodes parent is "None")
        self.parent = None
        # Current nodes puzzle state, set from the input parameter
        self.puzzle = puzzle
        # Index of zero tile in current puzzle (set in a future function)
        self.zero = 0

    def create_child(self, puzzle):
        # Create a child Node object using the input puzzle
        child = Node(puzzle)
        # Store the child node in the children list of the current node
        self.children.append(child)
        # Store the current node as the parent of the child node
        child.parent = self
    
    def move_right(self):
        # Check that the zero-tile is not in the right column
        if (self.zero + 1) % 3 != 0:
            # Create a copy of the current nodes puzzle to store the child's modified version
            puzzle_copy = self.puzzle[:]
            # Swap the position of the zero tile and the tile to its right
            puzzle_copy[self.zero], puzzle_copy[self.zero + 1] = puzzle_copy[self.zero + 1], puzzle_copy[self.zero]
            # Create a child node using the newly modified puzzle
            self.create_child(puzzle_copy)

    def move_left(self):
        # Check that the zero-tile is not in the left column
        if self.zero % 3 != 0:
            # Create a copy of the current nodes puzzle to store the child's modified version
            puzzle_copy = self.puzzle[:]
            # Swap the position of the zero tile and the tile to its left
            puzzle_copy[self.zero], puzzle_copy[self.zero - 1] = puzzle_copy[self.zero - 1], puzzle_copy[self.zero]
            # Create a child node using the newly modified puzzle
            self.create_child(puzzle_copy)
   
    def move_up(self):
        # Check that the zero-tile is not in the top row
        if self.zero > 2:
            # Create a copy of the current nodes puzzle to store the child's modified version
            puzzle_copy = self.puzzle[:]
            # Swap the position of the zero tile and the tile above it
            puzzle_copy[self.zero], puzzle_copy[self.zero - 3] = puzzle_copy[self.zero - 3], puzzle_copy[self.zero]
            # Create a child node using the newly modified puzzle
            self.create_child(puzzle_copy)
   
    def move_down(self):
        # Check that the zero-tile is not in the bottom row
        if self.zero < 6:
            # Create a copy of the current nodes puzzle to store the child's modified version
            puzzle_copy = self.puzzle[:]
            # Swap the position of the zero tile and the tile below it
            puzzle_copy[self.zero], puzzle_copy[self.zero + 3] = puzzle_copy[self.zero + 3], puzzle_copy[self.zero]
            # Create a child node using the newly modified puzzle
            self.create_child(puzzle_copy)

    def goal_test(self):
        # Loop over length of puzzle
        for i in range(len(self.puzzle)):
            if i != self.puzzle[i]:
                # If Every tile of the puzzle is not correct, return false
                return False
        # If Every tile of the puzzle is correct, return true
        return True 

    def expand_node(self):
        # Loop over the current puzzle and find the index of the zero-tile
        for i in range(len(self.puzzle)):
            if self.puzzle[i] == 0:
                self.zero = i
        self.move_right()
        self.move_left()
        self.move_up()
        self.move_down()

    def print_puzzle(self):
        print()
        m = 0
        for i in range(3):
            for j in range(3):
                print(self.puzzle[m], end=" ")
                m += 1
            print()

    def is_unsolvable(self):
        print(self.puzzle)
        count = 0
        for i in range(8):
            for j in range(i, 9):
                if self.puzzle[i] > self.puzzle[j] and self.puzzle[j] != 0:
                    count += 1
        if count % 2 == 1:
            return True
        else:
            return False

class Search:
    def breadth_first_search(self, root):
        # List to contain open nodes
        open_list = []
        # Set to contain visited nodes
        visited = set()
        # Add root node as open
        open_list.append(root)
        # Add root node as a visited state
        visited.add(tuple(root.puzzle))
        
        while(True):
            # print(visited)
            # Get next node to search from the top of the list of open nodes
            current_Node = open_list.pop(0)
            # Check if the current node is the goal state
            if current_Node.goal_test():
                # If we have found the goal state, store the path to the current state
                path_to_solution = self.path_trace(current_Node)
                # and, print out total number of moves to reach goal state
                print(len(visited))
                return path_to_solution

            # If current node is not the goal state, then find its neighbouring nodes
            current_Node.expand_node()
        
            # Loop through all nodes neighbouring the current node
            for current_child in current_Node.children:
                # If neighbouring child hasn't previously been visited
                if (not (tuple(current_child.puzzle) in visited)):
                    # Add neighbouring child to list of open nodes
                    open_list.append(current_child)
                    # Add current child to set of visited nodes
                    visited.add(tuple(current_child.puzzle))
    
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
    # The puzzle to be solved, you can modify this for any other configuration.
    puzzle = [6, 7, 5, 4, 3, 0, 2, 1, 8]
    # Create the root node of the puzzle
    root_puzzle = Node(puzzle)
    # Check if the puzzle is solvable
    if root_puzzle.is_unsolvable():
        print("Puzzle has no solution!")
    else:
        # Create the Search object
        search = Search()
        print("Finding solution...")
        # Get the time at the start of the search
        start = time()
        # Search for and get the solution using BFS
        solution_path = search.breadth_first_search(root_puzzle)
        # Get the time at the end of the search
        end = time()
        # Reverse the solution path so that we can print inital_node to goal_node
        solution_path.reverse()
        # Loop throguh solution path nodes
        for i in range(len(solution_path)):
            # Print out node puzzle
            solution_path[i].print_puzzle()
        print("Number of steps taken:", len(solution_path)-1)
        print("Elapsed time:", end-start)
