from time import time
from node import Node
from search import Search

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
        solution_path = search.depth_first_search(root_puzzle)
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
