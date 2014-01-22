# http://habrahabr.ru/post/209610/

import numpy as np
import matplotlib.pyplot as plt
import math

# Generate sities coordinates
cities = []
np.random.seed(123)
cities = np.random.randint(0, 100, size=(10, 2))

def draw_route(cities, E, n = 1):
    # Add 1st city to the end
    data_to_draw = np.concatenate(( cities, [cities[0]] ))

    plt.annotate('Route number: ' + str(n), xy=(0.05, 0.95), xycoords='axes fraction')
    plt.annotate('Route length: ' + str(round(E,2)), xy=(0.05, 0.90), xycoords='axes fraction')
    plt.scatter(*zip(*data_to_draw))
    plt.plot(*zip(*data_to_draw))
    # Save to disk
    plt.savefig('c:/simulated_annealing/route' + str(n) + '.png')
    #plt.show()
    plt.clf()

def calculate_energy(cities):
    n = len(cities)
    E = 0
    for i in range(1, n):
        # distance between neighbours
        distance = (cities[i-1][0] - cities[i][0])**2 + (cities[i-1][1] - cities[i][1])**2
        distance = math.sqrt(distance)
        E += distance

    from_last_to_first = (cities[n-1][0] - cities[0][0])**2 + (cities[n-1][1] - cities[0][1])**2
    from_last_to_first = math.sqrt(from_last_to_first)
    E += from_last_to_first
    return E

def generate_route_candidate(cities):
    n = len(cities)
    i = np.random.randint(0,n)
    j = np.random.randint(0,n)

    # Flip direction
    if i < j:
        cities[i:j] = np.flipud(cities[i:j])
    else:
        cities[j:i] = np.flipud(cities[j:i])

    return cities

def get_transition_probability(dE, T):
    p = math.exp(-dE/T)
    return p

def make_transit(probability):
    if np.random.uniform(0,1) < probability:
        return True
    else:
        return False

def simulated_annealing(cities, initial_temperature, end_temperature):
    n = len(cities)
    current_energy = calculate_energy(cities)
    t = initial_temperature

    for i in range(1, 100000):
        print(i)
        candidate = generate_route_candidate(cities)
        candidate_energy = calculate_energy(candidate)

        if candidate_energy < current_energy:
            draw_route(cities, current_energy, i)
            # If candidate's energy is less
            current_energy = candidate_energy
            cities = candidate
        else:
            # Probably change
            p = get_transition_probability(candidate_energy-current_energy, t)
            if make_transit(p):
                draw_route(cities, current_energy, i)
                current_energy = candidate_energy
                cities = candidate

        # Decrease temperature
        t = initial_temperature / (i * 10)

        if t <= end_temperature:
            return cities

simulated_annealing(cities, 10, 0.00001)
