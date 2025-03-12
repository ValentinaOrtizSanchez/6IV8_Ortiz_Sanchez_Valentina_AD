import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analizar_housing(housing.csv):

    df = pd.read_csv(housing.csv)
    column = "median_house_value"
    
    mean_value = np.mean(df[column])
    median_value = np.median(df[column])
    mode_value = stats.mode(df[column], keepdims=True)[0][0]
    range_value = np.ptp(df[column])
    variance_value = np.var(df[column], ddof=1)
    std_dev_value = np.std(df[column], ddof=1)
    
    freq_table = df[column].value_counts().reset_index()
    freq_table.columns = [column, "Frecuencia"]
    freq_table = freq_table.sort_values(by=column)
    
    print("Resumen Estadístico:")
    print(pd.DataFrame({
        "Métrica": ["Media", "Mediana", "Moda", "Rango", "Varianza", "Desviación Estándar"],
        "Valor": [mean_value, median_value, mode_value, range_value, variance_value, std_dev_value]
    }))
    
    print("\nTabla de Frecuencias:")
    print(freq_table.head(10))  
    
    plt.figure(figsize=(10, 6))
    plt.hist(df["median_house_value"], bins=30, alpha=0.5, label="median_house_value", color='blue')
    plt.hist(df["total_bedrooms"], bins=30, alpha=0.5, label="total_bedrooms", color='red')
    plt.hist(df["population"], bins=30, alpha=0.5, label="population", color='green')
    
    plt.axvline(mean_value, color='black', linestyle='dashed', linewidth=2, label="Promedio median_house_value")
    
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia")
    plt.title("Histograma de Median House Value, Total Bedrooms y Population")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    housing.csv = "housing.csv"  
    analizar_housing(housing.csv)
