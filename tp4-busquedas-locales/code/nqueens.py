import random

# Estado = lista de tamaño N, donde cada posición representa la columna
# y el valor representa la fila en la que está la reina.

def random_state(n: int):
    """Genera un estado aleatorio: una reina en alguna fila por columna."""
    return [random.randrange(n) for _ in range(n)]

def conflicts(state):
    """Calcula H(e): número de pares de reinas que se atacan."""
    n = len(state)
    h = 0
    for i in range(n):
        for j in range(i + 1, n):
            same_row = state[i] == state[j]
            same_diag = abs(state[i] - state[j]) == abs(i - j)
            if same_row or same_diag:
                h += 1
    return h

def is_goal(state):
    """True si no hay conflictos."""
    return conflicts(state) == 0

def pretty_board(state):
    """Devuelve un tablero en texto."""
    n = len(state)
    lines = []
    for r in range(n):
        row = ['Q' if state[c] == r else '.' for c in range(n)]
        lines.append(' '.join(row))
    return '\n'.join(lines)
