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

# Eliminar outliers y ver el antes y despues:

def eliminar_outliers_iqr(df, columna, factor=3.5, graficar=False):
    """
    Elimina outliers de una columna usando el método IQR con un factor ajustable.
    
    Parámetros:
    - df: DataFrame de entrada.
    - columna: (str) Nombre de la columna de la que se eliminarán los outliers.
    - factor: (float) Factor multiplicador del IQR para definir los límites (por defecto: 3.5).
    - graficar: (bool) Si es True, grafica el boxplot antes y después de eliminar outliers.
    
    Retorna:
    - DataFrame sin outliers en la columna seleccionada.
    """
    # Calcular Q1, Q3 e IQR
    Q1 = df[columna].quantile(0.25)
    Q3 = df[columna].quantile(0.75)
    IQR = Q3 - Q1

    # Definir límites ajustados con el factor
    lower_bound = Q1 - factor * IQR
    upper_bound = Q3 + factor * IQR

    # Filtrar outliers
    df_sin_outliers = df[(df[columna] >= lower_bound) & (df[columna] <= upper_bound)]
    
    # Graficar (opcional)
    if graficar:
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        # Boxplot antes
        df[columna].plot(kind='box', ax=axes[0], title=f"Antes de eliminar outliers ({columna})")
        # Boxplot después
        df_sin_outliers[columna].plot(kind='box', ax=axes[1], title=f"Después de eliminar outliers ({columna})")
        
        plt.show()
    
    return df_sin_outliers

# Eliminar outliers varias columnas:
def eliminar_outliers_iqr2(df, columnas, factor=3.5, graficar=False):
    """
    Reemplaza outliers con NaN en múltiples columnas usando IQR sin eliminar filas completas.
    
    Parámetros:
    - df: DataFrame de entrada.
    - columnas: (list) Lista de nombres de columnas a procesar.
    - factor: (float) Factor multiplicador del IQR (por defecto: 3.5).
    - graficar: (bool) Mostrar boxplots antes y después (opcional).

    Retorna:
    - DataFrame con outliers reemplazados por NaN solo en las columnas seleccionadas.
    """
    df_limpio = df.copy()
    
    for columna in columnas:
        # Calcular Q1, Q3 e IQR
        Q1 = df[columna].quantile(0.25)
        Q3 = df[columna].quantile(0.75)
        IQR = Q3 - Q1

        # Definir límites
        lower_bound = Q1 - factor * IQR
        upper_bound = Q3 + factor * IQR

        # Reemplazar outliers con NaN
        df_limpio.loc[(df[columna] < lower_bound) | (df[columna] > upper_bound), columna] = np.nan
        # Eliminar NaN
        df_limpio = df_limpio.dropna(subset=columnas)

        # Graficar boxplots (opcional)
        if graficar:
            fig, axes = plt.subplots(1, 2, figsize=(12, 5))
            df[columna].plot(kind='box', ax=axes[0], title=f"Antes de eliminar outliers ({columna})")
            df_limpio[columna].plot(kind='box', ax=axes[1], title=f"Después de eliminar outliers ({columna})")
            plt.show()

    return df_limpio

# Graficar una evolucion:
def graficar_evolucion(df, x_col, y_col, titulo="Evolución de Ventas", xlabel="Trimestre", ylabel="Cantidad Vendida"):
    """
    Función para graficar la evolución de un valor a lo largo de una columna

    Parámetros:
    - df (DataFrame): El DataFrame con los datos.
    - x_col (str): Nombre de la columna para el eje X.
    - y_col (str): Nombre de la columna para el eje Y.
    - titulo (str): Título del gráfico (opcional).
    - xlabel (str): Etiqueta del eje X (opcional).
    - ylabel (str): Etiqueta del eje Y (opcional).
    """
    plt.figure(figsize=(10, 6))  # Tamaño del gráfico

    # Graficar la línea con estilo mejorado
    plt.plot(df[x_col], df[y_col],
             marker="o", linestyle="-", color="#2C82C9", linewidth=2, markersize=8, label=y_col)
    
    # Ajustar los límites del eje Y para más espacio
    y_min, y_max = df[y_col].min(), df[y_col].max()
    plt.ylim(y_min - 100, y_max + 100)  # Ajusta los límites del eje Y

    # Añadir etiquetas sobre los puntos
    for i, value in enumerate(df[y_col]):
        plt.text(df[x_col][i], value + 50, f"{value}", 
                 ha='center', va='bottom', fontsize=10, fontweight='bold', color='black')

    # Personalización de títulos y ejes
    plt.title(titulo, fontsize=16, fontweight='bold', color="black")
    plt.xlabel(xlabel, fontsize=12, fontweight='bold', color="black")
    plt.ylabel(ylabel, fontsize=12, fontweight='bold', color="black")

    # Personalización de cuadrícula
    plt.grid(visible=True, linestyle="--", alpha=0.6)

    # Mejorar los ejes
    plt.xticks(df[x_col], fontsize=10, fontweight='bold')
    plt.yticks(fontsize=10)

    # Leyenda
    plt.legend(loc="upper right", fontsize=10, frameon=False)

    # Ajustar diseño y mostrar gráfico
    plt.tight_layout()
    plt.show()