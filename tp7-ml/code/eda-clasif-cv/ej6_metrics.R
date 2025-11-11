# === Ejercicio 6: Cálculo de métricas a partir de matriz de confusión ===
library(dplyr)

# -------------------------------------------------------------------------
# Funciones para calcular métricas
# -------------------------------------------------------------------------
calculate_accuracy <- function(TP, TN, FP, FN) {
  (TP + TN) / (TP + TN + FP + FN)
}

calculate_precision <- function(TP, FP) {
  ifelse((TP + FP) == 0, NA, TP / (TP + FP))
}

calculate_sensitivity <- function(TP, FN) {  # también llamado Recall
  ifelse((TP + FN) == 0, NA, TP / (TP + FN))
}

calculate_specificity <- function(TN, FP) {
  ifelse((TN + FP) == 0, NA, TN / (TN + FP))
}

# -------------------------------------------------------------------------
# Matrices de confusión obtenidas en los ejercicios anteriores
# -------------------------------------------------------------------------
# Clasificador aleatorio (ejercicio 4)
TP_r <- 363
TN_r <- 2888
FP_r <- 2783
FN_r <- 348

# Clasificador clase mayoritaria (ejercicio 5)
TP_b <- 0
TN_b <- 5671
FP_b <- 0
FN_b <- 711

# -------------------------------------------------------------------------
# Cálculo de métricas
# -------------------------------------------------------------------------
metrics_random <- data.frame(
  Clasificador = "Aleatorio",
  Accuracy     = calculate_accuracy(TP_r, TN_r, FP_r, FN_r),
  Precision    = calculate_precision(TP_r, FP_r),
  Sensitivity  = calculate_sensitivity(TP_r, FN_r),
  Specificity  = calculate_specificity(TN_r, FP_r)
)

metrics_bigger <- data.frame(
  Clasificador = "Clase mayoritaria",
  Accuracy     = calculate_accuracy(TP_b, TN_b, FP_b, FN_b),
  Precision    = calculate_precision(TP_b, FP_b),
  Sensitivity  = calculate_sensitivity(TP_b, FN_b),
  Specificity  = calculate_specificity(TN_b, FP_b)
)

# Unir ambas en una sola tabla
metrics_table <- rbind(metrics_random, metrics_bigger)

# -------------------------------------------------------------------------
# Mostrar resultados
# -------------------------------------------------------------------------
cat("\n--- Métricas de desempeño ---\n")
print(metrics_table)

# Guardar tabla como CSV para incluir en el informe
write.csv(metrics_table, "data/arbolado-mendoza-metricas.csv", row.names = FALSE)
