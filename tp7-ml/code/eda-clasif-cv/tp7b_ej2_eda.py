import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --- 0) Carga ---
path_csv = Path("arbolado-mendoza-dataset-train.csv")
path_txt = Path("arbolado-mendoza-dataset-train.txt")
path = path_csv if path_csv.exists() else path_txt
df = pd.read_csv(path)

# Asegurar tipo binario 0/1
df["inclinacion_peligrosa"] = pd.to_numeric(df["inclinacion_peligrosa"], errors="coerce").fillna(0).astype(int)

# === 2a) Distribución de la clase ===
cls_counts = df["inclinacion_peligrosa"].value_counts().sort_index()
cls_perc = (cls_counts / len(df) * 100).round(2)

plt.figure(figsize=(6, 4))
plt.bar(cls_counts.index.astype(str), cls_counts.values)
plt.title("Distribución de la clase 'inclinacion_peligrosa'")
plt.xlabel("inclinacion_peligrosa")
plt.ylabel("Cantidad de registros")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("distribucion_inclinacion_peligrosa.png")

pd.DataFrame({
    "clase": cls_counts.index.astype(int),
    "conteo": cls_counts.values,
    "porcentaje": cls_perc.values
}).to_csv("tabla_2a_distribucion_clase.csv", index=False)

# === 2b) Peligrosidad por sección ===
sec_stats = (
    df.groupby("nombre_seccion")["inclinacion_peligrosa"]
      .agg(n="size", tasa_peligrosa="mean")
      .sort_values("tasa_peligrosa", ascending=False)
)

plt.figure(figsize=(10, 5))
plt.bar(sec_stats.index.astype(str), sec_stats["tasa_peligrosa"].values)
plt.title("Proporción de inclinación peligrosa por sección")
plt.xlabel("Sección")
plt.ylabel("Proporción peligrosa")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("peligrosidad_por_seccion.png")

sec_stats.assign(tasa_peligrosa=sec_stats["tasa_peligrosa"].round(4)).to_csv(
    "peligrosidad_por_seccion.csv"
)

# === 2c) Peligrosidad por especie (con soporte mínimo) ===
esp_stats = (
    df.groupby("especie")["inclinacion_peligrosa"]
      .agg(n="size", tasa_peligrosa="mean")
      .sort_values("tasa_peligrosa", ascending=False)
)
min_soporte = 50
esp_top = esp_stats[esp_stats["n"] >= min_soporte].head(15)

plt.figure(figsize=(12, 6))
plt.bar(esp_top.index.astype(str), esp_top["tasa_peligrosa"].values)
plt.title(f"Top 15 especies por proporción peligrosa (n ≥ {min_soporte})")
plt.xlabel("Especie")
plt.ylabel("Proporción peligrosa")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("peligrosidad_por_especie_top15.png")

esp_stats.assign(tasa_peligrosa=esp_stats["tasa_peligrosa"].round(4)).to_csv(
    "peligrosidad_por_especie.csv"
)
esp_top.assign(tasa_peligrosa=esp_top["tasa_peligrosa"].round(4)).to_csv(
    "peligrosidad_por_especie_top15.csv"
)

# --- Mensaje final por consola ---
print("\n== 2a) Distribución de la clase ==")
print(pd.DataFrame({"conteo": cls_counts, "porcentaje": cls_perc}))
print("\n== 2b) Secciones más peligrosas (Top 5) ==")
print(sec_stats.head(5))
print("\n== 2c) Especies más peligrosas (Top 15, con soporte mínimo) ==")
print(esp_top)
