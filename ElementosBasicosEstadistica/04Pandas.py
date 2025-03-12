import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('ElementosBasicosEstadistica/housing.csv')

##Mostrar las primeras 5 filas
print(df.head())

##Mostrar las ultimas 5 filas
print(df.tail())

##Mostrar fila en especifico
print(df.iloc[7])

##Mostrar columna ocean_proximity
print(df["ocean_proximity"])

#Obtener la media de la columna total_rooms
mediadecuarto = df["total_rooms"].mean()
print('La media dde total room es: ', mediadecuarto)

medianacuarto = df["median_house_value"].median()
print('La mediana de median house value es: ', medianacuarto)

##La suma de popular
salariototal = df["population"].sum()
print('El salario total es: ', salariototal)

##Para poder filtrar
vamosahacerunfiltro = df[df['ocean_proximity'] == 'ISLAND']
print(vamosahacerunfiltro)

##vamos a hacer un grafico de dispersión
plt.scatter(df['ocean_proximity'][:10], df['median_house_value'][:10])

##Nombramos los ejes
plt.xlabel("Proximidad")
plt.ylabel("Precio")

plt.title("Gráfico de dispersión de proximidad al océano vs precio")
plt.show()