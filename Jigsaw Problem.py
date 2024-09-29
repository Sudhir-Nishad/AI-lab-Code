import random
import numpy as np
import math

# Define the jigsaw puzzle size
PUZZLE_SIZE = 3  # For a 3x3 puzzle
NUM_PIECES = PUZZLE_SIZE ** 2

# Create a goal state for a 3x3 puzzle
goal_state = np.arange(1, NUM_PIECES).tolist() + [0]  # 0 represents the empty space

# Function to generate a random initial state
def generate_initial_state():
    state = goal_state[:-1]  # Remove the empty space
    random.shuffle(state)
    return state + [0]  # Add the empty space at the end

# Function to calculate the cost of a puzzle state
def calculate_cost(state):
    cost = 0
    for index, value in enumerate(state):
        if value != 0 and value != index + 1:
            cost += 1  # Increment cost for each misalignment
    return cost

# Function to generate neighbors by swapping the empty space with adjacent pieces
def generate_neighbors(state):
    neighbors = []
    empty_index = state.index(0)
    row, col = divmod(empty_index, PUZZLE_SIZE)

    # Define possible moves: left, right, up, down
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # (delta_row, delta_col)

    for dr, dc in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < PUZZLE_SIZE and 0 <= new_col < PUZZLE_SIZE:
            # Calculate the index of the piece to swap
            swap_index = new_row * PUZZLE_SIZE + new_col
            new_state = state.copy()
            new_state[empty_index], new_state[swap_index] = new_state[swap_index], new_state[empty_index]
            neighbors.append(new_state)
    return neighbors

# Simulated Annealing algorithm
def simulated_annealing(initial_state):
    # Step 1: Initialize parameters
    temperature = 1000
    cooling_rate = 0.95
    current_solution = initial_state
    current_cost = calculate_cost(current_solution)
    best_solution = current_solution
    best_cost = current_cost

    # Step 2: Main loop until the system cools down
    while temperature > 1:
        # Step 2.1: Generate a new possible puzzle configuration
        new_solution = random.choice(generate_neighbors(current_solution))
        new_cost = calculate_cost(new_solution)

        # Step 2.2: Compute the cost difference between the new and current configuration
        cost_difference = new_cost - current_cost

        # Step 2.3: Decide whether to accept the new configuration
        if cost_difference < 0:  # If the new configuration is better
            current_solution = new_solution
            current_cost = new_cost
        else:  # If the new configuration is worse, accept with a probability
            acceptance_probability = math.exp(-cost_difference / temperature)
            if random.random() < acceptance_probability:
                current_solution = new_solution
                current_cost = new_cost

        # Step 2.4: Update the best solution if a better one is found
        if current_cost < best_cost:
            best_solution = current_solution
            best_cost = current_cost

        # Step 2.5: Cool down the system by reducing the temperature
        temperature *= cooling_rate

    # Step 3: Return the best solution found
    return best_solution

# Main execution
if _name_ == "_main_":
    initial_state = generate_initial_state()
    print("Initial State:", initial_state)
    solution = simulated_annealing(initial_state)
    print("Solved State:", solution)
    print("Cost of Solved State:", calculate_cost(solution))