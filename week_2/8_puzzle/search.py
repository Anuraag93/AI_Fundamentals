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
    
    def depth_first_search(self, root):
        # List to contain open nodes
        open_list = []
        # Set to contain visited nodes
        visited = set()
        # Add root node as open
        open_list.append(root)
        # Add root node as a visited state
        visited.add(tuple(root.puzzle))
        
        while(True):
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
                    open_list.insert(0, current_child)
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
