import pandas as pd
import matplotlib.pyplot as plt

def cargar_datos(ruta_archivo):
    return pd.read_csv(ruta_archivo)

def calcular_estadisticas(df, columnas):
    stats = {
        "Media": df[columnas].mean(),
        "Mediana": df[columnas].median(),
        "Moda": df[columnas].mode().iloc[0],  
        "Rango": df[columnas].max() - df[columnas].min(),
        "Varianza": df[columnas].var(),
        "Desviación Estándar": df[columnas].std()
    }
    return pd.DataFrame(stats)

def tabla_frecuencias(df, columna, bins=10):
    df[columna + '_bins'] = pd.cut(df[columna], bins=bins)
    freq_table = df[columna + '_bins'].value_counts().sort_index().reset_index()
    freq_table.columns = ["Intervalo", "Frecuencia"]
    return freq_table

def generar_histograma(df, columnas, titulo="Histograma comparativo"):
    plt.figure(figsize=(10, 6))
    for columna in columnas:
        plt.hist(df[columna], bins=30, alpha=0.5, label=columna)
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia")
    plt.title(titulo)
    plt.legend()
    plt.grid(True)
    plt.show()

ruta_csv = "housing.csv"

df = cargar_datos(ruta_csv)
columnas_analisis = ['median_house_value', 'total_bedrooms', 'population']

estadisticas = calcular_estadisticas(df, columnas_analisis)
print("\nEstadísticas Descriptivas:\n", estadisticas)

tabla_frec = tabla_frecuencias(df, 'median_house_value')
print("\nTabla de Frecuencias:\n", tabla_frec)

generar_histograma(df, columnas_analisis)