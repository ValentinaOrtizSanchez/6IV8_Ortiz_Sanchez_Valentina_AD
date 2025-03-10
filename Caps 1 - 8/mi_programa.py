import matplotlib.pyplot as plt
import numpy as np
import random
import seaborn as sns

tirosdados = [random.randrange(1, 7) for i in range(600)]
valores, frecuencias= np.unique(tirosdados, return_counts=True)

titulo = f'Resultados de tirar los dados {len(tirosdados)} veces'

sns.set_style('whitegrid')
axes = sns.barplot(x=valores, y=frecuencias, palette = 'bright')

axes.set_title(titulo)
axes.set(xlabel='Valores', ylabel='Frecuencias')

axes.set_ylim(top=max(frecuencias)*1.10)
for bar, frecuencias in zip(axes.patches, frecuencias):
    text_x=bar.get_x()+bar.get_width()/2.0
    text_y=bar.get_height()
    text= f'{frecuencias:,}\n{frecuencias/len(tirosdados):.3%}'

    axes.text(text_x, text_y, text, fontsize=11, ha='center', va='bottom')

plt.show()
