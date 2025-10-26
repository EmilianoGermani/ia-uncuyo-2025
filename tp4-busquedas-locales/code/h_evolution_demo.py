from hill_climbing import hill_climbing
from simulated_annealing import simulated_annealing
from genetic import genetic_algorithm
from random_search import random_search
from analysis import plot_h_evolution
import matplotlib.pyplot as plt
from pathlib import Path

out_dir = Path("../images")
out_dir.mkdir(exist_ok=True)

N = 8
SEED = 42
MAX_STATES = 10000

# Elegí el algoritmo que quieras analizar
result = hill_climbing(N, MAX_STATES, SEED)
plot_h_evolution(result["history"], "HillClimbing", out_dir)

result = simulated_annealing(N, MAX_STATES, SEED)
plot_h_evolution(result["history"], "SimulatedAnnealing", out_dir)

result = genetic_algorithm(N, MAX_STATES, SEED)
plot_h_evolution(result["history"], "GeneticAlgorithm", out_dir)

# Ejecutar búsqueda aleatoria
result = random_search(N, MAX_STATES, SEED)

# Curva 1: H real (subidas y bajadas)
plt.figure(figsize=(6, 4))
plt.plot(range(len(result["real_history"])), result["real_history"], color="gray", alpha=0.6, label="H actual (aleatorio)")
plt.plot(range(len(result["history"])), result["history"], color="blue", label="Mejor H encontrado")
plt.title("Evolución de H() - RandomSearch")
plt.xlabel("Iteraciones")
plt.ylabel("H()")
plt.grid(True)
plt.legend()
out_path = out_dir / "h_evolution_RandomSearch_completo.png"
plt.savefig(out_path)
plt.close()
print(f"📈 Curva completa de RandomSearch guardada: {out_path}")

print("\n✅ Gráficos de evolución H() generados en la carpeta /images")
