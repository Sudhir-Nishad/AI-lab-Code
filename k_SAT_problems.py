import random

def generate_k_sat(k, m, n):
    """
    Generate a random k-SAT problem.

    Parameters:
    k (int): Number of variables in each clause.
    m (int): Number of clauses in the formula.
    n (int): Total number of distinct variables.

    Returns:
    list: A list of clauses representing the k-SAT problem.
    """
    if k > n:
        raise ValueError("k cannot be greater than n (number of variables).")
    
    clauses = []

    for _ in range(m):
        # Randomly select k distinct variables
        variables = random.sample(range(1, n + 1), k)

        # Randomly assign each variable a negation
        clause = [(var if random.choice([True, False]) else -var) for var in variables]
        clauses.append(clause)

    return clauses

def print_k_sat(clauses):
    """
    Print the k-SAT problem in CNF format.

    Parameters:
    clauses (list): The list of clauses to print.
    """
    for clause in clauses:
        print(" ".join(map(str, clause)) + " 0")  # Append '0' to denote the end of a clause

def main():
    # Input for k, m, and n
    k = int(input("Enter the number of literals per clause (k): "))
    m = int(input("Enter the number of clauses (m): "))
    n = int(input("Enter the number of variables (n): "))

    # Generate the k-SAT problem
    k_sat_problem = generate_k_sat(k, m, n)

    # Print the generated k-SAT problem
    print("\nGenerated k-SAT Problem:")
    print_k_sat(k_sat_problem)

if __name__ == "__main__":
    main()
