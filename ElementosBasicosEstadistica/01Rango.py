import pandas as pd 
##Escribir un programa que pregunte al usuario por las ventas de un rango de años y muestre en la pantalla una serie de datos de ventas indexadas por los años.. antes y después de aplicarles un descuento.

inicio = int(input('Introduce el año de ventas inicial: '))
fin = int(input('Introduce el año final de ventas: '))

ventas = {}

for i in range(inicio, fin+1):
    ventas[i] = float(input ('Introduce ventas del año' + str(i) + ': '))

    ventas  = pd.Series(ventas)
    print('Ventas \n', ventas)
    print('Ventas con descuento\n', ventas*0.9)
     