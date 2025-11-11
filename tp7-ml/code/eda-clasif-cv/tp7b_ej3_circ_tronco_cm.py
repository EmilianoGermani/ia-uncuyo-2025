import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# === CARGA DE DATOS ===
path = Path("arbolado-mendoza-dataset-train.csv")
df = pd.read_csv(path)

# Limpieza: convertir circ_tronco_cm a numérico
df["circ_tronco_cm"] = pd.to_numeric(df["circ_tronco_cm"], errors="coerce")

# -------------------------------------------------------------------------
# === 3A: HISTOGRAMA GENERAL ===
# -------------------------------------------------------------------------
plt.figure(figsize=(10,5))
plt.hist(df["circ_tronco_cm"], bins=30, color="forestgreen", edgecolor="black")
plt.title("Histograma de circ_tronco_cm (30 bins)")
plt.xlabel("Circunferencia del tronco [cm]")
plt.ylabel("Frecuencia")
plt.grid(axis="y", alpha=0.5)
plt.tight_layout()
plt.savefig("histograma_circ_tronco_cm_30bins.png")

# También probamos con distintos bins para comparar
for bins in [10, 50]:
    plt.figure(figsize=(10,5))
    plt.hist(df["circ_tronco_cm"], bins=bins, color="seagreen", edgecolor="black")
    plt.title(f"Histograma de circ_tronco_cm ({bins} bins)")
    plt.xlabel("Circunferencia del tronco [cm]")
    plt.ylabel("Frecuencia")
    plt.grid(axis="y", alpha=0.5)
    plt.tight_layout()
    plt.savefig(f"histograma_circ_tronco_cm_{bins}bins.png")

# -------------------------------------------------------------------------
# === 3B: HISTOGRAMA SEPARADO POR CLASE (inclinacion_peligrosa) ===
# -------------------------------------------------------------------------
df["inclinacion_peligrosa"] = pd.to_numeric(df["inclinacion_peligrosa"], errors="coerce").fillna(0).astype(int)

plt.figure(figsize=(10,5))
plt.hist(df[df["inclinacion_peligrosa"] == 0]["circ_tronco_cm"],
         bins=30, alpha=0.6, label="No peligrosa (0)",
         color="mediumseagreen", edgecolor="black")
plt.hist(df[df["inclinacion_peligrosa"] == 1]["circ_tronco_cm"],
         bins=30, alpha=0.6, label="Peligrosa (1)",
         color="darkred", edgecolor="black")
plt.title("Distribución de circ_tronco_cm separada por inclinacion_peligrosa")
plt.xlabel("Circunferencia del tronco [cm]")
plt.ylabel("Frecuencia")
plt.legend()
plt.grid(axis="y", alpha=0.5)
plt.tight_layout()
plt.savefig("histograma_circ_tronco_cm_por_clase.png")

# -------------------------------------------------------------------------
# === 3C: CREACIÓN DE VARIABLE CATEGÓRICA circ_tronco_cm_cat ===
# -------------------------------------------------------------------------
# Usamos percentiles 25%, 50%, 75% para definir los cortes
cut_points = df["circ_tronco_cm"].quantile([0.25, 0.5, 0.75]).values
print("Puntos de corte:", cut_points)

labels = ["bajo", "medio", "alto", "muy alto"]

df["circ_tronco_cm_cat"] = pd.cut(
    df["circ_tronco_cm"],
    bins=[0, cut_points[0], cut_points[1], cut_points[2], df["circ_tronco_cm"].max()],
    labels=labels,
    include_lowest=True
)

# Guardamos el nuevo dataset
df.to_csv("arbolado-mendoza-dataset-circ_tronco_cm-train.csv", index=False)

# -------------------------------------------------------------------------
# === COMPROBACIÓN FINAL ===
# -------------------------------------------------------------------------
print("\nDistribución de circ_tronco_cm_cat:")
print(df["circ_tronco_cm_cat"].value_counts())
