from collections import deque

# Define the maze as a grid
# 0 = open space, 1 = wall
maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
]

# Directions for moving up, down, left, right
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Function to check if a position is valid
def is_valid(maze, pos):
    row, col = pos
    return (0 <= row < len(maze) and
            0 <= col < len(maze[0]) and
            maze[row][col] == 0)

# BFS function to find the shortest path in the maze
def bfs(maze, start, goal):
    queue = deque([start])  # Initialize the queue with the start position
    visited = {start}       # Use a hash table to track visited nodes
    parent_map = {start: None}  # To reconstruct the path

    while queue:
        current = queue.popleft()  # Dequeue the front node

        # Check if we reached the goal
        if current == goal:
            path = []
            while current is not None:  # Reconstruct the path
                path.append(current)
                current = parent_map[current]
            return path[::-1]  # Return reversed path
        
        # Explore neighbors
        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if is_valid(maze, neighbor) and neighbor not in visited:
                visited.add(neighbor)  # Mark neighbor as visited
                queue.append(neighbor)  # Enqueue the neighbor
                parent_map[neighbor] = current  # Record parent to reconstruct path

    return None  # Return None if no path is found

# Define start and goal positions
start = (0, 0)  # Top-left corner
goal = (4, 4)   # Bottom-right corner

# Run BFS to find the path
path = bfs(maze, start, goal)

# Output the result
if path:
    print("Path found:", path)
else:
    print("No path found.")
