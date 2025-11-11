TP7B – Parte I – Validación cruzada (k-fold) con árbol de decisión

## 1. Código de las funciones `create_folds()` y `cross_validation()`

A continuación se muestra el código en R utilizado para implementar la validación cruzada con un árbol de decisión (`rpart`) sobre el archivo `arbolado-mendoza-dataset-train.csv`.

```r
create_folds <- function(df, k = 10, seed = 42) {
  set.seed(seed)
  n <- nrow(df)
  indices <- sample(1:n)  # mezcla aleatoria de índices
  folds <- split(indices, cut(seq_along(indices), breaks = k, labels = FALSE))
  names(folds) <- paste0("Fold", 1:k)
  return(folds)
}

confusion_metrics <- function(actual, predicted) {
  TP <- sum(actual == 1 & predicted == 1, na.rm = TRUE)
  TN <- sum(actual == 0 & predicted == 0, na.rm = TRUE)
  FP <- sum(actual == 0 & predicted == 1, na.rm = TRUE)
  FN <- sum(actual == 1 & predicted == 0, na.rm = TRUE)
  
  Accuracy    <- (TP + TN) / (TP + TN + FP + FN)
  Precision   <- ifelse((TP + FP) == 0, NA, TP / (TP + FP))
  Sensitivity <- ifelse((TP + FN) == 0, NA, TP / (TP + FN))  # Recall
  Specificity <- ifelse((TN + FP) == 0, NA, TN / (TN + FP))
  
  return(c(Accuracy = Accuracy,
           Precision = Precision,
           Sensitivity = Sensitivity,
           Specificity = Specificity))
}

cross_validation <- function(df, k = 10, seed = 42) {
  folds <- create_folds(df, k, seed)
  metrics_list <- list()
  
  # Variables categóricas
  factor_cols <- c("seccion", "especie")
  
  for(i in 1:k) {
    test_idx <- folds[[i]]
    train_idx <- setdiff(1:nrow(df), test_idx)
    
    train_fold <- df[train_idx, ]
    test_fold  <- df[test_idx, ]
    
    # Variable objetivo como factor
    train_fold$inclinacion_peligrosa <- as.factor(train_fold$inclinacion_peligrosa)
    test_fold$inclinacion_peligrosa  <- as.factor(test_fold$inclinacion_peligrosa)
    
    # Alinear niveles de factores
    for(col in factor_cols) {
      levels_train <- levels(as.factor(train_fold[[col]]))
      train_fold[[col]] <- factor(train_fold[[col]], levels = levels_train)
      test_fold[[col]]  <- factor(test_fold[[col]],  levels = levels_train)
    }
    
    # Fórmula del árbol de decisión
    train_formula <- formula(inclinacion_peligrosa ~ altura + circ_tronco_cm + lat + long + seccion + especie)
    
    # Entrenar modelo
    tree_model <- rpart(train_formula, data = train_fold)
    
    # Predicción sobre el fold de test
    predictions <- predict(tree_model, test_fold, type = "class")
    predictions <- as.numeric(as.character(predictions))  # 0/1
    
    # Métricas para el fold
    metrics <- confusion_metrics(
      actual    = as.numeric(as.character(test_fold$inclinacion_peligrosa)),
      predicted = predictions
    )
    
    metrics_list[[i]] <- metrics
  }
  
  # Métricas por fold en un dataframe
  metrics_df <- do.call(rbind, metrics_list)
  
  # Media y desviación estándar
  mean_metrics <- colMeans(metrics_df, na.rm = TRUE)
  sd_metrics   <- apply(metrics_df, 2, sd, na.rm = TRUE)
  
  return(list(
    metrics_by_fold = metrics_df,
    mean            = mean_metrics,
    sd              = sd_metrics
  ))
}

### 2.1 Tabla de resultados (media y desviación estándar)

| Métrica      | Media   | Desviación estándar |
|-------------|---------|---------------------|
| Accuracy    | 0,8877  | 0,0069              |
| Precision   | NA      | NA                  |
| Sensitivity | 0,0000  | 0,0000              |
| Specificity | 1,0000  | 0,0000              |

