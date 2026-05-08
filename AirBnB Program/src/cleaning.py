import pandas as pd
import numpy as np

def LimpiezaProfunda(df_entrada):
    """
    Función que replica exactamente la limpieza de datos
    utilizada durante el entrenamiento del modelo.
    """
    # Creamos una copia para no modificar el original por accidente
    df = df_entrada.copy()

    # 1. Eliminar duplicados
    df = df.drop_duplicates()

    # 2. Limpiar nombres de columnas (espacios y minúsculas)
    df.columns = df.columns.str.strip().str.lower()

    # 3. Identificar columnas por tipo
    numericas = df.select_dtypes(include=[np.number]).columns
    categoricas = df.select_dtypes(include=['object']).columns

    # 4. Procesar Numéricas: Convertir y rellenar nulos con la media
    for col in numericas:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        if df[col].isnull().sum() > 0:
            # Aquí un detalle: en la App, si falta un dato, 
            # podrías usar valores precalculados del entrenamiento
            media = df[col].mean()
            df[col] = df[col].fillna(media)

    # 5. Procesar Categóricas: Rellenar nulos con la moda
    for col in categoricas:
        if df[col].isnull().sum() > 0:
            moda = df[col].mode()[0]
            df[col] = df[col].fillna(moda)

    return df