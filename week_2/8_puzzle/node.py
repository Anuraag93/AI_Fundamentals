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
