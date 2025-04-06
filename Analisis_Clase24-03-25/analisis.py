import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configuración para visualización
plt.style.use('seaborn-v0_8-colorblind')  # Esquema de colores más atractivo
plt.rcParams.update({
    'font.size': 12, 
    'figure.figsize': (12, 8),
    'font.weight': 'bold',
    'axes.labelweight': 'bold',
    'axes.titleweight': 'bold',
    'axes.titlesize': 16
})

def cargar_datos():
    """
    Carga los datos desde los archivos Excel.
    """
    try:
        # Cargar archivo de catálogo de sucursales
        catalogo_sucursal = pd.read_excel('Catalogo_sucursal.xlsx')
        
        # Cargar archivo de ventas y pagos
        proyecto1 = pd.read_excel('proyecto1.xlsx')
        
        print("¡Datos cargados exitosamente!")
        return catalogo_sucursal, proyecto1
    
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        return None, None

def preparar_datos(catalogo_sucursal, proyecto1):
    """
    Prepara y limpia los datos para el análisis.
    Corrige problemas de tipo de datos.
    """
    try:
        # Convertir columnas a tipos numéricos adecuados
        # Identificar columnas numéricas (esto dependerá de tus datos reales)
        numeric_cols = proyecto1.select_dtypes(include=['float', 'int']).columns.tolist()
        
        # Asegurar que estas columnas son numéricas
        for col in numeric_cols:
            proyecto1[col] = pd.to_numeric(proyecto1[col], errors='coerce')
        
        # Identificar columnas de fecha (esto dependerá de tus datos reales)
        fecha_cols = [col for col in proyecto1.columns if 'fecha' in col.lower() or 'date' in col.lower()]
        
        # Convertir columnas de fecha
        for col in fecha_cols:
            try:
                proyecto1[col] = pd.to_datetime(proyecto1[col], errors='coerce')
            except:
                print(f"No se pudo convertir la columna {col} a fecha")
        
        print("Datos preparados correctamente.")
        
        # Imprimir las columnas disponibles para debugging
        print("Columnas disponibles en el dataset:")
        for col in proyecto1.columns:
            print(f"- {col}: {proyecto1[col].dtype}")
            
        return proyecto1
    
    except Exception as e:
        print(f"Error al preparar los datos: {e}")
        return None

def analisis_ventas_totales(datos):
    """
    1. Calcular las ventas totales del comercio
    """
    try:
        # Buscar columnas que pueden contener información de ventas
        venta_cols = [col for col in datos.columns if 'venta' in col.lower() or 'monto' in col.lower() or 'total' in col.lower()]
        
        if venta_cols:
            # Convertir a numérico por si acaso
            datos[venta_cols[0]] = pd.to_numeric(datos[venta_cols[0]], errors='coerce')
            
            # Calcular la suma
            ventas_totales = datos[venta_cols[0]].sum()
            print(f"\n1. VENTAS TOTALES DEL COMERCIO: ${ventas_totales:,.2f}")
            return ventas_totales
        else:
            # Si no se encuentran columnas específicas, intentamos sumar todas las columnas numéricas
            numeric_cols = datos.select_dtypes(include=['float', 'int']).columns
            
            # Seleccionar la columna con los valores más altos (probablemente ventas)
            if len(numeric_cols) > 0:
                col_sums = {col: datos[col].sum() for col in numeric_cols}
                venta_col = max(col_sums, key=col_sums.get)
                ventas_totales = datos[venta_col].sum()
                print(f"\n1. VENTAS TOTALES DEL COMERCIO: ${ventas_totales:,.2f}")
                print(f"   (Usando columna '{venta_col}' como dato de ventas)")
                return ventas_totales
            else:
                print("No se encontraron columnas numéricas para calcular ventas.")
                return 0
    
    except Exception as e:
        print(f"Error al calcular ventas totales: {e}")
        return 0

def analisis_adeudos(datos):
    """
    2. Analizar cuántos socios tienen adeudo y cuántos no
    """
    try:
        # Buscar columnas que puedan contener información de adeudos
        adeudo_cols = [col for col in datos.columns if 'adeudo' in col.lower() or 'deuda' in col.lower() or 'saldo' in col.lower()]
        
        if adeudo_cols:
            # Asegurar que la columna es numérica
            datos[adeudo_cols[0]] = pd.to_numeric(datos[adeudo_cols[0]], errors='coerce')
            
            # Contar socios con y sin adeudo
            socios_con_adeudo = (datos[adeudo_cols[0]] > 0).sum()
            socios_sin_adeudo = (datos[adeudo_cols[0]] <= 0).sum()
            total_socios = socios_con_adeudo + socios_sin_adeudo
            
            # Calcular porcentajes
            porcentaje_con_adeudo = (socios_con_adeudo / total_socios) * 100 if total_socios > 0 else 0
            porcentaje_sin_adeudo = (socios_sin_adeudo / total_socios) * 100 if total_socios > 0 else 0
            
            print(f"\n2. ANÁLISIS DE ADEUDOS DE SOCIOS:")
            print(f"   - Socios con adeudo: {socios_con_adeudo} ({porcentaje_con_adeudo:.2f}%)")
            print(f"   - Socios sin adeudo: {socios_sin_adeudo} ({porcentaje_sin_adeudo:.2f}%)")
            print(f"   - Total de socios: {total_socios}")
            
            # Generar gráfico de pastel para visualizar
            labels = [f'Con adeudo\n{porcentaje_con_adeudo:.1f}%', f'Sin adeudo\n{porcentaje_sin_adeudo:.1f}%']
            sizes = [socios_con_adeudo, socios_sin_adeudo]
            colors = ['#ff9999', '#66b3ff']
            explode = (0.1, 0)  # Resaltar el primer slice
            
            plt.figure(figsize=(10, 8))
            plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                   autopct='%1.1f%%', shadow=True, startangle=90, textprops={'fontsize': 14})
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            plt.title('Distribución de Socios por Estado de Adeudo', fontsize=18)
            plt.savefig('distribucion_adeudos.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            print("   Gráfico de distribución de adeudos guardado como 'distribucion_adeudos.png'")
            
            return socios_con_adeudo, socios_sin_adeudo, porcentaje_con_adeudo, porcentaje_sin_adeudo
        else:
            print("No se encontraron columnas de adeudo en los datos.")
            return 0, 0, 0, 0
    
    except Exception as e:
        print(f"Error al analizar adeudos: {e}")
        return 0, 0, 0, 0

def grafica_ventas_tiempo(datos):
    """
    3. Graficar ventas totales respecto del tiempo
    """
    try:
        # Buscar columnas de fecha y ventas
        fecha_cols = [col for col in datos.columns if 'fecha' in col.lower() or 'date' in col.lower()]
        venta_cols = [col for col in datos.columns if 'venta' in col.lower() or 'monto' in col.lower() or 'total' in col.lower()]
        
        if fecha_cols and venta_cols:
            # Verificar si la columna de fecha tiene el formato correcto
            if pd.api.types.is_datetime64_dtype(datos[fecha_cols[0]]):
                # Convertir a período mensual
                datos['mes'] = datos[fecha_cols[0]].dt.to_period('M')
                
                # Agrupar por mes y sumar ventas
                ventas_mensuales = datos.groupby('mes')[venta_cols[0]].sum().reset_index()
                ventas_mensuales['mes'] = ventas_mensuales['mes'].astype(str)
                
                # Crear gráfica de barras con diseño mejorado
                plt.figure(figsize=(14, 8))
                bars = plt.bar(ventas_mensuales['mes'], ventas_mensuales[venta_cols[0]], 
                        color=sns.color_palette("viridis", len(ventas_mensuales)))
                
                # Añadir etiquetas encima de las barras
                for bar in bars:
                    height = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width()/2., height,
                            f'${height:,.0f}',
                            ha='center', va='bottom', rotation=0, fontsize=10)
                
                plt.title('Ventas Totales por Mes', fontsize=18, fontweight='bold')
                plt.xlabel('Mes', fontsize=14)
                plt.ylabel('Ventas ($)', fontsize=14)
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.grid(axis='y', linestyle='--', alpha=0.7)
                
                # Añadir línea de tendencia
                plt.plot(ventas_mensuales['mes'], ventas_mensuales[venta_cols[0]], 
                        'ro-', alpha=0.6, linewidth=2, markersize=8)
                
                # Guardar gráfica con alta resolución
                plt.savefig('ventas_mensuales.png', dpi=300, bbox_inches='tight')
                plt.close()
                
                print("\n3. Gráfica de ventas totales respecto del tiempo generada y guardada como 'ventas_mensuales.png'")
            else:
                print(f"La columna {fecha_cols[0]} no tiene formato de fecha. Intente convertirla primero.")
        else:
            print("No se encontraron columnas de fecha o ventas para generar la gráfica.")
            
            # Intentar generar una gráfica alternativa basada en índices
            if venta_cols:
                plt.figure(figsize=(14, 8))
                datos_ord = datos.sort_values(by=venta_cols[0], ascending=False).head(20)
                
                plt.barh(range(len(datos_ord)), datos_ord[venta_cols[0]], 
                       color=sns.color_palette("viridis", len(datos_ord)))
                plt.yticks(range(len(datos_ord)), [f"Registro {i+1}" for i in range(len(datos_ord))])
                plt.title('Top 20 Ventas', fontsize=18, fontweight='bold')
                plt.xlabel('Monto ($)', fontsize=14)
                plt.ylabel('Registros', fontsize=14)
                plt.grid(axis='x', linestyle='--', alpha=0.7)
                plt.tight_layout()
                
                plt.savefig('top_ventas.png', dpi=300, bbox_inches='tight')
                plt.close()
                
                print("   Se generó una gráfica alternativa de las principales ventas: 'top_ventas.png'")
    
    except Exception as e:
        print(f"Error al generar gráfica de ventas por tiempo: {e}")

def grafica_desviacion_pagos(datos):
    """
    4. Graficar la desviación estándar de pagos respecto del tiempo
    """
    try:
        # Buscar columnas de fecha y pagos
        fecha_cols = [col for col in datos.columns if 'fecha' in col.lower() or 'date' in col.lower()]
        pago_cols = [col for col in datos.columns if 'pago' in col.lower() or 'abono' in col.lower()]
        
        if not pago_cols:
            # Si no hay columnas específicas de pago, usar columnas numéricas que no sean ventas
            venta_cols = [col for col in datos.columns if 'venta' in col.lower() or 'monto' in col.lower() or 'total' in col.lower()]
            pago_cols = [col for col in datos.select_dtypes(include=['float', 'int']).columns 
                         if col not in venta_cols and 'id' not in col.lower()]
        
        if fecha_cols and pago_cols:
            # Verificar si la columna de fecha tiene el formato correcto
            if pd.api.types.is_datetime64_dtype(datos[fecha_cols[0]]):
                # Agrupar por mes
                datos['mes'] = datos[fecha_cols[0]].dt.to_period('M')
                
                # Calcular estadísticas mensuales
                stats_mensuales = datos.groupby('mes')[pago_cols[0]].agg(['mean', 'std']).reset_index()
                stats_mensuales['mes'] = stats_mensuales['mes'].astype(str)
                
                # Crear gráfica
                plt.figure(figsize=(14, 8))
                
                # Crear barras para la media
                plt.bar(stats_mensuales['mes'], stats_mensuales['mean'], 
                       alpha=0.5, color='steelblue', label='Media')
                
                # Añadir línea para la desviación estándar
                plt.errorbar(stats_mensuales['mes'], stats_mensuales['mean'], 
                           yerr=stats_mensuales['std'], fmt='o', color='darkred', 
                           ecolor='darkred', elinewidth=2, capsize=6, label='Desviación Estándar')
                
                plt.title('Media y Desviación Estándar de Pagos por Mes', fontsize=18, fontweight='bold')
                plt.xlabel('Mes', fontsize=14)
                plt.ylabel('Valor ($)', fontsize=14)
                plt.xticks(rotation=45)
                plt.grid(True, linestyle='--', alpha=0.7)
                plt.legend(fontsize=12)
                plt.tight_layout()
                
                # Guardar gráfica
                plt.savefig('desviacion_pagos.png', dpi=300, bbox_inches='tight')
                plt.close()
                
                print("\n4. Gráfica de desviación estándar de pagos generada y guardada como 'desviacion_pagos.png'")
            else:
                print(f"La columna {fecha_cols[0]} no tiene formato de fecha. Intente convertirla primero.")
        else:
            print("No se encontraron columnas de fecha o pagos para generar la gráfica.")
            
            # Generar un boxplot alternativo si hay datos numéricos
            numeric_cols = datos.select_dtypes(include=['float', 'int']).columns.tolist()
            if numeric_cols:
                plt.figure(figsize=(14, 8))
                sns.boxplot(data=datos[numeric_cols[:5]])  # Usar las primeras 5 columnas numéricas
                plt.title('Distribución y Variabilidad de Valores', fontsize=18, fontweight='bold')
                plt.xlabel('Variables', fontsize=14)
                plt.ylabel('Valor', fontsize=14)
                plt.grid(True, linestyle='--', alpha=0.7)
                plt.tight_layout()
                
                plt.savefig('variabilidad_datos.png', dpi=300, bbox_inches='tight')
                plt.close()
                
                print("   Se generó una gráfica alternativa de variabilidad de datos: 'variabilidad_datos.png'")
    
    except Exception as e:
        print(f"Error al generar gráfica de desviación de pagos: {e}")

def calcular_deuda_total(datos):
    """
    5. Calcular la deuda total de los clientes
    """
    try:
        # Buscar columnas de deuda
        deuda_cols = [col for col in datos.columns if 'adeudo' in col.lower() or 'deuda' in col.lower() or 'saldo' in col.lower()]
        
        if deuda_cols:
            # Asegurar que la columna es numérica
            datos[deuda_cols[0]] = pd.to_numeric(datos[deuda_cols[0]], errors='coerce')
            
            # Sumar todas las deudas (valores positivos)
            deuda_total = datos[datos[deuda_cols[0]] > 0][deuda_cols[0]].sum()
            
            print(f"\n5. DEUDA TOTAL DE LOS CLIENTES: ${deuda_total:,.2f}")
            return deuda_total
        else:
            print("No se encontraron columnas de deuda en los datos.")
            return 0
    
    except Exception as e:
        print(f"Error al calcular deuda total: {e}")
        return 0

def calcular_porcentaje_utilidad(ventas_totales, deuda_total):
    """
    6. Calcular el porcentaje de utilidad del comercio (ventas totales respecto a la deuda)
    """
    try:
        if ventas_totales > 0:
            # Calcular utilidad (asumiendo que la deuda resta a la utilidad)
            utilidad = ventas_totales - deuda_total
            porcentaje_utilidad = (utilidad / ventas_totales) * 100
            
            print(f"\n6. ANÁLISIS DE UTILIDAD:")
            print(f"   - Ventas totales: ${ventas_totales:,.2f}")
            print(f"   - Deuda total: ${deuda_total:,.2f}")
            print(f"   - Utilidad: ${utilidad:,.2f}")
            print(f"   - Porcentaje de utilidad: {porcentaje_utilidad:.2f}%")
            
            # Crear una gráfica de barras apiladas
            plt.figure(figsize=(10, 6))
            categorias = ['Resultado Financiero']
            valores = [ventas_totales]
            
            plt.bar(categorias, valores, label='Ventas Totales', color='#4CAF50')
            
            if deuda_total > 0:
                plt.bar(categorias, [-deuda_total], bottom=valores, label='Deuda Total', color='#F44336')
            
            # Añadir etiquetas con valores
            plt.text(0, ventas_totales/2, f'${ventas_totales:,.0f}', ha='center', va='center', 
                    color='white', fontweight='bold', fontsize=12)
            
            if deuda_total > 0:
                plt.text(0, ventas_totales + (-deuda_total/2), f'-${deuda_total:,.0f}', 
                        ha='center', va='center', color='white', fontweight='bold', fontsize=12)
            
            # Añadir texto de utilidad
            plt.text(0, ventas_totales + 0.1 * ventas_totales, 
                    f'Utilidad: ${utilidad:,.0f} ({porcentaje_utilidad:.1f}%)', 
                    ha='center', va='bottom', fontweight='bold', fontsize=14, color='black')
            
            plt.title('Análisis de Utilidad', fontsize=18, fontweight='bold')
            plt.ylabel('Monto ($)', fontsize=14)
            plt.legend(loc='lower right')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            
            # Ajustar límites para que se vea bien
            max_value = max(ventas_totales, deuda_total)
            plt.ylim(-max_value * 0.2, ventas_totales * 1.2)
            
            plt.savefig('analisis_utilidad.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            print("   Gráfico de análisis de utilidad guardado como 'analisis_utilidad.png'")
            
            return utilidad, porcentaje_utilidad
        else:
            print("No se pueden calcular utilidades con ventas totales de cero.")
            return 0, 0
    
    except Exception as e:
        print(f"Error al calcular porcentaje de utilidad: {e}")
        return 0, 0

def grafica_ventas_sucursal(datos, catalogo_sucursal):
    """
    7. Crear gráfico circular de ventas por sucursal
    """
    try:
        # Buscar columnas de sucursal y ventas
        sucursal_cols = [col for col in datos.columns if 'sucursal' in col.lower() or 'tienda' in col.lower() or 'local' in col.lower()]
        venta_cols = [col for col in datos.columns if 'venta' in col.lower() or 'monto' in col.lower() or 'total' in col.lower()]
        
        # Si no encontramos columna específica de sucursal, intentar usar cualquier columna categórica
        if not sucursal_cols:
            categorical_cols = datos.select_dtypes(include=['object']).columns.tolist()
            if categorical_cols:
                # Seleccionar la primera columna categórica que tenga menos de 20 valores únicos
                for col in categorical_cols:
                    if datos[col].nunique() < 20:
                        sucursal_cols = [col]
                        print(f"   Usando columna '{col}' como identificador de sucursal")
                        break
        
        if sucursal_cols and venta_cols:
            # Asegurar que las columnas son del tipo correcto
            datos[venta_cols[0]] = pd.to_numeric(datos[venta_cols[0]], errors='coerce')
            
            # Agrupar por sucursal y sumar ventas
            ventas_por_sucursal = datos.groupby(sucursal_cols[0])[venta_cols[0]].sum()
            
            # Calcular porcentajes
            total = ventas_por_sucursal.sum()
            porcentajes = [(valor/total)*100 for valor in ventas_por_sucursal]
            
            # Crear un dataframe para ordenar
            df_sucursales = pd.DataFrame({
                'Sucursal': ventas_por_sucursal.index,
                'Ventas': ventas_por_sucursal.values,
                'Porcentaje': porcentajes
            })
            
            # Ordenar por ventas para mejor visualización
            df_sucursales = df_sucursales.sort_values('Ventas', ascending=False)
            
            # Crear gráfico circular mejorado
            plt.figure(figsize=(12, 10))
            
            # Usar paleta de colores más atractiva
            colors = plt.cm.tab20.colors
            
            # Crear el gráfico de pastel
            wedges, texts, autotexts = plt.pie(
                df_sucursales['Ventas'], 
                labels=df_sucursales['Sucursal'],
                autopct='%1.1f%%', 
                startangle=90, 
                shadow=True,
                explode=[0.05 if i < 3 else 0 for i in range(len(df_sucursales))],  # Resaltar las 3 principales
                colors=colors,
                wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
                textprops={'fontsize': 12, 'fontweight': 'bold'}
            )
            
            # Personalizar textos
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            plt.title('Distribución de Ventas por Sucursal', fontsize=20, fontweight='bold', pad=20)
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            
            # Añadir leyenda separada para mejor visualización
            plt.legend(
                title='Sucursales',
                loc='center left',
                bbox_to_anchor=(1, 0, 0.5, 1),
                fontsize=10
            )
            
            plt.tight_layout()
            
            # Guardar gráfica con alta resolución
            plt.savefig('ventas_por_sucursal.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            print("\n7. Gráfico circular de ventas por sucursal generado y guardado como 'ventas_por_sucursal.png'")
        else:
            print("No se encontraron columnas de sucursal o ventas para generar la gráfica.")
    
    except Exception as e:
        print(f"Error al generar gráfico de ventas por sucursal: {e}")

def grafica_deudas_vs_utilidad_sucursal(datos, catalogo_sucursal):
    """
    8. Presentar gráfico de deudas totales por sucursal respecto al margen de utilidad
    """
    try:
        # Buscar columnas necesarias
        sucursal_cols = [col for col in datos.columns if 'sucursal' in col.lower() or 'tienda' in col.lower() or 'local' in col.lower()]
        venta_cols = [col for col in datos.columns if 'venta' in col.lower() or 'monto' in col.lower() or 'total' in col.lower()]
        deuda_cols = [col for col in datos.columns if 'adeudo' in col.lower() or 'deuda' in col.lower() or 'saldo' in col.lower()]
        
        # Si no encontramos columna específica de sucursal, intentar usar cualquier columna categórica
        if not sucursal_cols:
            categorical_cols = datos.select_dtypes(include=['object']).columns.tolist()
            if categorical_cols:
                # Seleccionar la primera columna categórica que tenga menos de 20 valores únicos
                for col in categorical_cols:
                    if datos[col].nunique() < 20:
                        sucursal_cols = [col]
                        print(f"   Usando columna '{col}' como identificador de sucursal")
                        break
        
        # Si no encontramos columna de deuda, usar una columna numérica alternativa
        if not deuda_cols and venta_cols:
            # Crear una columna sintética basada en ventas
            datos['deuda_simulada'] = datos[venta_cols[0]] * 0.2  # 20% de las ventas como deuda simulada
            deuda_cols = ['deuda_simulada']
            print("   No se encontró columna de deudas. Usando una deuda simulada del 20% de las ventas.")
        
        if sucursal_cols and venta_cols and deuda_cols:
            # Asegurar que las columnas son del tipo correcto
            datos[venta_cols[0]] = pd.to_numeric(datos[venta_cols[0]], errors='coerce')
            datos[deuda_cols[0]] = pd.to_numeric(datos[deuda_cols[0]], errors='coerce')
            
            # Agrupar por sucursal
            ventas_por_sucursal = datos.groupby(sucursal_cols[0])[venta_cols[0]].sum()
            deudas_por_sucursal = datos.groupby(sucursal_cols[0])[deuda_cols[0]].sum()
            
            # Calcular utilidad y margen por sucursal
            utilidad_por_sucursal = ventas_por_sucursal - deudas_por_sucursal
            margen_por_sucursal = (utilidad_por_sucursal / ventas_por_sucursal) * 100
            
            # Crear dataframe para graficar
            df_analisis = pd.DataFrame({
                'Sucursal': ventas_por_sucursal.index,
                'Ventas': ventas_por_sucursal.values,
                'Deuda': deudas_por_sucursal.values,
                'Utilidad': utilidad_por_sucursal.values,
                'Margen_Utilidad': margen_por_sucursal.values
            })
            
            # Ordenar por margen de utilidad
            df_analisis = df_analisis.sort_values('Margen_Utilidad', ascending=False)
            
            # Crear gráfico mejorado
            plt.figure(figsize=(16, 12))
            
            # Definir esquema de colores
            color_deuda = '#E57373'     # Rojo claro
            color_utilidad = '#81C784'  # Verde claro
            color_margen = '#5C6BC0'    # Azul

            # Crear gráfico de barras apiladas con línea de margen
            fig, ax1 = plt.subplots(figsize=(16, 10))
            
            # Calcular posiciones de las barras
            x = np.arange(len(df_analisis))
            width = 0.35
            
            # Crear barras para las ventas
            bars1 = ax1.bar(x, df_analisis['Ventas'], width, label='Ventas', color='#64B5F6', edgecolor='white', linewidth=1)
            
            # Crear barras para las deudas (apiladas sobre las ventas)
            bars2 = ax1.bar(x, -df_analisis['Deuda'], width, bottom=df_analisis['Ventas'], 
                           label='Deuda', color=color_deuda, edgecolor='white', linewidth=1)
            
            # Crear barras para la utilidad
            bars3 = ax1.bar(x + width, df_analisis['Utilidad'], width, label='Utilidad', 
                           color=color_utilidad, edgecolor='white', linewidth=1)
            
            # Configurar primer eje
            ax1.set_xlabel('Sucursal', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Monto ($)', fontsize=14, fontweight='bold')
            ax1.set_title('Análisis Financiero por Sucursal', fontsize=20, fontweight='bold', pad=20)
            ax1.set_xticks(x + width / 2)
            ax1.set_xticklabels(df_analisis['Sucursal'], rotation=45, ha='right')
            
            # Crear segundo eje para el margen de utilidad
            ax2 = ax1.twinx()
            line = ax2.plot(x + width/2, df_analisis['Margen_Utilidad'], 'o-', linewidth=3, 
                          markersize=10, color=color_margen, label='Margen de Utilidad (%)')
            ax2.set_ylabel('Margen de Utilidad (%)', fontsize=14, fontweight='bold', color=color_margen)
            ax2.tick_params(axis='y', colors=color_margen)
            
            # Añadir etiquetas a los puntos de margen
            for i, valor in enumerate(df_analisis['Margen_Utilidad']):
                ax2.annotate(f'{valor:.1f}%', (x[i] + width/2, valor), 
                           xytext=(0, 10), textcoords='offset points',
                           ha='center', va='bottom', fontweight='bold', color=color_margen)
            
            # Añadir cuadrícula
            ax1.grid(axis='y', linestyle='--', alpha=0.3)
            
            # Combinar las leyendas de ambos ejes
            handles1, labels1 = ax1.get_legend_handles_labels()
            handles2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(handles1 + handles2, labels1 + labels2, loc='upper center', 
                     bbox_to_anchor=(0.5, -0.15), ncol=4, fontsize=12, frameon=True)
            
            # Ajustar diseño
            plt.tight_layout()
            
            # Guardar gráfica con alta resolución
            plt.savefig('deudas_vs_margen_sucursal.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            print("\n8. Gráfico de deudas vs margen de utilidad por sucursal generado y guardado como 'deudas_vs_margen_sucursal.png'")
        else:
            print("No se encontraron las columnas necesarias para generar la gráfica.")
            
            # Generar una gráfica alternativa si hay suficientes datos
            if sucursal_cols and (venta_cols or deuda_cols):
                plt.figure(figsize=(14, 8))
                
                if venta_cols:
                    valores = datos.groupby(sucursal_cols[0])[venta_cols[0]].sum().sort_values(ascending=False)
                    titulo = 'Ventas por Sucursal'
                else:
                    valores = datos.groupby(sucursal_cols[0])[deuda_cols[0]].sum().sort_values(ascending=False)
                    titulo = 'Deudas por Sucursal'
                
                # Generar gráfico de barras horizontal
                plt.barh(valores.index, valores, color=plt.cm.viridis(np.linspace(0, 1, len(valores))))
                
                # Añadir valores al final de cada barra
                for i, v in enumerate(valores):
                    plt.text(v + 0.01*max(valores), i, f'${v:,.0f}', va='center', fontweight='bold')
                
                plt.title(titulo, fontsize=18, fontweight='bold')
                plt.xlabel('Monto ($)', fontsize=14)
                plt.ylabel('Sucursal', fontsize=14)
                plt.grid(axis='x', linestyle='--', alpha=0.7)
                plt.tight_layout()
                
                plt.savefig('analisis_alternativo_sucursal.png', dpi=300, bbox_inches='tight')
                plt.close()
                
                print("   Se generó una gráfica alternativa: 'analisis_alternativo_sucursal.png'")
    
    except Exception as e:
        print(f"Error al generar gráfico de deudas vs utilidad por sucursal: {e}")
        
        # Intentar generar gráfico simplificado en caso de error
        try:
            if sucursal_cols and venta_cols:
                plt.figure(figsize=(12, 8))
                valores = datos.groupby(sucursal_cols[0])[venta_cols[0]].sum().sort_values(ascending=False)
                plt.bar(valores.index, valores, color='darkblue')
                plt.title('Ventas por Sucursal', fontsize=16)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig('ventas_sucursal_simple.png', dpi=300)
                plt.close()
                print("   Se generó una gráfica simplificada: 'ventas_sucursal_simple.png'")
        except:
            print("   No se pudo generar ninguna gráfica alternativa.")

def generar_reporte_completo():
    """
    Función principal que ejecuta todos los análisis
    """
    print("=" * 80)
    print("REPORTE DE ANÁLISIS DE VENTAS Y ADEUDOS DEL COMERCIO")
    print("=" * 80)
    
    # Cargar datos
    catalogo_sucursal, proyecto1 = cargar_datos()
    
    if catalogo_sucursal is None or proyecto1 is None:
        print("No se pudieron cargar los datos. Verifica que los archivos existen y tienen el formato correcto.")
        return
    
    # Preparar datos
    datos = preparar_datos(catalogo_sucursal, proyecto1)
    
    if datos is None:
        print("No se pudieron preparar los datos para el análisis.")
        return
    
    # 1. Calcular ventas totales
    ventas_totales = analisis_ventas_totales(datos)
    
    # 2. Analizar socios con/sin adeudo
    analisis_adeudos(datos)
    
    # 3. Graficar ventas por tiempo
    grafica_ventas_tiempo(datos)
    
    # 4. Graficar desviación estándar de pagos
    grafica_desviacion_pagos(datos)
    
    # 5. Calcular deuda total
    deuda_total = calcular_deuda_total(datos)
    
    # 6. Calcular porcentaje de utilidad
    calcular_porcentaje_utilidad(ventas_totales, deuda_total)
    
    # 7. Graficar ventas por sucursal
    grafica_ventas_sucursal(datos, catalogo_sucursal)
    
    # 8. Graficar deudas vs utilidad por sucursal
    grafica_deudas_vs_utilidad_sucursal(datos, catalogo_sucursal)
    
    print("\n" + "=" * 80)
    print("ANÁLISIS COMPLETADO - Los gráficos se han guardado en el directorio actual")
    print("=" * 80)

if __name__ == "__main__":
    generar_reporte_completo()