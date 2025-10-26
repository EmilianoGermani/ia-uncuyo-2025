import csv
import time
from pathlib import Path
from hill_climbing import hill_climbing
from simulated_annealing import simulated_annealing
from genetic import genetic_algorithm
from random_search import random_search

ALGOS = {
    "HC": hill_climbing,
    "SA": simulated_annealing,
    "GA": genetic_algorithm,
    "RANDOM": random_search
}

def run_experiments(sizes, seeds, max_states, out_csv):
    """
    Ejecuta todos los algoritmos para los tamaños y semillas dados.
    Guarda los resultados en formato CSV.
    """
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "algorithm_name", "env_n", "size",
        "best_solution", "H", "states", "time", "seed"
    ]

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        env_n = 0
        for size in sizes:
            for seed in seeds:
                for algo_name, fn in ALGOS.items():
                    env_n += 1
                    print(f"\n→ Ejecutando {algo_name} | N={size} | seed={seed}")
                    start = time.time()
                    result = fn(size, max_states, seed)
                    elapsed = time.time() - start

                    row = {
                        "algorithm_name": algo_name,
                        "env_n": env_n,
                        "size": size,
                        "best_solution": result["best_solution"],
                        "H": result["H"],
                        "states": result["states"],
                        "time": round(result["time"], 6),
                        "seed": seed
                    }
                    writer.writerow(row)

    print(f"\n✅ Resultados guardados en: {out_csv}")


if __name__ == "__main__":
    # --- CONFIGURACIÓN DE EXPERIMENTOS ---
    sizes = [4, 8, 10]
    seeds = list(range(30))
    max_states = 10000

    # --- SALIDA ---
    base = Path(__file__).resolve().parents[1]
    out_csv = base / "tp4-Nreinas.csv"

    # --- EJECUTAR EXPERIMENTOS ---
    run_experiments(sizes, seeds, max_states, out_csv)
