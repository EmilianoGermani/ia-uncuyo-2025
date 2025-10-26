import random
import time
from nqueens import random_state, conflicts, pretty_board

def random_population(size, n):
    """Genera una población inicial aleatoria."""
    return [random_state(n) for _ in range(size)]

def fitness(state):
    """El fitness es -H(e) porque queremos minimizar los conflictos."""
    return -conflicts(state)

def tournament_selection(population, k=3):
    """Selecciona el mejor de k individuos al azar (torneo)."""
    selected = random.sample(population, k)
    selected.sort(key=lambda s: fitness(s), reverse=True)
    return selected[0]

def crossover(parent1, parent2):
    """Crossover de un punto."""
    n = len(parent1)
    point = random.randint(1, n - 2)
    child = parent1[:point] + parent2[point:]
    return child

def mutate(state, mutation_rate=0.05):
    """Mutación: cambia la fila de una reina con cierta probabilidad."""
    n = len(state)
    new_state = list(state)
    for i in range(n):
        if random.random() < mutation_rate:
            new_state[i] = random.randrange(n)
    return new_state

def genetic_algorithm(n, max_states=10000, seed=None,
                      pop_size=80, mutation_rate=0.05, stagnation_limit=200):
    random.seed(seed)
    start_time = time.time()

    population = random_population(pop_size, n)
    best = min(population, key=conflicts)
    best_h = conflicts(best)

    evaluated = len(population)
    generations_without_improvement = 0
    history = [best_h]
    while evaluated < max_states and best_h > 0 and generations_without_improvement < stagnation_limit:
        new_population = []
        history.append(best_h)
        for _ in range(pop_size):
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population

        current_best = min(population, key=conflicts)
        current_h = conflicts(current_best)

        if current_h < best_h:
            best, best_h = current_best, current_h
            generations_without_improvement = 0
        else:
            generations_without_improvement += 1

        evaluated += pop_size

    elapsed = time.time() - start_time
    return {
        "best_solution": best,
        "H": best_h,
        "states": evaluated,
        "time": elapsed,
        "history": history
    }

