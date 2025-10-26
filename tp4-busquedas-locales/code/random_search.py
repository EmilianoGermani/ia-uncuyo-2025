import time
import random
from nqueens import random_state, conflicts

def random_search(n, max_states=10000, seed=None):
    """
    Búsqueda aleatoria para el problema de N-Reinas.
    Ahora registra tanto la evolución real (H actual)
    como la mejor H histórica encontrada.
    """
    random.seed(seed)
    start_time = time.time()

    # Primer estado aleatorio
    current = random_state(n)
    current_h = conflicts(current)

    # Mejor encontrado hasta ahora
    best = list(current)
    best_h = current_h

    # Historias para graficar
    real_history = [current_h]   # H de cada intento (puede subir o bajar)
    best_history = [best_h]      # Mejor H encontrado hasta ahora

    for i in range(1, max_states):
        candidate = random_state(n)
        h = conflicts(candidate)
        current_h = h  # actualizamos el valor actual
        real_history.append(current_h)

        if h < best_h:
            best, best_h = candidate, h

        best_history.append(best_h)

        if best_h == 0:
            break

    elapsed = time.time() - start_time
    return {
        "best_solution": best,
        "H": best_h,
        "states": i + 1,
        "time": elapsed,
        "history": best_history,       # lo que ya tenías
        "real_history": real_history   # la evolución real
    }
