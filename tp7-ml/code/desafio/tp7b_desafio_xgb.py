from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import roc_auc_score
from xgboost import XGBClassifier


# ---------------------------------------------------------------------
# 1. Rutas y carga de datos
# ---------------------------------------------------------------------

DATA_DIR = Path("data")
TRAIN_PATH = DATA_DIR / "arbolado-mza-dataset.csv"
TEST_PATH = DATA_DIR / "arbolado-mza-dataset-test.csv"  # en Kaggle debería existir

if not TRAIN_PATH.exists():
    raise FileNotFoundError(f"No se encontró {TRAIN_PATH}. "
                            f"Verificá la ruta y el nombre del archivo.")

train_df = pd.read_csv(TRAIN_PATH)

print(f"✔ Dataset de entrenamiento cargado: {train_df.shape[0]} filas, "
      f"{train_df.shape[1]} columnas")


# ---------------------------------------------------------------------
# 2. Función de preprocesamiento
# ---------------------------------------------------------------------

def preprocess_features(df: pd.DataFrame,
                        encoders: dict | None = None,
                        fit_encoders: bool = True):
    """
    - Separa X e y (si está la columna 'inclinacion_peligrosa').
    - Descarta algunas columnas poco útiles.
    - Codifica variables categóricas.
    Devuelve (X_proc, y, encoders_actualizados)
    """
    df = df.copy()

    # Separar target si existe
    y = None
    if "inclinacion_peligrosa" in df.columns:
        y = df["inclinacion_peligrosa"].astype(int)
        df = df.drop(columns=["inclinacion_peligrosa"])

    # Eliminar columnas que no queremos usar como features
    drop_cols = [col for col in ["id", "ultima_modificacion", "nombre_seccion"]
                 if col in df.columns]
    if drop_cols:
        df = df.drop(columns=drop_cols)

    # Mapear altura a ordinal
    if "altura" in df.columns:
        altura_map = {
            "Muy bajo (1 - 2 mts)": 0,
            "Bajo (2 - 4 mts)": 1,
            "Medio (4 - 8 mts)": 2,
            "Alto (> 8 mts)": 3,
        }
        df["altura"] = df["altura"].map(altura_map).fillna(-1).astype(int)

    # Mapear diámetro de tronco a ordinal (ajustado a categorías típicas del TP)
    if "diametro_tronco" in df.columns:
        diametro_map = {
            "Chico": 0,
            "Mediano": 1,
            "Grande": 2,
        }
        df["diametro_tronco"] = df["diametro_tronco"].map(diametro_map).fillna(-1).astype(int)

    # Preparar / reutilizar LabelEncoders para especie y seccion
    if encoders is None:
        encoders = {}

    for col in ["especie", "seccion"]:
        if col in df.columns:
            if fit_encoders or col not in encoders:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                encoders[col] = le
            else:
                le = encoders[col]
                # Para valores no vistos, los pasamos a -1
                df[col] = df[col].astype(str).map(
                    lambda v: le.transform([v])[0] if v in le.classes_ else -1
                )

    # Rellenar posibles NaNs numéricos con la media de la columna
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].mean())

    return df, y, encoders


# ---------------------------------------------------------------------
# 3. Split train/valid y entrenamiento para evaluar AUC
# ---------------------------------------------------------------------

X_all, y_all, encoders = preprocess_features(train_df,
                                             encoders=None,
                                             fit_encoders=True)

X_train, X_val, y_train, y_val = train_test_split(
    X_all,
    y_all,
    test_size=0.2,
    random_state=42,
    stratify=y_all,
)

print(f"✔ Split train/valid: {X_train.shape[0]} train, {X_val.shape[0]} valid")

# Modelo XGBoost (árboles de decisión boosting)
model = XGBClassifier(
    n_estimators=500,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="binary:logistic",
    eval_metric="logloss",
    n_jobs=-1,
)

print("Entrenando modelo XGBoost...")
model.fit(X_train, y_train)

val_proba = model.predict_proba(X_val)[:, 1]
val_auc = roc_auc_score(y_val, val_proba)
print(f"✅ AUC en validación (20% hold-out): {val_auc:.4f}")


# ---------------------------------------------------------------------
# 4. Entrenar modelo final con TODOS los datos
# ---------------------------------------------------------------------

print("Entrenando modelo final con todo el conjunto de entrenamiento...")
model.fit(X_all, y_all)


# ---------------------------------------------------------------------
# 5. Generar archivo de envío para Kaggle
# ---------------------------------------------------------------------

DATA_DIR.mkdir(exist_ok=True)

if TEST_PATH.exists():
    # Caso normal: Kaggle / dataset con archivo de test aparte
    test_df = pd.read_csv(TEST_PATH)
    print(f"✔ Dataset de test cargado: {test_df.shape[0]} filas")

    X_test, _, _ = preprocess_features(
        test_df, encoders=encoders, fit_encoders=False
    )

    test_proba = model.predict_proba(X_test)[:, 1]

    if "id" in test_df.columns:
        ids = test_df["id"].values
    else:
        ids = np.arange(len(test_df))

    submission = pd.DataFrame(
        {"id": ids, "inclinacion_peligrosa": test_proba}
    )
    out_path = DATA_DIR / "submission_xgb_test.csv"
    submission.to_csv(out_path, index=False)

    print(f"📁 Archivo de envío generado: {out_path} "
          f"({submission.shape[0]} filas)")
else:
    # Fallback local: no existe test, generamos predicciones para todo el train
    print("⚠ No se encontró archivo de test "
          f"({TEST_PATH}). Generando predicciones sobre todo el "
          "dataset de entrenamiento (solo para prueba local).")

    full_proba = model.predict_proba(X_all)[:, 1]

    if "id" in train_df.columns:
        ids = train_df["id"].values
    else:
        ids = np.arange(len(train_df))

    submission = pd.DataFrame(
        {"id": ids, "inclinacion_peligrosa": full_proba}
    )
    out_path = DATA_DIR / "submission_xgb_fulltrain.csv"
    submission.to_csv(out_path, index=False)

    print(f"📁 Archivo con predicciones generado: {out_path} "
          f"({submission.shape[0]} filas)")

print("\nListo. Usá el archivo de 'submission' correspondiente para subirlo a Kaggle.")
