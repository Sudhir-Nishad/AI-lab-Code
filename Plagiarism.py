import heapq

def levenshtein_distance(s1, s2):
    """Calculate the Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def heuristic_function(remaining_sentences1, remaining_sentences2):
    """Estimate remaining cost based on the remaining sentences."""
    return sum(levenshtein_distance(s1, s2) for s1, s2 in zip(remaining_sentences1, remaining_sentences2))

def a_star_search(sentences1, sentences2):
    """A* search algorithm to align sentences between two documents."""
    open_list = []
    heapq.heappush(open_list, (0, 0, [], sentences1, sentences2))  # (total_cost, g(n), path, remaining sentences)
    visited = set()  # To keep track of visited states

    while open_list:
        total_cost, g_n, path, remaining1, remaining2 = heapq.heappop(open_list)

        # If all sentences from both documents are aligned
        if not remaining1 and not remaining2:
            return path

        state = (tuple(remaining1), tuple(remaining2))
        if state in visited:
            continue
        visited.add(state)

        # Explore all possibilities
        if remaining1:  # If there are sentences left in document 1
            for i, s1 in enumerate(remaining1):
                if remaining2:  # If there are sentences in document 2
                    for j, s2 in enumerate(remaining2):
                        # Calculate the cost of aligning sentences
                        edit_cost = levenshtein_distance(s1, s2)
                        new_path = path + [(s1, s2)]
                        new_g_n = g_n + edit_cost
                        remaining_sentences1 = remaining1[i + 1:]  # Remaining sentences in document 1
                        remaining_sentences2 = remaining2[j + 1:]  # Remaining sentences in document 2
                        h_n = heuristic_function(remaining_sentences1, remaining_sentences2)
                        new_total_cost = new_g_n + h_n
                        heapq.heappush(open_list, (new_total_cost, new_g_n, new_path, remaining_sentences1, remaining_sentences2))

    return None  # If no alignment found

# Example documents
doc1 = [
    "The cat sat on the mat.",
    "The dog barked.",
    "The quick brown fox jumps over the lazy dog."
]

doc2 = [
    "The quick brown fox jumps over the lazy dog.",
    "A dog barks.",
    "The cat is on the mat."
]

# Run A* search for text alignment
aligned_pairs = a_star_search(doc1, doc2)

# Output the results
if aligned_pairs:
    print("Aligned Sentences:")
    for s1, s2 in aligned_pairs:
        print(f"Doc1: {s1} <-> Doc2: {s2}")
else:
    print("No alignment found.")
