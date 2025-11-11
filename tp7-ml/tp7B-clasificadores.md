TP7B – Parte I – Clasificadores base

En esta sección se resumen los resultados de:

- Clasificador **aleatorio** (Ejercicio 4).
- Clasificador por **clase mayoritaria** (Ejercicio 5).

Las métricas se calcularon en el conjunto de validación (`arbolado-mendoza-dataset-validation.csv`).

## 1. Clasificador aleatorio

El clasificador aleatorio genera, para cada árbol, una probabilidad `prediction_prob ~ U(0,1)` y asigna:

- `prediction_class = 1` si `prediction_prob > 0,5`
- `prediction_class = 0` en caso contrario.

### 1.1 Matriz de confusión

A partir de las predicciones generadas y de la verdadera clase `inclinacion_peligrosa`, se obtuvo:

- TP = 363  
- TN = 2 888  
- FP = 2 783  
- FN = 348  

Matriz de confusión (Predicho vs Real):

| Predicho \\ Real | 1 (peligrosa) | 0 (no peligrosa) |
|------------------|---------------|------------------|
| **1 (peligrosa)**| TP = 363      | FP = 2 783       |
| **0 (no pelig.)**| FN = 348      | TN = 2 888       |

### 1.2 Métricas

Se calcularon las métricas estándar:

\[
\text{Accuracy}    = \frac{TP + TN}{TP + TN + FP + FN}
\]
\[
\text{Precision}   = \frac{TP}{TP + FP}
\]
\[
\text{Sensitivity} = \frac{TP}{TP + FN}
\]
\[
\text{Specificity} = \frac{TN}{TN + FP}
\]

Resultados:

| Clasificador | Accuracy | Precision | Sensitivity | Specificity |
|-------------|----------|-----------|-------------|-------------|
| Aleatorio   | 0,5094   | 0,1154    | 0,5105      | 0,5093      |

**Interpretación:**  
El clasificador aleatorio acierta aproximadamente el **51 %** de los casos, como era esperable para un modelo sin información. Tanto Sensitivity como Specificity se encuentran cerca de 0,5.

## 2. Clasificador por clase mayoritaria

Este clasificador siempre predice la **clase más frecuente** observada en el conjunto de validación.  
En nuestro caso, la clase mayoritaria es `0` (no peligrosa), por lo que:

- `prediction_class = 0` para todos los árboles.

### 2.1 Matriz de confusión

A partir de las predicciones y la clase real:

- TP = 0  
- TN = 5 671  
- FP = 0  
- FN = 711  

Matriz de confusión:

| Predicho \\ Real | 1 (peligrosa) | 0 (no peligrosa) |
|------------------|---------------|------------------|
| **1 (peligrosa)**| TP = 0        | FP = 0           |
| **0 (no pelig.)**| FN = 711      | TN = 5 671       |

### 2.2 Métricas

| Clasificador        | Accuracy | Precision | Sensitivity | Specificity |
|---------------------|----------|-----------|-------------|-------------|
| Clase mayoritaria   | 0,8886   | NA        | 0,0000      | 1,0000      |

- **Accuracy ≈ 0,89:** el modelo acierta casi todos los casos, pero solo porque la clase negativa es muy frecuente.
- **Sensitivity = 0:** nunca detecta árboles peligrosos (ningún positivo correcto).
- **Specificity = 1:** clasifica perfectamente a los árboles no peligrosos.
- **Precision = NA:** no se puede definir porque el modelo nunca predice clase 1 (TP + FP = 0).

**Conclusión general:**  
El clasificador por clase mayoritaria obtiene una Accuracy alta debido al desbalance de clases, pero es inútil para detectar árboles peligrosos. El clasificador aleatorio tiene un desempeño cercano al azar. Ambos modelos sirven como **baseline** para comparar con modelos más sofisticados en etapas posteriores.

