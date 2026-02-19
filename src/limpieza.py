import pandas as pd
import glob
import os

print("--> Iniciando proceso de limpieza de datos...")

# 1. CARGAR DATOS
archivos = glob.glob('data/raw/*.csv')
lista_dfs = []

for archivo in archivos:
    try:
        df_temp = pd.read_csv(archivo, encoding='latin-1', sep=None, engine='python')
        # Creamos una columna temporal para saber de qué archivo viene (opcional pero útil)
        df_temp['Archivo_Origen'] = os.path.basename(archivo)
        lista_dfs.append(df_temp)
    except Exception as e:
        print(f"   [ERROR] No se pudo leer {archivo}: {e}")

df_total = pd.concat(lista_dfs, ignore_index=True)
print(f"--> Total datos crudos: {len(df_total)} siniestros.")

# 2. FILTRAR POR COMUNAS DEL GRAN CONCEPCIÓN
# Usamos upper() por si en un archivo dice "Concepcion" y en otro "CONCEPCION"
comunas_conce = ['CONCEPCION', 'TALCAHUANO', 'CHIGUAYANTE', 'SAN PEDRO DE LA PAZ', 'HUALPEN']

# Aplicamos el filtro asegurándonos de que la columna sea string y esté en mayúsculas
df_conce = df_total[df_total['Comuna'].astype(str).str.upper().isin(comunas_conce)].copy()
print(f"--> Accidentes en el Gran Concepción: {len(df_conce)}")

# 3. LIMPIEZA DE COORDENADAS
# Botamos a la basura las filas que no tengan Latitud o Longitud, o que sean cero
df_conce = df_conce.dropna(subset=['Lat', 'Lon'])
df_conce = df_conce[(df_conce['Lat'] != 0) & (df_conce['Lon'] != 0)]
print(f"--> Accidentes con coordenadas GPS válidas: {len(df_conce)}")

# 4. GUARDAR EL RESULTADO
ruta_salida = 'data/processed/siniestros_conce_limpio.csv'

# Guardamos usando UTF-8 para arreglar un poco los caracteres raros en el futuro
df_conce.to_csv(ruta_salida, index=False, encoding='utf-8')
print(f"--> ¡ÉXITO! Archivo limpio guardado en: {ruta_salida}")