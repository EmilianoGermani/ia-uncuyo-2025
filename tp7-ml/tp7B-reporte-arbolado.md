TP7B – Parte II: Desafío Kaggle – Predicción de inclinación peligrosa del arbolado público de Mendoza

## 1. Descripción general del problema

El objetivo del desafío es **predecir la peligrosidad del arbolado público de Mendoza**, es decir, si un árbol presenta una inclinación peligrosa (`inclinacion_peligrosa = 1`) o no (`inclinacion_peligrosa = 0`).  
La métrica utilizada para evaluar el rendimiento del modelo es el **AUC (Area Under the ROC Curve)**, y el trabajo práctico requiere obtener un valor superior a **0.69**.

## 2. Proceso de preprocesamiento

Se utilizó como base el archivo `arbolado-mza-dataset.csv`, que contiene información de cada ejemplar de árbol, incluyendo características como altura, circunferencia del tronco, ubicación (latitud y longitud), sección y especie.

El preprocesamiento consistió en los siguientes pasos:

1. **Eliminación de columnas irrelevantes o redundantes**:
   - Se mantuvieron solo las variables más informativas:  
     `altura`, `circ_tronco_cm`, `lat`, `long`, `seccion`, `especie` e `inclinacion_peligrosa`.
   - Se descartaron variables de identificación u observación manual que no aportaban valor predictivo.

2. **Tratamiento de valores faltantes**:
   - Los registros con valores faltantes en variables numéricas fueron completados mediante la imputación con la **mediana** de la columna correspondiente.
   - Para variables categóricas (`seccion` y `especie`), los valores faltantes se reemplazaron por la categoría `"Desconocido"`.

3. **Codificación de variables categóricas**:
   - Se aplicó **One-Hot Encoding** para transformar las variables `seccion` y `especie` en variables numéricas binarias, permitiendo que el modelo pueda procesarlas correctamente.

4. **Escalado de variables numéricas**:
   - Dado que los algoritmos de árboles como XGBoost **no son sensibles a la escala**, no fue necesario normalizar las variables numéricas entre (0, 1).

5. **Separación de conjuntos**:
   - Se realizó un **split del 80 % para entrenamiento y 20 % para validación** interna, garantizando una evaluación objetiva del modelo antes del envío a Kaggle.
   - Posteriormente, se utilizó el conjunto `arbolado-mza-dataset-test.csv` para generar las predicciones finales destinadas al archivo de envío.

## 3. Descripción del algoritmo propuesto

Para resolver el problema se utilizó el algoritmo **XGBoost (Extreme Gradient Boosting)**, un modelo basado en **árboles de decisión con boosting**.  
Este enfoque combina múltiples árboles débiles de forma secuencial, de manera que cada árbol corrige los errores cometidos por los anteriores, logrando un modelo robusto y de alta capacidad predictiva.

### Características del modelo:
- **Tipo de modelo:** Clasificador binario (árboles de decisión).
- **Librería:** `xgboost` (versión para Python).
- **Parámetros utilizados:**
  - `n_estimators = 200`
  - `learning_rate = 0.1`
  - `max_depth = 6`
  - `subsample = 0.8`
  - `colsample_bytree = 0.8`
  - `random_state = 42`
- **Métrica de evaluación:** AUC (Area Under Curve).

El modelo fue elegido por su **capacidad de manejar relaciones no lineales**, su **resistencia al sobreajuste** y su **eficiencia computacional** frente a conjuntos de datos de tamaño medio como el del arbolado de Mendoza.

## 4. Resultados obtenidos en el conjunto de validación

Tras entrenar el modelo con un 80 % del conjunto de entrenamiento y evaluar sobre el 20 % restante (hold-out interno), se obtuvo un resultado de:

| Métrica | Valor |
|----------|--------|
| **AUC (validación interna)** | **0.7785** |

## 5. Resultados obtenidos en Kaggle

El archivo de envío generado fue `submission_xgb_test.csv`, con **13.676 filas**, correspondiente al conjunto de test provisto por el desafío.

El archivo fue subido correctamente a la competencia  
**[“Inclinación del Arbolado Público Mendoza 2025”](https://www.kaggle.com/competitions/arbolado-publico-mendoza-2025)**  
y obtuvo el siguiente puntaje público:

| Métrica | Valor |
|----------|--------|
| **AUC (Kaggle Public Score)** | **0.77919** |

## 6. Conclusiones

- El modelo XGBoost alcanzó un **AUC de 0.7785 en validación local** y **0.77919 en Kaggle**, superando con holgura el requisito del trabajo práctico.
- No se aplicó normalización debido a que los árboles de decisión son invariantes ante la escala de las variables.
- Se aplicó un preprocesamiento liviano pero suficiente: limpieza de datos, codificación de variables categóricas y separación de conjuntos.

