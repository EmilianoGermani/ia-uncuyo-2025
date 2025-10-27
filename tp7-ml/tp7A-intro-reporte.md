Trabajo Practico 7A — Introducción a ML

## 1) ¿Cuándo conviene un método **flexible** vs. **inflexible**?

**a) \(n\) extremadamente grande y \(p\) pequeño →** **Flexible (mejor).**  
Con muchos datos y pocos predictores, un método flexible puede modelar relaciones más complejas reduciendo el sesgo sin que la varianza explote, porque el gran \(n\) ayuda a estabilizar el ajuste.

**b) \(p\) extremadamente grande y \(n\) pequeño →** **Inflexible (mejor).**  
En alta dimensión con pocos datos, los modelos flexibles tienden a sobreajustar y sufren la **maldición de la dimensionalidad**; conviene controlar la complejidad (regularización/estructura paramétrica).

**c) Relación altamente no lineal →** **Flexible (mejor).**  
Si la relación verdadera es muy no lineal, los métodos flexibles (p. ej., KNN, árboles, kernels) pueden aproximarla mejor que un modelo rígido lineal.

**d) Varianza del error \(\σ^2\) extremadamente alta →** **Inflexible (mejor).**  
Con mucho ruido irreducible, incrementar flexibilidad solo captura ruido (sube varianza del estimador); modelos más simples/regularizados suelen generalizar mejor.

## 2) Tipo de problema, objetivo (inferir vs predecir), \(n\) y \(p\)

**a) Empresas (500 firmas; ganancias, #empleados, industria ⇒ salario CEO)**  
- **Tipo:** **Regresión** (salario es continuo).  
- **Interés principal:** **Inferir** (entender qué factores afectan el salario).  
- **\(n\):** 500 (empresas).  
- **\(p\):** al menos 3 variables listadas; “industria” es categórica → al codificarla (dummies) aumenta \(p\).

**b) Lanzamiento de producto (éxito/fracaso; 20 productos + 13 predictores)**  
- **Tipo:** **Clasificación** (éxito/fracaso).  
- **Interés principal:** **Predecir** (si será éxito o fracaso).  
- **\(n\):** 20 (productos).  
- **\(p\):** 13 (precio, marketing, competencia + otras 10).

**c) Cambio % USD/EUR semanal 2021 según mercados (US, UK, DE)**  
- **Tipo:** **Regresión** (cambio porcentual continuo).  
- **Interés principal:** **Predecir** (el % de cambio).  
- **\(n\):** ~52 semanas en 2021.  
- **\(p\):** 3 (cambios % US, UK, Alemania).

## 3) Enfoques **muy flexibles** vs **menos flexibles** (ventajas/desventajas)

**Flexibles (KNN, árboles profundos, kernels, redes):**  
- **Ventajas:** Bajo sesgo; capturan **no linealidades** y **interacciones** complejas; gran potencial predictivo si hay suficiente \(n\).  
- **Desventajas:** Mayor **varianza** (overfitting), menor **interpretabilidad**, mayor costo computacional; sensibles a **alta dimensión**.

**Menos flexibles (lineales, árboles someros):**  
- **Ventajas:** Más **robustos** con \(n\) pequeño o ruido alto; **interpretables**; computacionalmente eficientes.  
- **Desventajas:** Mayor **sesgo**; pueden fallar si la relación es fuertemente no lineal.

**¿Cuándo preferir cada uno?**  
- **Más flexible:** relaciones no lineales, \(n\) grande respecto a \(p\), bajo ruido.  
- **Menos flexible:** \(p > n\), ruido alto, necesidad de interpretabilidad o eficiencia.

## 4) **Paramétrico** vs **No paramétrico**

**Paramétrico:** asume una **forma funcional** fija (p. ej., lineal) y estima **pocos parámetros**.  
- **Ventajas:** Simple, rápido, requiere menos datos, **interpretables**.  
- **Desventajas:** **Sesgo de especificación** si la forma no coincide con la realidad; limitada capacidad para no linealidad.

**No paramétrico:** no fija forma funcional; la **complejidad crece con los datos** (KNN, árboles, kernels).  
- **Ventajas:** **Bajo sesgo**, modela funciones complejas.  
- **Desventajas:** **Alta varianza**, necesita más datos; sensible a la dimensionalidad.

## 5) K vecinos más cercanos (KNN)

Se quiere predecir para \((X_1, X_2, X_3) = (0,0,0)\).

| Obs | X_1 | X_2 | X_3 | Y    |
|-----|----|----|----|------|
| 1   | 0  | 3  | 0  | Rojo |
| 2   | 2  | 0  | 0  | Rojo |
| 3   | 0  | 1  | 3  | Rojo |
| 4   | 0  | 1  | 2  | Verde |
| 5   | -1 | 0  | 1  | Verde |
| 6   | 1  | 1  | 1  | Rojo |

**a) Distancias a (0,0,0):**  
d= \(\sqrt{(X_1​−0)^2+(X_2​−0)^2+(X_3​−0)^2}\)

| Obs | Distancia | Y |
|-----|------------|---|
| 1 | 3.000 | Rojo |
| 2 | 2.000 | Rojo |
| 3 | 3.162 | Rojo |
| 4 | 2.236 | Verde |
| 5 | 1.414 | Verde |
| 6 | 1.732 | Rojo |

**b) \(K = 1\):** vecino más cercano: Obs 5 (**Verde**). **Predicción: Verde.**  

**c) \(K = 3\):** tres más cercanos: Obs 5 (Verde), 6 (Rojo), 2 (Rojo). Mayoría Rojo → **Predicción: Rojo.**  

**d) Si la frontera de Bayes es altamente no lineal:** conviene \(K\) **pequeño**, ya que permite una frontera local más flexible.
