# === Ejercicio 5: Clasificador por clase mayoritaria ===
library(dplyr)

# Cargar dataset de validación
val_df <- read.csv("data/arbolado-mendoza-dataset-validation.csv")

# Función del clasificador
biggerclass_classifier <- function(df, target_col="inclinacion_peligrosa") {
  # Identificar la clase más frecuente (0 o 1)
  major_class <- as.numeric(names(which.max(table(df[[target_col]]))))
  
  # Agregar columna de predicciones (todo igual a la clase mayoritaria)
  df <- df %>% mutate(prediction_class = major_class)
  
  return(df)
}

# Aplicar clasificador
val_bigger <- biggerclass_classifier(val_df, "inclinacion_peligrosa")

# Guardar resultados
write.csv(val_bigger, "data/arbolado-mendoza-biggerclass.csv", row.names = FALSE)

# Calcular métricas
TP <- sum(val_bigger$inclinacion_peligrosa == 1 & val_bigger$prediction_class == 1)
TN <- sum(val_bigger$inclinacion_peligrosa == 0 & val_bigger$prediction_class == 0)
FP <- sum(val_bigger$inclinacion_peligrosa == 0 & val_bigger$prediction_class == 1)
FN <- sum(val_bigger$inclinacion_peligrosa == 1 & val_bigger$prediction_class == 0)

cat("\n--- Resultados Clasificador Clase Mayoritaria ---\n")
cat("Clase mayoritaria predicha:", unique(val_bigger$prediction_class), "\n")
cat("TP:", TP, "\nTN:", TN, "\nFP:", FP, "\nFN:", FN, "\n")

# Matriz de confusión
conf_matrix <- matrix(
  c(TP, FP, FN, TN),
  nrow = 2,
  byrow = TRUE,
  dimnames = list("Predicted" = c("1","0"), "Actual" = c("1","0"))
)

cat("\nMatriz de Confusión:\n")
print(conf_matrix)
