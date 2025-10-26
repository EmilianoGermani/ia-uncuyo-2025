import time
import random
from nqueens import random_state, conflicts

def best_neighbor(state):
    n = len(state)
    best = list(state)
    best_h = conflicts(state)
    for col in range(n):
        original_row = state[col]
        for row in range(n):
            if row == original_row:
                continue
            neighbor = list(state)
            neighbor[col] = row
            h = conflicts(neighbor)
            if h < best_h:
                best, best_h = neighbor, h
    return best, best_h

def hill_climbing(n, max_states=10000, seed=None):
    random.seed(seed)
    start_time = time.time()

    current = random_state(n)
    current_h = conflicts(current)
    evaluated = 1
    history = [current_h]

    while evaluated < max_states and current_h > 0:
        neighbor, h = best_neighbor(current)
        evaluated += 1
        if h < current_h:
            current, current_h = neighbor, h
        else:
            break
        history.append(current_h)

    elapsed = time.time() - start_time
    return {
        "best_solution": current,
        "H": current_h,
        "states": evaluated,
        "time": elapsed,
        "history": history
    }
