import os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter

def leer_archivo_fluxlog(ruta_archivo):
    # Lee el archivo FluxLog y retorna una lista de listas con las columnas deseadas
    with open(ruta_archivo, 'r') as file:
        lines = [line.strip().split('\t') for line in file]

    return [[line[0], line[1], line[3]] for line in lines[5:] if line[3] != '0.00']


def procesar_carpeta_serial(ruta_base, nombre_serial, ruta_salida):
    datos_totales = []

    for ruta_serial_carpeta, carpetas, archivos in os.walk(ruta_base):
        for archivo_fluxlog in archivos:
            if archivo_fluxlog.startswith(nombre_serial) and archivo_fluxlog.endswith('.txt'):
                ruta_archivo_fluxlog = os.path.join(ruta_serial_carpeta, archivo_fluxlog)
                datos_totales.extend(leer_archivo_fluxlog(ruta_archivo_fluxlog))

    # Verifica si hay datos y realiza los cálculos
    if datos_totales:
        datos_totales.sort(key=lambda x: (x[0], x[1]))  # Ordena por Fecha y Hora

        # Guarda el archivo consolidado
        nombre_archivo_salida = f'Datos_Vinagre3.txt'
        ruta_archivo_salida = os.path.join(ruta_salida, nombre_archivo_salida)

        with open(ruta_archivo_salida, 'w') as file_salida:
            file_salida.write("tiempo\tflujoKgs\tflujoTond\n")

            for linea in datos_totales:
                Fecha_H = f"{linea[0]} {linea[1]}"
                tiempo = datetime.strptime(Fecha_H, '%Y-%m-%d %H:%M:%S')
                flux_ton_dias = '{:.2f}'.format(float(linea[2]) * 952397)
                file_salida.write(f"{tiempo}\t{linea[2]}\t{flux_ton_dias}\n")

        print(f'Datos consolidados guardados en: {ruta_archivo_salida}')
        return ruta_archivo_salida
    else:
        print(f'No se encontraron datos para {nombre_serial}')
        return None

def cargar_archivos_consolidados(archivos_consolidados):

    with open(archivos_consolidados, 'r') as fila:
        next(fila)

        data = [line.strip().split('\t') for line in fila]
        tiempo = [datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") for row in data]
        flujoKgs = [float(row[1]) for row in data]
        flujoTond = [float(row[2]) for row in data]
    
    return tiempo, flujoKgs, flujoTond

def calcular_promedio_movil(datos, ventana=24):
    return np.convolve(datos, np.ones(ventana) / ventana, mode='valid')

def configurar_grafico(ax, fechas, datos, nombre, color):
    ax.plot(fechas, datos, marker='o', linestyle='-', markersize=3, label=nombre, color=color, alpha=0.5)

def configurar_ticks_y_formato_fecha(axs, fechas, ticks_cada_n=30):
    for ax in axs:
        ax.set_xticks(fechas[::ticks_cada_n])
        ax.xaxis.set_major_formatter(DateFormatter('%d-%b'))

def dibujar_linea_punteada(ax, fechas, promedio_movil, alpha=0.5):
    ax.plot(fechas, [np.nan]*23 + promedio_movil.tolist(), 'r--', alpha=alpha)

def graficar_desde_txt(archivo, ruta_archivo_salida):
    ruta_archivo = os.path.join(ruta_archivo_salida, archivo)
    tiempo, flujoKgs, flujoTond = cargar_archivos_consolidados(ruta_archivo)

    if tiempo:  # Verificar si se cargaron fechas correctamente
        promedio_flujoKgs = calcular_promedio_movil(flujoKgs)
        promedio_flujoTond = calcular_promedio_movil(flujoTond)
        
        carpeta_salida = f'Graficos_SO2'
        directorio_salida = os.path.join(ruta_salida, carpeta_salida)
        os.makedirs(directorio_salida, exist_ok=True)

        fig, axs = plt.subplots(2, 1, figsize=(8, 7), sharex=False)
        fig.suptitle(f'Vinagre3', y=0.92)
        
        
        configurar_grafico(axs[0], tiempo, flujoKgs, 'Flujo Kg/s', (0,0,153/255))
        configurar_grafico(axs[1], tiempo, flujoTond, 'Flujo Ton/días', (0,153/255,0))

        #for ax in axs:
        #    ax.set_xticks(ax.get_xticks())
        #    ax.set_xticklabels(ax.get_xticklabels(), rotation=20)

        configurar_ticks_y_formato_fecha(axs, tiempo)
        dibujar_linea_punteada(axs[0], tiempo, promedio_flujoKgs)
        dibujar_linea_punteada(axs[1], tiempo, promedio_flujoTond)

        maximos_diarios_Kgs = [max(flujoKgs[i:i+31]) for i in range(0, len(flujoKgs), 31)]
        maximos_diarios_Tond = [max(flujoTond[i:i+31]) for i in range(0, len(flujoTond), 31)]

        axs[0].plot(tiempo[::31], maximos_diarios_Kgs, 'k--', alpha=0.3, label='Máx. diario Kg/s')
        axs[1].plot(tiempo[::31], maximos_diarios_Tond, label='Máx. diario Ton/días')

        # Anotar los valores máximos con inclinación de 20 grados
        for i, fecha in enumerate(tiempo[::31]):
            axs[0].annotate(f'{maximos_diarios_Kgs[i]:.2f}',
                            (fecha, maximos_diarios_Kgs[i]),
                            textcoords="offset points",
                            xytext=(10, 10),
                            ha='center',
                            fontsize=8,
                            )
            
            axs[1].annotate(f'{maximos_diarios_Tond[i]:.2e}',
                            (fecha, maximos_diarios_Tond[i]),
                            textcoords="offset points",
                            xytext=(10, 10),
                            ha='center',
                            fontsize=8,
                            )

        # Crear el nombre del archivo de salida
        nombre_archivo_salida = f'gráfico_Vinagre3.png'
        ruta_guardado = os.path.join(directorio_salida, nombre_archivo_salida)
        plt.savefig(ruta_guardado, bbox_inches='tight', dpi=300)
        
        plt.close()

if __name__ == "__main__":
    ruta_base = input("Ingrese la ruta del directorio base (por ejemplo, Pruebas/): ")
    nombre_serial = "FluxLog_2011050M1_"
    ruta_salida = input("Ingrese la ruta de salida para los datos consolidados: ")

    # Procesar carpeta serial y guardar datos consolidados
    datos_consolidados = procesar_carpeta_serial(ruta_base, nombre_serial, ruta_salida)

    graficar_desde_txt(datos_consolidados, ruta_salida)

    #if datos_consolidados:
    #    # Graficar datos
    #    opcion_graficar = input("¿Desea graficar los datos? (Sí/No): ").lower()
#
    #    graficar_desde_txt(datos_consolidados, ruta_salida)
#
    #    if opcion_graficar == 'sí' or opcion_graficar == 'si':
    #        opcion_rango_fechas = input("¿Quiere graficar por rango de fechas? (Sí/No): ").lower()
#
    #        if opcion_rango_fechas == 'sí' or opcion_rango_fechas == 'si':
    #            fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
    #            fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")
    #            graficar_desde_txt(datos_consolidados, ruta_salida, fecha_inicio, fecha_fin)
    #        else:
    #            graficar_desde_txt(datos_consolidados, ruta_salida)