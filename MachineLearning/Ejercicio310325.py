import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import distance

# Definimos las coordenadas de las tiendas
puntos = {
    'Punto A': (2, 3),
    'Punto B': (5, 4),
    'Punto C': (1, 1),
    'Punto D': (6, 7),
    'Punto E': (3, 5),
    'Punto F': (8, 2),
    'Punto G': (4, 6),
    'Punto H': (2, 1),
}

# Convertir las coordenadas a un dataframe para facilitar el cálculo
df_puntos = pd.DataFrame.from_dict(puntos, orient='index', columns=['x', 'y'])
print('Coordenadas de los puntos:')
print(df_puntos)

def calcular_distancias(df_puntos, metrica):
    """
    Calcula las distancias entre todos los pares de puntos usando una métrica específica

    """
    distancias = pd.DataFrame(index=df_puntos.index, columns=df_puntos.index)
    
    # Cálculo de distancias
    for i in df_puntos.index:
        for j in df_puntos.index:
            if i != j:  # No calcula la distancia del mismo punto
                distancias.loc[i, j] = metrica(df_puntos.loc[i], df_puntos.loc[j])
    
    return distancias

# Calcular distancias para cada métrica
dist_euc = calcular_distancias(df_puntos, distance.euclidean)
dist_man = calcular_distancias(df_puntos, distance.cityblock)
dist_cheb = calcular_distancias(df_puntos, distance.chebyshev)

# Función para encontrar la distancia máxima
def encontrar_distancia_maxima(distancias):
    max_value = distancias.values.max()
    punto1, punto2 = distancias.stack().idxmax()
    return max_value, punto1, punto2

# Imprimir resultados de distancias
print('\nTabla de Distancias Euclidianas:')
print(dist_euc)
print('\nTabla de Distancias Manhattan:')
print(dist_man)
print('\nTabla de Distancias Chebyshev:')
print(dist_cheb)

# Encontrar y mostrar distancias máximas
dist_max_euc, punto1_euc, punto2_euc = encontrar_distancia_maxima(dist_euc)
dist_max_man, punto1_man, punto2_man = encontrar_distancia_maxima(dist_man)
dist_max_cheb, punto1_cheb, punto2_cheb = encontrar_distancia_maxima(dist_cheb)

print("\nDistancia máxima Euclidiana:", dist_max_euc, 
      f"entre {punto1_euc} y {punto2_euc}")
print("Distancia máxima Manhattan:", dist_max_man, 
      f"entre {punto1_man} y {punto2_man}")
print("Distancia máxima Chebyshev:", dist_max_cheb, 
      f"entre {punto1_cheb} y {punto2_cheb}")

# Visualización de los puntos
plt.figure(figsize=(10, 6))
plt.scatter(df_puntos['x'], df_puntos['y'], c='red', s=100)

# Agregar etiquetas para cada punto
for punto, coord in df_puntos.iterrows():
    plt.annotate(punto, (coord['x'], coord['y']), xytext=(5, 5), 
                 textcoords='offset points', fontsize=10)

plt.title('Distribución de Puntos')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()