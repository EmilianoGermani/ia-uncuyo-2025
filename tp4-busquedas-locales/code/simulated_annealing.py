import time
import math
import random
from nqueens import random_state, conflicts

def random_neighbor(state):
    n = len(state)
    neighbor = list(state)
    col = random.randrange(n)
    new_row = random.randrange(n)
    while new_row == state[col]:
        new_row = random.randrange(n)
    neighbor[col] = new_row
    return neighbor

def simulated_annealing(n, max_states=10000, seed=None,
                        T0=1.5, alpha=0.995, Tmin=1e-4):
    random.seed(seed)
    start_time = time.time()

    current = random_state(n)
    current_h = conflicts(current)
    best = list(current)
    best_h = current_h

    T = T0
    evaluated = 1
    history = [current_h]

    while evaluated < max_states and T > Tmin and current_h > 0:
        neighbor = random_neighbor(current)
        h = conflicts(neighbor)
        evaluated += 1

        delta = h - current_h
        if delta < 0 or random.random() < math.exp(-delta / T):
            current = neighbor
            current_h = h
            if current_h < best_h:
                best, best_h = list(current), current_h

        T *= alpha
        history.append(current_h)

    elapsed = time.time() - start_time
    return {
        "best_solution": best,
        "H": best_h,
        "states": evaluated,
        "time": elapsed,
        "history": history
    }
