import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
# Asegúrate de tener un archivo CSV con columnas:
# size, dirt_rate, agent, performance
# Ejemplo: resultados_tp2.csv
# ============================================================================
csv_path = "../resultados_tp2.csv"   # cambia si tu archivo tiene otro nombre
output_dir = "../images"
os.makedirs(output_dir, exist_ok=True)

# ============================================================================
# LECTURA DE DATOS
# ============================================================================
df = pd.read_csv(csv_path)

# Convertir tipos por seguridad
df['size'] = df['size'].astype(str)
df['dirt_rate'] = df['dirt_rate'].astype(float)

# ============================================================================
# GENERACIÓN DE BOXPLOTS
# ============================================================================
sns.set(style="whitegrid", palette="muted")

for size in sorted(df['size'].unique(), key=lambda x: int(x)):
    subset = df[df['size'] == size]
    
    plt.figure(figsize=(9,6))
    sns.boxplot(
        x='dirt_rate', 
        y='performance', 
        hue='agent', 
        data=subset,
        width=0.6,
        fliersize=3
    )
    
    plt.title(f"Desempeño de los agentes – Tamaño {size}×{size}", fontsize=13, weight='bold')
    plt.xlabel("Porcentaje de suciedad inicial", fontsize=11)
    plt.ylabel("Celdas limpiadas", fontsize=11)
    plt.legend(title="Agente")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{size}x{size}_boxplot.png"))
    plt.close()

print("✅ Boxplots generados correctamente en la carpeta /images")
