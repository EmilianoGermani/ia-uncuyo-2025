import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def read_results(csv_path):
    """Lee el CSV generado por runner.py"""
    df = pd.read_csv(csv_path)
    return df

def summarize(df):
    """Calcula métricas estadísticas agrupadas por algoritmo y tamaño."""
    summary = df.groupby(["algorithm_name", "size"]).agg(
        success_rate=("H", lambda x: (x == 0).mean() * 100),
        H_mean=("H", "mean"),
        H_std=("H", "std"),
        time_mean=("time", "mean"),
        time_std=("time", "std"),
        states_mean=("states", "mean"),
        states_std=("states", "std"),
    ).reset_index()
    return summary

def save_summary_csv(summary, out_csv):
    """Guarda la tabla resumen en CSV."""
    summary.to_csv(out_csv, index=False)
    print(f"✅ Archivo resumen guardado en: {out_csv}")

def save_boxplots(df, out_dir):
    """Genera boxplots para comparar H, tiempo y estados."""
    out_dir.mkdir(parents=True, exist_ok=True)

    metrics = ["H", "time", "states"]
    for metric in metrics:
        plt.figure(figsize=(8, 5))
        df.boxplot(column=metric, by=["algorithm_name", "size"], grid=False)
        plt.title(f"Distribución de {metric} por algoritmo y tamaño")
        plt.suptitle("")
        plt.xlabel("Algoritmo y tamaño")
        plt.ylabel(metric)
        plt.xticks(rotation=45)
        plt.tight_layout()
        out_path = out_dir / f"boxplot_{metric}.png"
        plt.savefig(out_path)
        plt.close()
        print(f"📊 Gráfico guardado: {out_path}")

def plot_h_evolution(h_values, algo_name, out_dir):
    """Grafica la evolución de H a lo largo de las iteraciones para una ejecución."""
    plt.figure(figsize=(6, 4))
    plt.plot(range(len(h_values)), h_values, marker='o', markersize=2)
    plt.title(f"Evolución de H() - {algo_name}")
    plt.xlabel("Iteraciones")
    plt.ylabel("H()")
    plt.grid(True)
    out_path = out_dir / f"h_evolution_{algo_name}.png"
    plt.savefig(out_path)
    plt.close()
    print(f"📈 Curva H() guardada: {out_path}")


if __name__ == "__main__":
    base = Path(__file__).resolve().parents[1]
    csv_path = base / "tp4-Nreinas.csv"
    out_summary = base / "tp4-summary.csv"
    out_images = base / "images"

    df = read_results(csv_path)
    summary = summarize(df)
    save_summary_csv(summary, out_summary)
    save_boxplots(df, out_images)

    print("\n✅ Análisis completado.")
