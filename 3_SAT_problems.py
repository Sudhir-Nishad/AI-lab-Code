import random

def generate_3_sat(m, n):
    clauses = []
    for _ in range(m):
        variables = random.sample(range(1, n + 1), 3)  # Select 3 distinct variables
        clause = [(var if random.choice([True, False]) else -var) for var in variables]
        clauses.append(clause)
    return clauses

def evaluate(assignment, clauses):
    satisfied = 0
    for clause in clauses:
        if any((var > 0 and assignment[var - 1]) or (var < 0 and not assignment[-var - 1]) for var in clause):
            satisfied += 1
    return satisfied

def hill_climbing(clauses, n, heuristic_function):
    current_assignment = [random.choice([True, False]) for _ in range(n)]
    current_score = heuristic_function(current_assignment, clauses)
    
    while True:
        neighbors = []
        for i in range(n):
            neighbor = current_assignment[:]
            neighbor[i] = not neighbor[i]  # Flip the variable
            neighbors.append(neighbor)

        best_neighbor = max(neighbors, key=lambda x: heuristic_function(x, clauses))
        best_score = heuristic_function(best_neighbor, clauses)

        if best_score <= current_score:  # Stop if no better neighbor found
            break
        current_assignment, current_score = best_neighbor, best_score

    return current_assignment, current_score

def beam_search(clauses, n, beam_width, heuristic_function):
    current_beam = [[random.choice([True, False]) for _ in range(n)] for _ in range(beam_width)]
    
    while True:
        next_beam = []
        for assignment in current_beam:
            neighbors = []
            for i in range(n):
                neighbor = assignment[:]
                neighbor[i] = not neighbor[i]
                neighbors.append(neighbor)

            next_beam.extend(neighbors)

        # Keep the best assignments in the beam
        next_beam = sorted(next_beam, key=lambda x: heuristic_function(x, clauses), reverse=True)[:beam_width]

        # Check if any assignment is a solution
        for assignment in next_beam:
            if evaluate(assignment, clauses) == len(clauses):
                return assignment

        current_beam = next_beam

def variable_neighborhood_descent(clauses, n, heuristics, k):
    current_assignment = [random.choice([True, False]) for _ in range(n)]
    current_score = evaluate(current_assignment, clauses)

    for _ in range(k):
        for heuristic in heuristics:
            neighbors = []
            for i in range(n):
                neighbor = current_assignment[:]
                neighbor[i] = not neighbor[i]
                neighbors.append(neighbor)

            best_neighbor = max(neighbors, key=lambda x: heuristic(x, clauses))
            best_score = evaluate(best_neighbor, clauses)

            if best_score > current_score:
                current_assignment, current_score = best_neighbor, best_score
                break

    return current_assignment, current_score

# Heuristic Functions
def heuristic_1(assignment, clauses):
    return evaluate(assignment, clauses)

def heuristic_2(assignment, clauses):
    return len(clauses) - evaluate(assignment, clauses)

def main():
    # Parameters
    m = 5  # Number of clauses
    n = 7  # Number of variables

    # Generate a random 3-SAT problem
    clauses = generate_3_sat(m, n)

    print("Generated 3-SAT Problem Clauses:")
    for clause in clauses:
        print(clause)

    # Run Hill Climbing
    print("\nHill Climbing:")
    hc_solution, hc_score = hill_climbing(clauses, n, heuristic_1)
    print(f"Best Assignment: {hc_solution}, Satisfied Clauses: {hc_score}")

    # Run Beam Search
    print("\nBeam Search (Beam Width 3):")
    bs_solution = beam_search(clauses, n, beam_width=3, heuristic_function=heuristic_1)
    print(f"Best Assignment: {bs_solution}, Satisfied Clauses: {evaluate(bs_solution, clauses)}")

    # Run Variable Neighborhood Descent
    print("\nVariable Neighborhood Descent:")
    vnd_solution, vnd_score = variable_neighborhood_descent(clauses, n, [heuristic_1, heuristic_2], k=3)
    print(f"Best Assignment: {vnd_solution}, Satisfied Clauses: {vnd_score}")

if __name__ == "__main__":
    main()
