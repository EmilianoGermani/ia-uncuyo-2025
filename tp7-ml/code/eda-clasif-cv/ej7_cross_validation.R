# ============================================================
# Ejercicio 7 - Validación cruzada (k-fold) con árbol de decisión (rpart)
# ============================================================

# --- Librerías necesarias ---
library(dplyr)
library(rpart)

# --- Crear carpetas si no existen ---
if(!dir.exists("data")) dir.create("data")
if(!dir.exists("plots")) dir.create("plots")

# --- Cargar dataset de entrenamiento ---
train_df <- read.csv("data/arbolado-mendoza-dataset-train.csv")

# ============================================================
# 7a) Crear función create_folds()
# ============================================================
# Esta función recibe el dataframe y la cantidad de folds (k)
# y devuelve una lista con los índices de cada fold.
create_folds <- function(df, k = 10, seed = 42) {
  set.seed(seed)
  n <- nrow(df)
  indices <- sample(1:n)  # mezcla aleatoria de índices
  folds <- split(indices, cut(seq_along(indices), breaks = k, labels = FALSE))
  names(folds) <- paste0("Fold", 1:k)
  return(folds)
}

# ============================================================
# Función auxiliar para calcular métricas
# ============================================================
confusion_metrics <- function(actual, predicted) {
  TP <- sum(actual == 1 & predicted == 1, na.rm = TRUE)
  TN <- sum(actual == 0 & predicted == 0, na.rm = TRUE)
  FP <- sum(actual == 0 & predicted == 1, na.rm = TRUE)
  FN <- sum(actual == 1 & predicted == 0, na.rm = TRUE)
  
  Accuracy    <- (TP + TN) / (TP + TN + FP + FN)
  Precision   <- ifelse((TP + FP) == 0, NA, TP / (TP + FP))
  Sensitivity <- ifelse((TP + FN) == 0, NA, TP / (TP + FN))  # también llamado Recall
  Specificity <- ifelse((TN + FP) == 0, NA, TN / (TN + FP))
  
  return(c(Accuracy = Accuracy,
           Precision = Precision,
           Sensitivity = Sensitivity,
           Specificity = Specificity))
}

# ============================================================
# 7b) Función cross_validation()
# ============================================================
# Entrena un árbol de decisión con rpart() en cada fold,
# calcula las métricas y devuelve sus medias y desviaciones.
cross_validation <- function(df, k = 10, seed = 42) {
  folds <- create_folds(df, k, seed)
  metrics_list <- list()
  
  # Variables categóricas
  factor_cols <- c("seccion", "especie")
  
  for(i in 1:k) {
    cat("\n--- Fold", i, "de", k, "---\n")
    
    test_idx <- folds[[i]]
    train_idx <- setdiff(1:nrow(df), test_idx)
    
    train_fold <- df[train_idx, ]
    test_fold  <- df[test_idx, ]
    
    # Convertir variable objetivo a factor
    train_fold$inclinacion_peligrosa <- as.factor(train_fold$inclinacion_peligrosa)
    test_fold$inclinacion_peligrosa  <- as.factor(test_fold$inclinacion_peligrosa)
    
    # Alinear niveles de factores entre train y test
    for(col in factor_cols) {
      levels_train <- levels(as.factor(train_fold[[col]]))
      train_fold[[col]] <- factor(train_fold[[col]], levels = levels_train)
      test_fold[[col]]  <- factor(test_fold[[col]],  levels = levels_train)
    }
    
    # Definir fórmula del modelo
    train_formula <- formula(inclinacion_peligrosa ~ altura + circ_tronco_cm + lat + long + seccion + especie)
    
    # Entrenar árbol de decisión
    tree_model <- rpart(train_formula, data = train_fold)
    
    # Predecir sobre el conjunto de test
    predictions <- predict(tree_model, test_fold, type = 'class')
    predictions <- as.numeric(as.character(predictions))  # convertir a 0/1
    
    # Calcular métricas y guardarlas
    metrics <- confusion_metrics(actual = as.numeric(as.character(test_fold$inclinacion_peligrosa)),
                                 predicted = predictions)
    
    metrics_list[[i]] <- metrics
  }
  
  # Convertir lista a dataframe
  metrics_df <- do.call(rbind, metrics_list)
  
  # Calcular media y desviación estándar
  mean_metrics <- colMeans(metrics_df, na.rm = TRUE)
  sd_metrics   <- apply(metrics_df, 2, sd, na.rm = TRUE)
  
  # Guardar resultados en CSV
  write.csv(metrics_df, "data/arbolado-mendoza-cv-metricas-folds.csv", row.names = FALSE)
  
  # Retornar resultados
  return(list(metrics_by_fold = metrics_df,
              mean = mean_metrics,
              sd = sd_metrics))
}

# ============================================================
# Ejecución de la validación cruzada
# ============================================================
set.seed(123)
cv_results <- cross_validation(train_df, k = 10)

cat("\n============================\n")
cat("MÉTRICAS POR FOLD:\n")
print(cv_results$metrics_by_fold)

cat("\nMEDIA DE MÉTRICAS:\n")
print(cv_results$mean)

cat("\nDESVIACIÓN ESTÁNDAR DE MÉTRICAS:\n")
print(cv_results$sd)

# Guardar medias y desviaciones en un CSV
summary_df <- rbind(cv_results$mean, cv_results$sd)
rownames(summary_df) <- c("Media", "Desviación estándar")
write.csv(summary_df, "data/arbolado-mendoza-cv-resumen.csv")
cat("\n✅ Archivos generados correctamente en la carpeta /data\n")
