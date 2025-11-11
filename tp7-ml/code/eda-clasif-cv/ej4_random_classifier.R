# === Ejercicio 4: Clasificador aleatorio ===
library(dplyr)

# Crear carpeta de salida (si no existe)
if(!dir.exists("data")) dir.create("data")

# Cargar dataset de validación
val_df <- read.csv("data/arbolado-mendoza-dataset-validation.csv")

# a) y b) Función clasificador aleatorio
random_classifier <- function(df) {
  df <- df %>% mutate(
    prediction_prob = runif(nrow(df)),               # valores aleatorios entre 0 y 1
    prediction_class = ifelse(prediction_prob > 0.5, 1, 0)  # criterio de clasificación
  )
  return(df)
}

# Aplicar clasificador
val_random <- random_classifier(val_df)

# Guardar resultados
write.csv(val_random, "data/arbolado-mendoza-random.csv", row.names = FALSE)

# d) Calcular TP, TN, FP, FN y matriz de confusión
TP <- sum(val_random$inclinacion_peligrosa == 1 & val_random$prediction_class == 1)
TN <- sum(val_random$inclinacion_peligrosa == 0 & val_random$prediction_class == 0)
FP <- sum(val_random$inclinacion_peligrosa == 0 & val_random$prediction_class == 1)
FN <- sum(val_random$inclinacion_peligrosa == 1 & val_random$prediction_class == 0)

# Mostrar resultados
cat("\n--- Resultados ---\n")
cat("TP:", TP, "\nTN:", TN, "\nFP:", FP, "\nFN:", FN, "\n")

# Crear matriz de confusión
conf_matrix <- matrix(
  c(TP, FP, FN, TN),
  nrow = 2,
  byrow = TRUE,
  dimnames = list("Predicted" = c("1", "0"), "Actual" = c("1", "0"))
)

cat("\nMatriz de Confusión:\n")
print(conf_matrix)
