import gymnasium as gym
from gymnasium import wrappers
import numpy as np
import random
import heapq
import time
import csv
import argparse
import os
import matplotlib.pyplot as plt

# -------------------------------------------------------------
# 1. Generar mapa personalizado
# -------------------------------------------------------------
def generate_random_map_custom(size=10, p=0.92, seed=None):
    if seed is not None:
        np.random.seed(seed)
    mapa = np.random.choice(['F', 'H'], size=(size, size), p=[p, 1-p])
    start = (np.random.randint(0, size), np.random.randint(0, size))
    goal = (np.random.randint(0, size), np.random.randint(0, size))
    mapa[start] = 'S'
    mapa[goal] = 'G'
    return ["".join(row) for row in mapa]

# -------------------------------------------------------------
# 2. Funciones auxiliares
# -------------------------------------------------------------
def vecinos(pos, mapa):
    size = len(mapa)
    r, c = pos
    posibles = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
    return [(nr, nc) for nr, nc in posibles if 0 <= nr < size and 0 <= nc < size and mapa[nr][nc] != 'H']

def heuristica(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

# -------------------------------------------------------------
# 3. Algoritmos de búsqueda
# -------------------------------------------------------------
def busqueda_aleatoria(mapa, inicio, objetivo, max_intentos=1000):
    pos = inicio
    camino = [inicio]
    for _ in range(max_intentos):
        if pos == objetivo:
            return camino, len(camino)
        movs = vecinos(pos, mapa)
        if not movs:
            return None, None
        pos = random.choice(movs)
        camino.append(pos)
    return None, None

def busqueda_anchura(mapa, inicio, objetivo):
    cola = [(inicio, [inicio])]
    visitados = set([inicio])
    expandidos = 0
    while cola:
        estado, camino = cola.pop(0)
        expandidos += 1
        if estado == objetivo:
            return camino, expandidos
        for v in vecinos(estado, mapa):
            if v not in visitados:
                visitados.add(v)
                cola.append((v, camino+[v]))
    return None, expandidos

def busqueda_profundidad(mapa, inicio, objetivo):
    pila = [(inicio, [inicio])]
    visitados = set()
    expandidos = 0
    while pila:
        estado, camino = pila.pop()
        expandidos += 1
        if estado == objetivo:
            return camino, expandidos
        if estado not in visitados:
            visitados.add(estado)
            for v in vecinos(estado, mapa):
                if v not in visitados:
                    pila.append((v, camino+[v]))
    return None, expandidos

def busqueda_profundidad_limitada(mapa, inicio, objetivo, limite):
    pila = [(inicio, [inicio], 0)]
    visitados = set()
    expandidos = 0
    while pila:
        estado, camino, prof = pila.pop()
        expandidos += 1
        if estado == objetivo:
            return camino, expandidos
        if prof < limite and estado not in visitados:
            visitados.add(estado)
            for v in vecinos(estado, mapa):
                pila.append((v, camino+[v], prof+1))
    return None, expandidos

def busqueda_costo_uniforme(mapa, inicio, objetivo, costos):
    frontera = [(0, inicio, [inicio])]
    visitados = {}
    expandidos = 0
    while frontera:
        costo, estado, camino = heapq.heappop(frontera)
        if estado == objetivo:
            return camino, costo, expandidos
        if estado in visitados and visitados[estado] <= costo:
            continue
        visitados[estado] = costo
        expandidos += 1
        for v in vecinos(estado, mapa):
            dr, dc = v[0]-estado[0], v[1]-estado[1]
            paso = costos.get((dr, dc), 1)
            heapq.heappush(frontera, (costo+paso, v, camino+[v]))
    return None, None, expandidos

def busqueda_a_estrella(mapa, inicio, objetivo, costos):
    frontera = [(heuristica(inicio, objetivo), 0, inicio, [inicio])]
    visitados = {}
    expandidos = 0
    while frontera:
        f, g, estado, camino = heapq.heappop(frontera)
        if estado == objetivo:
            return camino, g, expandidos
        if estado in visitados and visitados[estado] <= g:
            continue
        visitados[estado] = g
        expandidos += 1
        for v in vecinos(estado, mapa):
            dr, dc = v[0]-estado[0], v[1]-estado[1]
            paso = costos.get((dr, dc), 1)
            g2 = g + paso
            f2 = g2 + heuristica(v, objetivo)
            heapq.heappush(frontera, (f2, g2, v, camino+[v]))
    return None, None, expandidos

# -------------------------------------------------------------
# 4. Función para calcular costo total de un camino
# -------------------------------------------------------------
def calcular_costo(camino, costos):
    if camino is None:
        return None
    total = 0
    for i in range(1, len(camino)):
        dr = camino[i][0]-camino[i-1][0]
        dc = camino[i][1]-camino[i-1][1]
        total += costos.get((dr, dc), 1)
    return total

# -------------------------------------------------------------
# 5. Mostrar resultados por consola
# -------------------------------------------------------------
def mostrar_resultado(nombre, camino, costo, expandidos, t):
    if camino is None:
        print(f"{nombre}: sin camino")
    else:
        pasos = len(camino)-1
        print(f"{nombre}: {pasos} pasos, costo {costo}, expandidos {expandidos}, tiempo {t:.4f}s")

# -------------------------------------------------------------
# 6. Ejecución de una demo
# -------------------------------------------------------------
def demo_unica():
    mapa = generate_random_map_custom(size=100, p=0.92, seed=888)
    env = gym.make("FrozenLake-v1", desc=mapa, is_slippery=False)
    env = wrappers.TimeLimit(env, max_episode_steps=1000)
    size = len(mapa)
    start, goal = None, None
    for r in range(size):
        for c in range(size):
            if mapa[r][c] == 'S': start = (r, c)
            if mapa[r][c] == 'G': goal = (r, c)

    print("\n=== DEMO: entorno reproducible (seed=888) ===")
    print(f"Inicio: {start}  Objetivo: {goal}")
    print(f"Número de estados: {size*size}\n")
    print("=== ENTORNO GENERADO ===")
    for fila in mapa:
        print(fila)

    costos1 = {(1,0):1,(-1,0):1,(0,1):1,(0,-1):1}
    costos2 = {(1,0):10,(-1,0):10,(0,1):1,(0,-1):1}

    print("\n--- ESCENARIO 1 (costo=1 por acción) ---")
    inicio_t = time.time()
    camino, _ = busqueda_aleatoria(mapa, start, goal)
    mostrar_resultado("Aleatoria", camino, calcular_costo(camino, costos1), 0, time.time()-inicio_t)

    for nombre, funcion in [("BFS", busqueda_anchura), ("DFS", busqueda_profundidad)]:
        t0 = time.time()
        camino, exp = funcion(mapa, start, goal)
        c = calcular_costo(camino, costos1)
        mostrar_resultado(nombre, camino, c, exp, time.time()-t0)
        if camino and nombre == "BFS":
            print("Camino:", camino)

    for limite in [50,75,100]:
        t0 = time.time()
        camino, exp = busqueda_profundidad_limitada(mapa, start, goal, limite)
        c = calcular_costo(camino, costos1)
        mostrar_resultado(f"DLS({limite})", camino, c, exp, time.time()-t0)

    for nombre, funcion in [("UCS", busqueda_costo_uniforme), ("A*", busqueda_a_estrella)]:
        t0 = time.time()
        camino, c, exp = funcion(mapa, start, goal, costos1)
        mostrar_resultado(nombre, camino, c, exp, time.time()-t0)

    print("\n--- ESCENARIO 2 (izq/der=1, arriba/abajo=10) ---")
    for nombre, funcion in [("BFS", busqueda_anchura), ("DFS", busqueda_profundidad)]:
        t0 = time.time()
        camino, exp = funcion(mapa, start, goal)
        c = calcular_costo(camino, costos2)
        mostrar_resultado(nombre, camino, c, exp, time.time()-t0)

    for limite in [50,75,100]:
        t0 = time.time()
        camino, exp = busqueda_profundidad_limitada(mapa, start, goal, limite)
        c = calcular_costo(camino, costos2)
        mostrar_resultado(f"DLS({limite})", camino, c, exp, time.time()-t0)

    for nombre, funcion in [("UCS", busqueda_costo_uniforme), ("A*", busqueda_a_estrella)]:
        t0 = time.time()
        camino, c, exp = funcion(mapa, start, goal, costos2)
        mostrar_resultado(nombre, camino, c, exp, time.time()-t0)

# -------------------------------------------------------------
# 7. Ejecuciones múltiples (30 veces) y guardado CSV
# -------------------------------------------------------------
def ejecutar_varias_veces(n=30, size=50):
    resultados = []
    costos1 = {(1,0):1,(-1,0):1,(0,1):1,(0,-1):1}
    costos2 = {(1,0):10,(-1,0):10,(0,1):1,(0,-1):1}

    for i in range(n):
        mapa = generate_random_map_custom(size=size, p=0.92, seed=i+42)
        start, goal = None, None
        for r in range(size):
            for c in range(size):
                if mapa[r][c] == 'S': start = (r, c)
                if mapa[r][c] == 'G': goal = (r, c)

        for esc, costos in [(1, costos1), (2, costos2)]:
            for nombre, funcion in [
                ("Aleatoria", lambda m,s,g: busqueda_aleatoria(m,s,g)),
                ("BFS", busqueda_anchura),
                ("DFS", busqueda_profundidad),
                ("DLS50", lambda m,s,g: busqueda_profundidad_limitada(m,s,g,50)),
                ("UCS", lambda m,s,g: busqueda_costo_uniforme(m,s,g,costos)),
                ("A*", lambda m,s,g: busqueda_a_estrella(m,s,g,costos))
            ]:
                t0 = time.time()

                # Ejecutar el algoritmo correspondiente
                if nombre.startswith("UCS") or nombre.startswith("A*"):
                    camino, costo, exp = funcion(mapa, start, goal)
                elif nombre == "Aleatoria":
                    camino, _ = funcion(mapa, start, goal)
                    exp = 0
                    costo = calcular_costo(camino, costos)
                else:
                    camino, exp = funcion(mapa, start, goal)
                    costo = calcular_costo(camino, costos)

                # Verificar límite de vida (1000 pasos)
                if camino and len(camino) > 1000:
                    camino = None
                    costo = None

                t = time.time() - t0
                pasos = len(camino)-1 if camino else None

                # Calcular ambos tipos de costo (esc1 y esc2)
                costo_esc1 = calcular_costo(camino, costos1) if camino else None
                costo_esc2 = calcular_costo(camino, costos2) if camino else None

                resultados.append([
                    i+1, esc, nombre, exp,
                    pasos, costo_esc1, costo_esc2,
                    round(t,4), camino is not None
                ])

    # Guardar CSV con ambas columnas completas
    with open('results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'algorithm_name',
            'env_n',
            'states_n',
            'actions_count',
            'actions_cost',
            'time',
            'solution_found'
        ])
        for fila in resultados:
            # fila = [Mapa, Escenario, Algoritmo, Expandidos, Pasos, CostoEsc1, CostoEsc2, Tiempo, Exito]
            writer.writerow([
                fila[2],     # algorithm_name
                fila[0],     # env_n
                fila[3],     # states_n
                fila[5],     # actions_count (siempre completado)
                fila[6],     # actions_cost (siempre completado)
                fila[7],     # time
                fila[8]      # solution_found
            ])

    print("\n✔ Resultados guardados en results.csv (ambas columnas completadas)")

# -------------------------------------------------------------
# 8. Generar boxplots desde CSV
# -------------------------------------------------------------
def generar_boxplots():
    import pandas as pd
    datos = pd.read_csv('results.csv')

    if not os.path.exists('images'):
        os.makedirs('images')

    # ⚠️ Filtramos solo las columnas numéricas que tengan valores válidos
    metricas = ['states_n', 'actions_count', 'actions_cost', 'time']

    for metrica in metricas:
        # Quitamos filas NaN (ya que algunas métricas pueden ser None según el escenario)
        subset = datos.dropna(subset=[metrica])
        plt.figure(figsize=(8,5))
        subset.boxplot(column=metrica, by='algorithm_name')
        plt.title(f"Distribución de {metrica}")
        plt.suptitle('')
        plt.ylabel(metrica)
        plt.xlabel("algorithm_name")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"images/{metrica}_boxplot.png")

    print("✔ Boxplots generados en carpeta images/")

# -------------------------------------------------------------
# 9. Ejecución principal
# -------------------------------------------------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--skip-exp', action='store_true')
    parser.add_argument('--no-demo', action='store_true')
    parser.add_argument('--analyze', action='store_true')
    args = parser.parse_args()

    if not args.no_demo and not args.analyze:
        demo_unica()
    if not args.skip_exp and not args.analyze:
        ejecutar_varias_veces()
        generar_boxplots()
    if args.analyze:
        generar_boxplots()
