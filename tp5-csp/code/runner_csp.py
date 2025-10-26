import csv
import time
from pathlib import Path
from nqueens_csp_backtracking import backtracking_csp
from nqueens_csp_fc import nqueens_forward_checking

ALGOS = {
    "BT": backtracking_csp,
    "FC": nqueens_forward_checking,
}

def run_experiments(sizes, seeds, out_csv):
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "algorithm_name", "env_n", "size",
        "success", "states", "time", "seed",
        "solution"
    ]

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        env_n = 0
        for size in sizes:
            for seed in seeds:
                for algo_name, fn in ALGOS.items():
                    env_n += 1
                    start = time.time()
                    result = fn(size, seed=seed)
                    # (result["time"] ya viene del algoritmo; no usamos 'elapsed' de acá)
                    row = {
                        "algorithm_name": algo_name,
                        "env_n": env_n,
                        "size": size,
                        "success": int(result["success"]),
                        "states": result["states"],
                        "time": round(result["time"], 6),
                        "seed": seed,
                        "solution": result["solution"] if result["success"] else ""
                    }
                    writer.writerow(row)
                    print(f"✔ {algo_name} | N={size} | seed={seed} | success={row['success']} | states={row['states']} | time={row['time']}")

    print(f"\n✅ Resultados guardados en: {out_csv}")


if __name__ == "__main__":
    sizes = [4, 8, 10]
    seeds = list(range(30))
    base = Path(__file__).resolve().parents[1]
    out_csv = base / "tp5-csp-results.csv"
    run_experiments(sizes, seeds, out_csv)
