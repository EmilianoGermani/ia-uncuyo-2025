Informe Comparativo – Agentes en el Mundo de la Aspiradora
1. Introducción

En este trabajo se analiza el desempeño de diferentes agentes en el entorno clásico del mundo de la aspiradora (Russell & Norvig). El objetivo es observar cómo varía la performance de los agentes en función del tamaño del entorno y del nivel de suciedad inicial.

Los agentes evaluados son:

Agente Reflexivo: se basa en reglas simples como limpiar si la celda está sucia y recorrer el entorno siguiendo un patrón de serpiente, desde la posicion donde empieza hasta llegar a la ultima celda de la ultima fila.

Agente Aleatorio: selecciona sus acciones sin un criterio específico, eligiendo movimientos al azar, pero si encuentra una celda sucia la limpia.

El foco del análisis está en comparar cuántas celdas son efectivamente limpiadas según el porcentaje de suciedad y cómo esto se ve afectado por el tamaño del mapa.

2. Metodología para la comparación de ambos agentes

Tamaños de mapa evaluados: 2x2, 4x4, 8x8, 16x16, 32x32, 64x64 y 128x128.

Niveles de suciedad inicial: 0.1, 0.2, 0.4 y 0.8.

Métrica medida: número de celdas limpiadas por el agente.

Procedimiento: para cada combinación de tamaño y porcentaje de suciedad se ejecutaron varias corridas y se representaron los resultados en un gráfico.

Visualización: se generó un gráfico por cada tamaño de mapa, en el que el eje X representa el porcentaje de suciedad inicial y el eje Y la cantidad de celdas limpiadas en promedio.

3. Resultados
   
3.1. Entorno 2x2

En el tablero más chico, de 2×2, la diferencia entre los agentes es prácticamente mínima. Ambos logran limpiar una cantidad similar de casillas, ya que el espacio reducido no permite que aparezcan grandes variaciones de desempeño, pero el agente random sigue logrando limpiar el total de casillas en comparacion con el agente reflexivo.
<img width="1546" height="801" alt="2x2" src="https://github.com/user-attachments/assets/980acd53-cba4-4bd4-874f-b168e6a1ba8e" />

3.2. Entorno 4x4

El gráfico muestra que el agente aleatorio logra limpiar más casillas que el reflexivo en un tablero pequeño de 4×4. La diferencia es clara, ya que el espacio reducido favorece al random, que termina cubriendo gran parte del tablero casi sin importar la secuencia de movimientos. El reflexivo, en cambio, se ve limitado en su capacidad de alcanzar tantas casillas.
<img width="1546" height="780" alt="4x4" src="https://github.com/user-attachments/assets/2e21e6cc-4f3f-4d2f-9761-0de849163ef9" />

3.3. Entorno 8x8

El agente random continúa siendo superior en este tamaño, alcanzando una mayor proporción de casillas limpias. El reflexivo todavía queda por detrás, lo que refuerza la tendencia de que en tableros pequeños e intermedios el random resulta más efectivo en cuanto a cantidad de celdas limpiadas.
<img width="1547" height="776" alt="8x8" src="https://github.com/user-attachments/assets/c57bbea3-1f39-40ac-bed7-769a12e15be6" />

3.4. Entorno 16x16

En este tamaño se confirma que el agente aleatorio logra limpiar una cantidad considerablemente mayor de casillas en todas las pruebas realizadas. El reflexivo, en cambio, prácticamente no consigue limpiar: de las 40 corridas solo obtuvo resultados en un único caso, correspondiente a un dirty_rate de 0.1, mientras que en el resto no alcanzó a limpiar ninguna casilla. Esto muestra que su desempeño en este escenario es casi nulo frente al random.

<img width="1548" height="783" alt="16x16" src="https://github.com/user-attachments/assets/361e4c29-80e8-4bce-95cd-7702ca436202" />

3.5. Entorno 32x32

Aquí se empieza a notar un cambio en la tendencia. Si bien el random todavía mantiene un desempeño relativamente bueno, el reflexivo empieza a mejorar y logra un mejor desempeño que el agente random en la mayoria de los casos. Esto sugiere que en tableros más grandes el reflexivo puede aprovechar mejor su estrategia.
<img width="1553" height="777" alt="32x32" src="https://github.com/user-attachments/assets/8aecea3f-c13b-4da3-a068-48611d361ed4" />

3.6. Entorno 64x64

En este tamaño ya se observa que el agente reflexivo supera al random. El aleatorio, al depender de movimientos sin dirección, no consigue mantener su nivel de limpieza cuando la superficie se vuelve más extensa. En cambio, el reflexivo muestra un mejor desempeño y logra limpiar más casillas en promedio.
<img width="1553" height="779" alt="64x64" src="https://github.com/user-attachments/assets/de8a78fb-da31-4e43-bdbd-74b06cf0cf7f" />

3.7. Entorno 128x128

La diferencia entre ambos agentes se amplía a favor del reflexivo. El random cae notablemente en la cantidad de casillas cubiertas, mientras que el reflexivo mantiene un progreso sostenido, consolidándose como la mejor opción en tableros grandes.
<img width="1552" height="778" alt="128x128" src="https://github.com/user-attachments/assets/45d5bfa5-f335-46e6-ab97-7a635d0bb38f" />

4. Conclusiones

El agente reflexivo demuestra ser más eficiente tamaños mas grandes del spacio, manteniendo un nivel de limpieza cercano al máximo esperado.

El agente aleatorio solo funciona aceptablemente en entornos pequeños (2x2, 4x4, 8x8 y 16x16). En mapas más grandes su rendimiento cae bastante.

Los resultados confirman que incluso una estrategia simple basada en percepciones supera a la aleatoriedad pura, especialmente cuando la complejidad del entorno aumenta.
