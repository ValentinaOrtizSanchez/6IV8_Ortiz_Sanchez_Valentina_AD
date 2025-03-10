import pandas as pd
##Escribir una funcion que reciba un diccionario con las notas de los estudiantes del curso y devuelve una serie con minimo, máximo, media, desviación típica

def estadistica_notas(notas):
    notas = pd.Series(notas)
    estadisticas = pd.Series(notas.min(), notas.max(), notas.mean(), notas.std())
    
