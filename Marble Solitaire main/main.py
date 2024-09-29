# main.py

from marble_solitaire.board import create_initial_board, create_goal_board
from marble_solitaire.solver import best_first_search, a_star_search

def main():
    initial_board = create_initial_board()
    goal_board = create_goal_board()

    print("Initial Board:")
    for row in initial_board:
        print(row)

    print("\nGoal Board:")
    for row in goal_board:
        print(row)

    print("Solving Marble Solitaire with Best-First Search:")
    best_first_solution = best_first_search(initial_board, goal_board)
    if best_first_solution:
        print("Solution Found:", best_first_solution)
    else:
        print("No Solution Found with Best-First Search.")

    print("\nSolving Marble Solitaire with A* Search:")
    a_star_solution = a_star_search(initial_board, goal_board)
    if a_star_solution:
        print("Solution Found:", a_star_solution)
    else:
        print("No Solution Found with A* Search.")

if __name__ == "__main__":
    main()
