
import numpy as np
import random
import math

# Haversine formula to calculate distance between two points on the Earth's surface
def haversine(coord1, coord2):
    R = 6371  # Radius of Earth in kilometers
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Total tour cost calculation (sum of distances between consecutive cities)
def total_distance(tour, locations):
    distance = 0
    for i in range(len(tour)):
        city1 = locations[tour[i]]
        city2 = locations[tour[(i + 1) % len(tour)]]  # Loop back to the start
        distance += haversine(city1, city2)
    return distance

# Simulated Annealing Algorithm
def simulated_annealing(locations, initial_temp, cooling_rate, stop_temp):
    # Initial random solution
    num_locations = len(locations)
    current_solution = list(range(num_locations))
    random.shuffle(current_solution)
    current_cost = total_distance(current_solution, locations)

    best_solution = current_solution[:]
    best_cost = current_cost

    temperature = initial_temp

    while temperature > stop_temp:
        # Generate neighbor solution by swapping two cities
        neighbor = current_solution[:]
        i, j = random.sample(range(num_locations), 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

        # Calculate cost of neighbor solution
        neighbor_cost = total_distance(neighbor, locations)

        # Acceptance criterion
        cost_diff = neighbor_cost - current_cost
        if cost_diff < 0 or random.uniform(0, 1) < math.exp(-cost_diff / temperature):
            current_solution = neighbor[:]
            current_cost = neighbor_cost

            if current_cost < best_cost:
                best_solution = current_solution[:]
                best_cost = current_cost

        # Decrease temperature
        temperature *= cooling_rate

    return best_solution, best_cost

# Example usage:

# Define coordinates of 20 tourist locations in Rajasthan (latitude, longitude)
locations = [
    (26.9124, 75.7873),  # Jaipur
    (26.4499, 74.6399),  # Ajmer
    (24.5854, 73.7125),  # Udaipur
    (27.0238, 74.2179),  # Sikar
    (25.1475, 75.8391),  # Kota
    (26.4856, 74.5472),  # Kishangarh
    (28.0229, 73.3119),  # Bikaner
    (25.7490, 73.4483),  # Pali
    (26.2389, 73.0243),  # Jodhpur
    (28.6139, 77.2090),  # Delhi
    (29.0780, 75.3980),  # Hisar
    (27.9157, 75.7861),  # Pilani
    (25.7711, 73.3234),  # Barmer
    (28.6315, 74.3496),  # Churu
    (25.2080, 75.8494),  # Bundi
    (26.2937, 74.3047),  # Pushkar
    (25.3649, 74.6411),  # Bhilwara
    (25.0005, 73.3233),  # Jaisalmer
    (27.5790, 75.1734),  # Mandawa
    (26.7047, 73.1252)   # Nagaur
]

# Simulated Annealing parameters
initial_temp = 10000
cooling_rate = 0.995
stop_temp = 0.001

# Find the best tour using Simulated Annealing
best_tour, best_cost = simulated_annealing(locations, initial_temp, cooling_rate, stop_temp)

print("Best Tour:", best_tour)
print("Minimum Cost (Distance):",best_cost)