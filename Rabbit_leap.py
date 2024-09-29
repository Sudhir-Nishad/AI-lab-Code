from collections import deque

# Define the initial state, goal state, and empty stone position
initial_state = ['E', 'E', 'E', '_', 'W', 'W', 'W']  # Three east-bound 'E', one empty stone '_', three west-bound 'W'
goal_state = ['W', 'W', 'W', '_', 'E', 'E', 'E']

# Helper function to check if a state is valid
def is_valid_state(state):
    return True  # All states are valid in this problem

# Function to swap positions in the list
def swap_positions(state, i, j):
    new_state = state[:]
    new_state[i], new_state[j] = new_state[j], new_state[i]
    return new_state

# Function to get next possible states
def get_next_states(state):
    empty_index = state.index('_')
    next_states = []

    # Possible moves (left, right, jump)
    moves = [-1, -2, 1, 2]
    
    for move in moves:
        new_index = empty_index + move
        if 0 <= new_index < len(state):
            # Swap the empty stone with the rabbit
            new_state = swap_positions(state, empty_index, new_index)
            if is_valid_state(new_state):
                next_states.append(new_state)
    
    return next_states

# BFS to solve the rabbit leap problem
def bfs_rabbit_leap(initial_state, goal_state):
    queue = deque([(initial_state, [])])  # (current state, path)
    visited = set()
    visited.add(tuple(initial_state))

    while queue:
        current_state, path = queue.popleft()

        # Check if goal state is reached
        if current_state == goal_state:
            return path + [current_state]  # Return the solution path

        # Get all next possible states
        next_states = get_next_states(current_state)
        
        for next_state in next_states:
            if tuple(next_state) not in visited:
                visited.add(tuple(next_state))
                queue.append((next_state, path + [current_state]))
    
    return None  # No solution found

# Run the BFS to find the solution
solution = bfs_rabbit_leap(initial_state, goal_state)
if solution:
    print("Solution found!")
    for step in solution:
        print(step)
else:
    print("No solution exists.")
