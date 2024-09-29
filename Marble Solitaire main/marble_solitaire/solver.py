import heapq

def heuristic_1(board):
    return sum(row.count(1) for row in board)

def heuristic_2(board):
    center_pos = (2, 2)
    distance = 0
    for r in range(5):
        for c in range(5):
            if board[r][c] == 1:
                distance += abs(center_pos[0] - r) + abs(center_pos[1] - c)
    return distance

def get_neighbors(board):
    # Define the movement directions
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # Up, Down, Left, Right
    neighbors = []
    
    for r in range(5):
        for c in range(5):
            if board[r][c] == 1:  # If there's a marble
                for dr, dc in directions:
                    # Check if a jump is possible
                    if (0 <= r + dr < 5) and (0 <= c + dc < 5) and (0 <= r + dr // 2 < 5) and (0 <= c + dc // 2 < 5):
                        if board[r + dr][c + dc] == 0 and board[r + dr // 2][c + dc // 2] == 1:
                            # Create a new board state
                            new_board = [row[:] for row in board]
                            new_board[r][c] = 0  # Move marble
                            new_board[r + dr // 2][c + dc // 2] = 0  # Remove jumped marble
                            new_board[r + dr][c + dc] = 1  # Place marble
                            neighbors.append(new_board)

    return neighbors

def best_first_search(initial_board, goal_board):
    visited = set()
    priority_queue = []
    
    # Initial state
    heapq.heappush(priority_queue, (heuristic_1(initial_board), initial_board))

    while priority_queue:
        current_heuristic, current_board = heapq.heappop(priority_queue)

        # Check if the goal state is reached
        if current_board == goal_board:
            return current_board

        visited.add(tuple(map(tuple, current_board)))  # Add to visited

        for neighbor in get_neighbors(current_board):
            if tuple(map(tuple, neighbor)) not in visited:
                print("Exploring:", neighbor)  # Debug output
                heapq.heappush(priority_queue, (heuristic_1(neighbor), neighbor))

    return None  # No solution found

def a_star_search(initial_board, goal_board):
    visited = set()
    priority_queue = []
    
    # Initial state
    heapq.heappush(priority_queue, (0 + heuristic_1(initial_board), 0, initial_board))

    while priority_queue:
        current_cost, g_cost, current_board = heapq.heappop(priority_queue)

        # Check if the goal state is reached
        if current_board == goal_board:
            return current_board

        visited.add(tuple(map(tuple, current_board)))

        for neighbor in get_neighbors(current_board):
            if tuple(map(tuple, neighbor)) not in visited:
                # Calculate cost to reach the neighbor
                new_g_cost = g_cost + 1
                print("Exploring (A*):", neighbor)  # Debug output
                heapq.heappush(priority_queue, (new_g_cost + heuristic_1(neighbor), new_g_cost, neighbor))

    return None  # No solution found
