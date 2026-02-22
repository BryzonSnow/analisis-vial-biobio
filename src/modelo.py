import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import warnings

# Ignorar advertencias menores para que la consola se vea limpia
warnings.filterwarnings('ignore')

print("--> Iniciando el laboratorio de Machine Learning\n")

# 1. CARGAR DATOS
df = pd.read_csv('data/processed/siniestros_conce_limpio.csv')

# 2. FEATURE ENGINEERING (Ingeniería de Características)
# Crear la variable "Tipo_Vehiculo" a partir del nombre del archivo
df['Tipo_Vehiculo'] = df['Archivo_Origen'].apply(lambda x: 'Bicicleta' if 'bici' in str(x).lower() else 'Motocicleta')

# 3. DEFINIR LA VARIABLE OBJETIVO (TARGET - Lo que queremos predecir)
# Vamos a predecir si el accidente fue GRAVE/FATAL (1) o LEVE/DAÑOS (0)
df['Es_Grave'] = ((df['Graves'] > 0) | (df['Fallecidos'] > 0)).astype(int)

print(f"Total de accidentes Leves (0): {len(df[df['Es_Grave'] == 0])}")
print(f"Total de accidentes Graves/Fatales (1): {len(df[df['Es_Grave'] == 1])}\n")

# 4. SELECCIONAR VARIABLES PREDICTORAS (FEATURES)
# Elegimos variables categóricas que tienen sentido para la predicción
columnas_predictoras = ['Comuna', 'Dia_semana', 'Zona', 'Tipo_Vehiculo']

# Filtramos para quedarnos solo con lo que necesitamos y eliminamos filas con nulos en estas columnas
df_modelo = df[columnas_predictoras + ['Es_Grave']].dropna()

# 5. TRANSFORMACIÓN DE TEXTO A NÚMEROS (One-Hot Encoding)
# Los algoritmos no leen texto. Convertimos "Bicicleta" y "Comuna" en columnas de 1s y 0s.
X = pd.get_dummies(df_modelo[columnas_predictoras], drop_first=True)
y = df_modelo['Es_Grave']

# 6. DIVISIÓN DE DATOS (Train / Test Split)
# 80% de los datos para enseñar al modelo, 20% para examinarlo (ponerlo a prueba)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 7. ENTRENAMIENTO DEL MODELO (Random Forest)
print("--> Entrenando el modelo Random Forest (Bosque Aleatorio)...")
modelo = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
modelo.fit(X_train, y_train)

# 8. EVALUACIÓN Y PREDICCIÓN
# Hacemos que el modelo adivine los resultados del 20% de prueba
predicciones = modelo.predict(X_test)

print("\n--- RESULTADOS DEL MODELO ---")
print(f"Precisión Global (Accuracy): {accuracy_score(y_test, predicciones):.2%}")
print("\nReporte de Clasificación Detallado:")
print(classification_report(y_test, predicciones))

# 9. IMPORTANCIA DE LAS VARIABLES (El "Factor Wow")
# Le preguntamos al modelo: "¿Qué variable te sirvió más para adivinar si era grave?"
importancias = pd.DataFrame({
    'Variable': X.columns,
    'Importancia': modelo.feature_importances_
}).sort_values(by='Importancia', ascending=False)

print("\n--- ¿QUÉ FACTORES CAUSAN MÁS ACCIDENTES GRAVES? (Top 5) ---")
print(importancias.head(5))
print("\n--> Prototipo ML finalizado con éxito.")