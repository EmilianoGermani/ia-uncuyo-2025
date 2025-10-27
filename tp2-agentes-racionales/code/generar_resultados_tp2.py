import csv
import time
import os

# Importamos los agentes directamente del mismo directorio
from student_emiliano_germani_ReflexiveAgent import ReflexiveAgent
from student_emiliano_germani_RandomAgent import RandomAgent

# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================
SERVER_URL = "http://localhost:5000"   # Servidor del entorno
DIR_OUTPUT = "../"                     # Guarda los CSV en la raíz del proyecto
REPEAT = 10                            # Cantidad de corridas por combinación

TAMANOS = [2, 4, 8, 16, 32, 64, 128]
DIRT_RATES = [0.1, 0.2, 0.4, 0.8]


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================
def ejecutar_agente(AgenteClase, nombre_agente, archivo_csv):
    """
    Ejecuta las simulaciones del agente dado y guarda los resultados en un CSV.
    """
    ruta_csv = os.path.join(DIR_OUTPUT, archivo_csv)
    os.makedirs(os.path.dirname(ruta_csv), exist_ok=True)

    with open(ruta_csv, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["size", "dirt_rate", "agent", "performance"])

        for size in TAMANOS:
            for dirt in DIRT_RATES:
                for run in range(REPEAT):
                    print(f"[{nombre_agente}] Ejecutando {size}x{size}, dirt_rate={dirt}, intento {run+1}/10")
                    agent = AgenteClase(server_url=SERVER_URL)

                    try:
                        if not agent.connect_to_environment(size, size, dirt):
                            print("❌ Error al conectar con el entorno.")
                            continue

                        performance = agent.run_simulation(verbose=False)
                        writer.writerow([size, dirt, nombre_agente, performance])

                    except Exception as e:
                        print(f"⚠️ Error durante la simulación: {e}")
                        continue

                    finally:
                        agent.disconnect()
                        time.sleep(0.3)  # pequeña pausa entre simulaciones

    print(f"✅ Resultados guardados en {ruta_csv}")
    return ruta_csv


def combinar_csv(reflex_csv, random_csv, salida="resultados_tp2.csv"):
    """
    Combina ambos CSV (Reflexive y Random) en uno solo.
    """
    import pandas as pd

    df1 = pd.read_csv(reflex_csv)
    df2 = pd.read_csv(random_csv)
    df_final = pd.concat([df1, df2])
    ruta_salida = os.path.join(DIR_OUTPUT, salida)
    df_final.to_csv(ruta_salida, index=False)
    print(f"📊 Archivo combinado guardado en {ruta_salida}")


# ============================================================
# EJECUCIÓN PRINCIPAL
# ============================================================
if __name__ == "__main__":
    print("🚀 INICIANDO SIMULACIONES DE TP2 – AGENTES RACIONALES\n")

    reflexive_csv = ejecutar_agente(ReflexiveAgent, "Reflexive", "resultados_reflexive.csv")
    random_csv = ejecutar_agente(RandomAgent, "Random", "resultados_random.csv")

    combinar_csv(reflexive_csv, random_csv)

    print("\n🎉 Todo listo. Ahora podés usar 'graficar_resultados.py' para generar los boxplots.")
