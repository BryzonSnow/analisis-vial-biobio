import pandas as pd

print("--> Analizando los datos limpios...\n")

# Cargar datos
df = pd.read_csv('data/processed/siniestros_conce_limpio.csv')

# Crear una columna más limpia para el tipo de vehículo
df['Tipo_Vehiculo'] = df['Archivo_Origen'].apply(lambda x: 'Bicicleta' if 'bici' in str(x).lower() else 'Motocicleta')

# 1. TOTALES
print("--- RESUMEN GENERAL ---")
print(df['Tipo_Vehiculo'].value_counts())
print("-" * 25)

# 2. LAS COMUNAS MÁS PELIGROSAS
print("\n--- TOP COMUNAS CON MÁS SINIESTROS ---")
resumen_comunas = df.groupby(['Comuna', 'Tipo_Vehiculo']).size().unstack(fill_value=0)
resumen_comunas['Total'] = resumen_comunas.sum(axis=1)
print(resumen_comunas.sort_values(by='Total', ascending=False))

# 3. GRAVEDAD (¿Qué tan feos son los accidentes?)
# Sumamos las columnas de lesionados y fallecidos
print("\n--- CONSECUENCIAS (Total de víctimas) ---")
columnas_gravedad = ['Fallecidos', 'Graves', 'Menos_Grav', 'Leves']
# Filtramos solo las columnas que existan para no tener errores
columnas_existentes = [col for col in columnas_gravedad if col in df.columns]
print(df.groupby('Tipo_Vehiculo')[columnas_existentes].sum())