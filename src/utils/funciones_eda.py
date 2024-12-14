import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def cardinalidad(df, umbral_categoria, umbral_continua):
    resultados = []
    
    for columna in df.columns:
        # Calcular la cardinalidad como el número de valores únicos
        valores_unicos = df[columna].nunique()
        # Calcular el porcentaje de cardinalidad
        porcentaje_cardinalidad = valores_unicos / len(df) * 100
        
        # Clasificación según la cardinalidad
        if valores_unicos == 2:
            tipo = "Binaria"
        elif valores_unicos < umbral_categoria:
            tipo = "Categórica"
        else:
            if porcentaje_cardinalidad >= umbral_continua:
                tipo = "Numérica Continua"
            else:
                tipo = "Numérica Discreta"
        
        resultados.append({
            "Columna": columna,
            "Cardinalidad": valores_unicos,
            "Porcentaje Cardinalidad": porcentaje_cardinalidad,
            "Tipo": tipo
        })
    
    # Convertir los resultados a un DataFrame
    return pd.DataFrame(resultados)

