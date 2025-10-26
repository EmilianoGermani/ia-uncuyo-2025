Trabajo Práctico N°3 — Búsquedas Informadas y No Informadas

## 1. Introducción

En este trabajo práctico se implementaron y compararon distintos **algoritmos de búsqueda informada y no informada** aplicados al entorno **FrozenLake** del paquete *Gymnasium*.  
El objetivo fue analizar la eficiencia de cada método para encontrar una solución óptima (llegar al objetivo desde la posición inicial sin caer en los agujeros) y evaluar su desempeño en términos de **cantidad de estados explorados, número de acciones, costo total y tiempo de ejecución**.

Los algoritmos implementados fueron:

* **Búsqueda Aleatoria (Random Search)**
* **Búsqueda en Anchura (BFS)**
* **Búsqueda en Profundidad (DFS)**
* **Búsqueda en Profundidad Limitada (DLS50)**
* **Búsqueda de Costo Uniforme (UCS)**
* **Búsqueda A\*** (A estrella)

El entorno consiste en un mapa cuadrado de tamaño 50×50, generado aleatoriamente con celdas seguras (‘F’), agujeros (‘H’), un inicio (‘S’) y una meta (‘G’).  
El agente posee un **límite de vida de 1000 pasos**: si supera ese valor sin alcanzar la meta, se considera que falló la búsqueda.

## 2. Metodología experimental

Se evaluaron los seis algoritmos en **30 mapas distintos** (semillas 42 a 71) bajo **dos escenarios de costos**:

1. **Escenario 1:** todas las acciones tienen costo 1.  
2. **Escenario 2:** moverse **arriba o abajo cuesta 10**, y moverse **izquierda o derecha cuesta 1**.

Para cada combinación de mapa, escenario y algoritmo, se registraron las siguientes métricas:

* `states_n`: cantidad de estados expandidos.  
* `actions_count`: cantidad total de acciones realizadas.  
* `actions_cost`: costo total acumulado.  
* `time`: tiempo total de ejecución (en segundos).  
* `solution_found`: valor booleano que indica si se alcanzó la meta.

Los resultados fueron almacenados en el archivo **`results.csv`**, y los análisis estadísticos y visualizaciones se realizaron con *Pandas* y *Matplotlib* generando gráficos tipo **boxplot**.

## 3. Resultados y análisis

### 3.1 Distribución de estados explorados (`states_n`)

![Distribución de estados explorados](images/states_n_boxplot.png)

* **DFS** y **DLS50** presentan una alta dispersión en la cantidad de estados expandidos, producto de su naturaleza de exploración exhaustiva y lineal.  
* **BFS** muestra una expansión controlada, aunque mayor que A\* y UCS.  
* **A\*** y **UCS** son los algoritmos más eficientes, con menor número de expansiones.  
* **Aleatoria** prácticamente no expande estados, ya que depende del azar.

**Conclusión:** los algoritmos informados (A\* y UCS) exploran menos estados y son más eficientes que los métodos no informados.

### 3.2 Distribución de cantidad de acciones (`actions_count`)

![Distribución de cantidad de acciones](images/actions_count_boxplot.png)

* **DFS** y **Aleatoria** realizan un gran número de pasos, evidenciando caminos más largos y erráticos.  
* **BFS**, **UCS** y **A\*** producen caminos más cortos y consistentes.  
* **DLS50** tiene valores intermedios, aunque puede fallar si la meta se encuentra más allá de su límite de profundidad.

**Conclusión:** A\* y UCS logran las rutas más cortas, mientras que DFS tiende a extender los caminos innecesariamente.

### 3.3 Distribución de costo total (`actions_cost`)

![Distribución de costo total](images/actions_cost_boxplot.png)

* En el **escenario 2**, los costos penalizan fuertemente los movimientos verticales.  
* **DFS** y **Aleatoria** presentan los mayores costos, al no priorizar movimientos económicos.  
* **A\*** y **UCS** logran los menores costos, reflejando trayectorias más eficientes.  
* **BFS** mantiene costos moderados, mientras que **DLS50** puede variar según el éxito de la búsqueda.

**Conclusión:** los algoritmos informados adaptan su comportamiento al entorno, minimizando los costos globales.

### 3.4 Distribución del tiempo de ejecución (`time`)

![Distribución del tiempo de ejecución](images/time_boxplot.png)

* **DFS** presenta el mayor tiempo promedio debido a su exploración profunda.  
* **A\*** y **UCS** consumen algo más de tiempo que BFS, pero obtienen soluciones óptimas.  
* **Aleatoria** y **DLS50** son más rápidas, aunque su efectividad es baja.

**Conclusión:** los algoritmos informados son los más equilibrados entre tiempo y calidad de solución.

## 4. Comparación general

| Algoritmo | Eficiencia | Optimalidad | Tiempo | Observaciones |
|------------|-------------|-------------|---------|----------------|
| **Aleatoria** | Muy baja | ❌ | Bajo | Sin dirección heurística, éxito aleatorio |
| **BFS** | Alta | ✅ | Medio | Encuentra caminos óptimos, alto consumo de memoria |
| **DFS** | Baja | ❌ | Alto | Explora profundamente, suele desviarse |
| **DLS50** | Media | ❌ | Bajo | Puede fallar por límite de profundidad |
| **UCS** | Muy alta | ✅ | Medio | Óptimo en costo, eficiente en exploración |
| **A\*** | Muy alta | ✅ | Medio-Alto | Mejor equilibrio entre tiempo y calidad |

**Síntesis:**  
El algoritmo **A\*** ofrece el mejor rendimiento global, logrando soluciones óptimas con menor exploración y menor costo total.  
**UCS** presenta resultados similares, mientras que **DFS** y **Aleatoria** son los menos eficientes.  
**BFS** resulta efectivo pero costoso en memoria y tiempo.

## 5. Conclusiones

El análisis evidencia que los algoritmos informados (A\*, UCS) superan a los no informados (BFS, DFS, DLS) en eficiencia y calidad de solución.  
A\* logra un equilibrio óptimo entre exploración, tiempo y costo, gracias a la utilización de una heurística admisible (distancia Manhattan).  

Los resultados demuestran que, en entornos con diferentes costos de movimiento, los algoritmos informados logran adaptarse mejor, manteniendo bajo el número de estados expandidos y el costo total de las acciones.

## 6. Archivos generados

* `results.csv` — resultados de 30×2×6 ejecuciones.  
* `states_n_boxplot.png` — distribución de estados explorados.  
* `actions_count_boxplot.png` — distribución de cantidad de acciones.  
* `actions_cost_boxplot.png` — distribución del costo total.  
* `time_boxplot.png` — distribución del tiempo de ejecución.

💻 **Entorno:** Python 3.12 + Gymnasium + Matplotlib + Pandas  

