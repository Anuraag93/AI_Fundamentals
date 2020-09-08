class Node():
    def __init__(self, parent=None, position=None):
        # Initialize all attributes that we want a node to have
        # List to store child nodes
        self.children = []
        # Store parent node for later path tracing
        self.parent = parent
        # Store position of node, with respect to puzzle
        self.position = position
        # Store the g,h, and f values
        self.g = 0
        self.h = 0
        self.f = 0
    
    def expand(self, puzzle):
        # Loop through all possible movements
        for movement in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            
            # Get node position after moving
            node_position = (self.position[0] + movement[0], self.position[1] + movement[1])
            
            # Check that the new node is within the boundaries of the puzzle
            if node_position[0] <= (len(puzzle) - 1) and node_position[0] >= 0 and node_position[1] <= (len(puzzle[len(puzzle)-1]) - 1) and node_position[1] >= 0:
                # Check if its trying to move into a position occupied by a wall
                if puzzle[node_position[0]][node_position[1]] == 0:
                    # Create new child
                    child = Node(self, node_position)
                    self.children.append(child)

def a_star_search(puzzle, start, end):
    # initialize node with no parent and "start" coords
    start_node = Node(None, start)
    # initialize node with unknown parent and "end" coords
    end_node = Node(None, end)
    # Initialize both open and closed list
    open_list = []
    closed_list = []
    # Add the start node
    open_list.append(start_node)
    # Loop until you find the end
    while len(open_list) > 0:
        # Get the current node
        current_node = open_list.pop(0)
        closed_list.append(current_node)
        # Check if it is the goal node
        if current_node.position == end_node.position:
            path_to_solution = []
            current = current_node
            while current is not None:
                path_to_solution.append(current.position)
                current = current.parent
            return list(reversed(path_to_solution))

        # # Generate children
        current_node.expand(puzzle)
        
        # Loop through children
        for child in current_node.children:
            flag = False
            # if the child with the same position isnt in the closed list:
            for closed_child in closed_list:
                if child.position == closed_child.position:
                    flag = True
            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h
            # Child is already in the open list
            for open_node in open_list:
                if child.position == open_node.position and child.g > open_node.g:
                    # Dont add child to the open_list, move on to next one
                    flag = True
            # Add the child to the open list
            if flag == False:
                open_list.append(child)
        open_list.sort(key=lambda x: x.f)
    print("No Solution Found!")

if __name__ == '__main__':
    puzzle = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]
    start_point = (0, 0)
    end_point = (0, 8)
    path = a_star_search(puzzle, start_point, end_point)
    print(path)