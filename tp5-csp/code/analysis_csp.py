import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def read_results(csv_path):
    df = pd.read_csv(csv_path)
    return df

def summarize(df):
    summary = df.groupby(["algorithm_name", "size"]).agg(
        success_rate=("success", lambda x: 100 * x.mean()),
        time_mean=("time", "mean"),
        time_std=("time", "std"),
        states_mean=("states", "mean"),
        states_std=("states", "std"),
    ).reset_index()
    return summary

def save_summary_csv(summary, out_csv):
    summary.to_csv(out_csv, index=False)
    print(f"✅ Resumen guardado en: {out_csv}")

def save_boxplots(df, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)

    # Boxplot tiempos
    plt.figure(figsize=(8,5))
    df.boxplot(column="time", by=["algorithm_name", "size"], grid=False)
    plt.title("Distribución de tiempos por algoritmo y tamaño (CSP)")
    plt.suptitle("")
    plt.xlabel("Algoritmo y tamaño")
    plt.ylabel("Tiempo (s)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    out_path = out_dir / "csp_boxplot_time.png"
    plt.savefig(out_path); plt.close()
    print(f"📊 Gráfico guardado: {out_path}")

    # Boxplot estados
    plt.figure(figsize=(8,5))
    df.boxplot(column="states", by=["algorithm_name", "size"], grid=False)
    plt.title("Distribución de estados por algoritmo y tamaño (CSP)")
    plt.suptitle("")
    plt.xlabel("Algoritmo y tamaño")
    plt.ylabel("Estados")
    plt.xticks(rotation=45)
    plt.tight_layout()
    out_path = out_dir / "csp_boxplot_states.png"
    plt.savefig(out_path); plt.close()
    print(f"📊 Gráfico guardado: {out_path}")

def optional_compare_with_tp4(df_csp, base_dir):
    """
    Compara tiempos/estados promedio con TP4 si existe 'tp4-Nreinas.csv' en la raíz.
    Solo produce una tabla csv simple. Los algoritmos no son comparables 1:1,
    pero sirve para discutir orden de magnitud.
    """
    tp4_csv = base_dir / "tp4-Nreinas.csv"
    if not tp4_csv.exists():
        print("ℹ No se encontró tp4-Nreinas.csv: se omite la comparación con TP4.")
        return

    df4 = pd.read_csv(tp4_csv)
    # resumen TP4
    sum4 = df4.groupby(["algorithm_name", "size"]).agg(
        success_rate=("H", lambda x: 100 * (x == 0).mean()),
        time_mean=("time", "mean"),
        time_std=("time", "std"),
        states_mean=("states", "mean"),
        states_std=("states", "std"),
    ).reset_index()

    # resumen CSP
    sum5 = df_csp.groupby(["algorithm_name", "size"]).agg(
        success_rate=("success", lambda x: 100 * x.mean()),
        time_mean=("time", "mean"),
        time_std=("time", "std"),
        states_mean=("states", "mean"),
        states_std=("states", "std"),
    ).reset_index()

    out_csv = base_dir / "tp5-vs-tp4-summary.csv"
    # Guardamos con un prefijo de origen en columnas
    sum4["origin"] = "TP4"
    sum5["origin"] = "TP5-CSP"
    both = pd.concat([sum4, sum5], ignore_index=True)
    both.to_csv(out_csv, index=False)
    print(f"🧮 Comparación TP5 vs TP4 guardada en: {out_csv}")

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[1]
    csv_path = base / "tp5-csp-results.csv"
    out_summary = base / "tp5-csp-summary.csv"
    out_images = base / "images"

    df = read_results(csv_path)
    summary = summarize(df)
    save_summary_csv(summary, out_summary)
    save_boxplots(df, out_images)
    optional_compare_with_tp4(df, base)

    print("\n✅ Análisis CSP completado.")
