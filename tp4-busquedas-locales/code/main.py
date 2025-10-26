import argparse
from nqueens import pretty_board
from hill_climbing import hill_climbing
from simulated_annealing import simulated_annealing
from genetic import genetic_algorithm
from random_search import random_search

def main():
    parser = argparse.ArgumentParser(
        description="Ejecutor general de algoritmos para el problema de las N-Reinas."
    )
    parser.add_argument("--algo", choices=["HC", "SA", "GA", "RANDOM"], required=True,
                        help="Algoritmo a ejecutar: HC (Hill Climbing), SA (Simulated Annealing), GA (Genético), RANDOM (Búsqueda Aleatoria)")
    parser.add_argument("--n", type=int, default=8, help="Tamaño del tablero (N reinas)")
    parser.add_argument("--seed", type=int, default=None, help="Semilla aleatoria")
    parser.add_argument("--max-states", type=int, default=10000, help="Máximo de estados evaluados")

    args = parser.parse_args()

    if args.algo == "HC":
        result = hill_climbing(args.n, args.max_states, args.seed)
        algo_name = "Hill Climbing"
    elif args.algo == "SA":
        result = simulated_annealing(args.n, args.max_states, args.seed)
        algo_name = "Simulated Annealing"
    elif args.algo == "GA":
        result = genetic_algorithm(args.n, args.max_states, args.seed)
        algo_name = "Algoritmo Genético"
    elif args.algo == "RANDOM":
        result = random_search(args.n, args.max_states, args.seed)
        algo_name = "Búsqueda Aleatoria"
    else:
        raise ValueError("Algoritmo no reconocido")

    print(f"\n===== RESULTADOS {algo_name.upper()} =====")
    print(f"Tamaño del tablero: {args.n}")
    print(f"Semilla: {args.seed}")
    print(f"Mejor solución encontrada: {result['best_solution']}")
    print(f"H (conflictos): {result['H']}")
    print(f"Estados explorados: {result['states']}")
    print(f"Tiempo: {result['time']:.6f} segundos")

    print("\nTablero resultante:\n")
    print(pretty_board(result["best_solution"]))


if __name__ == "__main__":
    main()
