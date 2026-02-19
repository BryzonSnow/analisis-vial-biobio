import pandas as pd
import glob
import os

# 1. BUSCAR ARCHIVOS
# Busca todos los .csv en la carpeta data/raw
path_archivos = 'data/raw/*.csv'
archivos = glob.glob(path_archivos)

print(f"--> Encontré {len(archivos)} archivos CSV en data/raw/.")

lista_dfs = []

# 2. LEER Y UNIR
for archivo in archivos:
    print(f"   Leyendo: {os.path.basename(archivo)}...")
    try:
        # A veces los CSV en español vienen separados por punto y coma (;)
        # engine='python' y sep=None ayudan a detectar el separador solo.
        df_temp = pd.read_csv(archivo, encoding='latin-1', sep=None, engine='python')
        lista_dfs.append(df_temp)
    except Exception as e:
        print(f"   [ERROR] No se pudo leer {archivo}: {e}")

if len(lista_dfs) > 0:
    # Unimos todos los archivos en uno solo
    df_total = pd.concat(lista_dfs, ignore_index=True)
    print(f"\n--> ¡ÉXITO! Base de datos consolidada creada.")
    print(f"--> Total de siniestros cargados: {len(df_total)}")
    
    # 3. INSPECCIÓN DE COLUMNAS (Lo que nos importa ahora)
    print("\n--- NOMBRES DE LAS COLUMNAS ---")
    print(df_total.columns.tolist())
    
    print("\n--- EJEMPLO DE UNA FILA ---")
    # Mostramos la primera fila transpuesta para leerla mejor
    print(df_total.iloc[0])
else:
    print("\n[ERROR] No se cargaron datos. Revisa que los archivos estén en data/raw/")