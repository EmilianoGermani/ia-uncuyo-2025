import time
import random
from copy import deepcopy


def is_consistent(assignment, var, value):
    for other_var, other_value in assignment.items():
        if other_value == value:
            return False
        if abs(other_value - value) == abs(other_var - var):
            return False
    return True


def forward_checking(domains, var, value, n):
    """
    Aplica forward checking tras asignar 'value' a 'var'.
    Elimina valores inconsistentes de los dominios de variables futuras.
    """
    new_domains = deepcopy(domains)
    for future_var in range(var + 1, n):
        # quitar misma fila
        if value in new_domains[future_var]:
            new_domains[future_var].remove(value)
        # quitar diagonales
        delta = future_var - var
        diag1 = value + delta
        diag2 = value - delta
        if diag1 in new_domains[future_var]:
            new_domains[future_var].remove(diag1)
        if diag2 in new_domains[future_var]:
            new_domains[future_var].remove(diag2)

        # Si algún dominio queda vacío, inconsistente
        if not new_domains[future_var]:
            return None
    return new_domains


def nqueens_forward_checking(n, seed=None):
    start_time = time.time()
    states = 0
    assignment = {}

    # Orden base por columna (determinístico en función de la seed)
    rng = random.Random(seed)
    base_order = {}
    for col in range(n):
        order = list(range(n))
        rng.shuffle(order)
        base_order[col] = order

    # Dominios iniciales
    domains = {i: list(range(n)) for i in range(n)}

    def backtrack(col, domains):
        nonlocal states
        if col == n:
            return assignment.copy()

        # Ordenar valores de esta columna según base_order, filtrando por dominio actual
        values = [v for v in base_order[col] if v in domains[col]]

        for value in values:
            states += 1
            if is_consistent(assignment, col, value):
                assignment[col] = value
                new_domains = forward_checking(domains, col, value, n)
                if new_domains is not None:
                    result = backtrack(col + 1, new_domains)
                    if result is not None:
                        return result
                del assignment[col]
        return None

    solution = backtrack(0, domains)
    elapsed = time.time() - start_time
    return {
        "solution": solution,
        "states": states,
        "time": elapsed,
        "success": solution is not None
    }


if __name__ == "__main__":
    n = 8
    result = nqueens_forward_checking(n, seed=0)
    print(f"Solución: {result['solution']}")
    print(f"Estados: {result['states']}")
    print(f"Tiempo: {result['time']:.6f}s")
