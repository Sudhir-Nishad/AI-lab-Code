from collections import deque

# Define the initial state and goal state
initial_state = (3, 3, 'left')  # (missionaries, cannibals, boat position)
goal_state = (0, 0, 'right')

# Check if a state is valid
def is_valid_state(state):
    missionaries, cannibals, _ = state
    if missionaries < 0 or cannibals < 0 or missionaries > 3 or cannibals > 3:
        return False
    if missionaries > 0 and missionaries < cannibals:  # More cannibals than missionaries on one side
        return False
    if (3 - missionaries) > 0 and (3 - missionaries) < (3 - cannibals):  # Same on the other side
        return False
    return True

# Define the possible actions (combinations of missionaries and cannibals that can cross the river)
actions = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]  # (missionaries, cannibals)

# Function to apply action and move the boat
def apply_action(state, action):
    missionaries, cannibals, boat_position = state
    m_move, c_move = action
    if boat_position == 'left':
        new_state = (missionaries - m_move, cannibals - c_move, 'right')
    else:
        new_state = (missionaries + m_move, cannibals + c_move, 'left')
    return new_state

# Perform BFS to find the solution
def bfs_missionaries_cannibals(initial_state, goal_state):
    queue = deque([(initial_state, [])])  # (state, path)
    visited = set()
    visited.add(initial_state)

    while queue:
        current_state, path = queue.popleft()
        
        # Check if the goal state is reached
        if current_state == goal_state:
            return path + [current_state], len(path) + 1  # Return the solution path and the number of steps

        # Try all possible actions
        for action in actions:
            next_state = apply_action(current_state, action)
            
            # If the next state is valid and not visited
            if is_valid_state(next_state) and next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [current_state]))

    return None, 0  # No solution found

# Get the solution and the number of steps
solution, steps = bfs_missionaries_cannibals(initial_state, goal_state)
if solution:
    print("Solution found!")
    for step in solution:
        print(step)
    print(f"Number of steps: {steps}")
else:
    print("No solution exists.")
