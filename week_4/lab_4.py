import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class Graph():
    def __init__(self, adjacency_matrix):
        # Initialize vertices count and store adjacency matrix
        self.num_vertices = len(adjacency_matrix)
        self.graph = adjacency_matrix
    def get_colours(self, max_num_colours):
        # Initialize list to store colours, of same length as number of vertices
        colour_map = [0] * self.num_vertices
        # Try to colour graph
        if self.get_colours_recursive(max_num_colours, colour_map, 0) == None:
            # If get_colours_recursive fails and returns None,
            # The algorithm has failed to find a solution.
            return False
        # If get_colours_recursive return True,
        # we can return the solution colour_map list.
        return colour_map
    
    def get_colours_recursive(self, max_num_colours, colour_map, vertex):
        # Recursive function that solves colouring for the graph
        # if this is the final vertex
        if vertex == self.num_vertices:
            # All other vertices have been coloured,
            # and the current vertex colour is already set as 0 by default,
            # so we can now exit out of this recursive function.
            return True
        # For all colours in within the max range
        for colour in range(1, max_num_colours+1):
            # If the current vertex is allowed to be this colour
            if self.colour_is_safe(vertex, colour_map, colour) == True:
                # Store the colour in the colour_map
                colour_map[vertex] = colour
                # Recursively call this same function for the next vertex (vertex+1)
                if self.get_colours_recursive(max_num_colours, colour_map, vertex+1) == True:
                    # If this is true, it means we have reached the end of the recursion loop from above.
                    # All colours have been successfully set
                    return True
                colour_map[vertex] = 0
    
    def colour_is_safe(self, vertex, colour_map, colour):
        # Function to check if current colour is allowed to be assigned to this vertex.
        # For all vertices in the same row as the current vertex in the graph;
        for i in range(self.num_vertices):
            # If the colour for the vertex at this index is the same as the current vertex;
            if self.graph[vertex][i] == 1 and colour_map[i] == colour:
                # Return False, meaning that this colour is not correct.
                return False
        return True

def show_graph(adjacency_matrix, color_map):
    # Storing the row and column index for the adjacency matrix where adajency_matrix[row][column] == 1
    rows, cols = np.where(adjacency_matrix == 1)
    # Zip function "zips" together the values at each index of the list
    # e.g. zip([1,2,3],[4,5,6]) -> [(1,4),(2,5),(3,6)]
    edges = zip(rows.tolist(), cols.tolist())
    # Instantiate a graph object using the networkx library
    gr = nx.Graph()
    # Add our edges
    gr.add_edges_from(edges)
    # Create the drawing, setting parameters as required
    nx.draw(gr, node_size=500, with_labels=True, node_color=color_map)
    # use matplotlib to display the plot
    plt.show()

if __name__ == "__main__":
    # Declare your adjacency matrix,
    # Ensure this entered correctly and is symmetrical.
    adjacency_matrix = [[0, 1, 1, 1, 0],
                        [1, 0, 1, 0, 0],
                        [1, 1, 0, 1, 1],
                        [1, 0, 1, 1, 1],
                        [0, 0, 1, 1, 0]]
    # Create your graph object
    graph = Graph(adjacency_matrix)
    # Set number of colours
    max_num_colours = 2
    # Store calculated colour mapping
    color_map = graph.get_colours(max_num_colours)
    
    if color_map == False:
        # If colour mapping failed
        print("Failed to complete colour mapping!")
    else:
        # If colour mapping succeeded, display graph
        show_graph(np.asarray(adjacency_matrix), color_map)
