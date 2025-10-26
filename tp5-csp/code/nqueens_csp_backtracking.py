import time
import random

def is_consistent(assignment, var, value):
    """
    Verifica si asignar 'value' a 'var' es consistente con las asignaciones previas.
    'assignment' es un diccionario {columna: fila}.
    """
    for other_var, other_value in assignment.items():
        # Restricción de fila
        if other_value == value:
            return False
        # Restricción de diagonales
        if abs(other_value - value) == abs(other_var - var):
            return False
    return True


def backtracking_csp(n, seed=None):
    """
    Resuelve N-Reinas utilizando backtracking con orden de valores por columna
    determinado por 'seed' (para generar variación entre corridas).
    Devuelve la primera solución encontrada y métricas.
    """
    start_time = time.time()
    assignment = {}
    states = 0

    # Precomputamos el orden de valores por columna en base a la seed (determinístico)
    rng = random.Random(seed)
    value_order = {}
    for col in range(n):
        order = list(range(n))
        rng.shuffle(order)
        value_order[col] = order

    def backtrack(col):
        nonlocal states
        if col == n:
            return assignment.copy()

        for row in value_order[col]:
            states += 1
            if is_consistent(assignment, col, row):
                assignment[col] = row
                result = backtrack(col + 1)
                if result is not None:
                    return result
                del assignment[col]
        return None

    solution = backtrack(0)
    elapsed = time.time() - start_time
    return {
        "solution": solution,
        "states": states,
        "time": elapsed,
        "success": solution is not None
    }


if __name__ == "__main__":
    n = 8
    result = backtracking_csp(n, seed=0)
    print(f"Solución: {result['solution']}")
    print(f"Estados: {result['states']}")
    print(f"Tiempo: {result['time']:.6f}s")
