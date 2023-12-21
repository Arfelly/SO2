import os
from datetime import datetime
import matplotlib.pyplot as plt

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
        nombre_archivo_salida = f'Datos_Procesados_{nombre_serial}.txt'
        ruta_archivo_salida = os.path.join(ruta_salida, nombre_archivo_salida)

        with open(ruta_archivo_salida, 'w') as file_salida:
            file_salida.write("tiempo\tflujoKgs\tfluxTond\n")

            for linea in datos_totales:
                fecha_hora = f"{linea[0]} {linea[1]}"
                combined_datetime = datetime.strptime(fecha_hora, '%Y-%m-%d %H:%M:%S')
                flux_ton_dias = '{:.2f}'.format(float(linea[2]) * 952397)
                file_salida.write(f"{linea[0]}\t{linea[1]}\t{linea[2]}\t{flux_ton_dias}\n")

        print(f'Datos consolidados guardados en: {ruta_archivo_salida}')
        return ruta_archivo_salida
    else:
        print(f'No se encontraron datos para {nombre_serial}')
        return None

def graficar_datos(datos, ruta_grafica, fecha_inicio=None, fecha_fin=None):
    if fecha_inicio and fecha_fin:
        datos = [linea for linea in datos if fecha_inicio <= linea[0] <= fecha_fin]

    fechas_hora = [f"{linea[0]} {linea[1]}" for linea in datos]
    flux_values = [float(linea[2]) for linea in datos]
    flux_ton_dias = [float(linea[3]) for linea in datos]

    fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    fig.suptitle(f'Gráfico {datos[0][2]} SO2')

    # Gráfico de Fecha vs Flux[Kg/s]
    axs[0].plot(fechas_hora, flux_values, marker='o', linestyle='-', label='Flux[Kg/s]')
    axs[0].set_ylabel('Flux[Kg/s]')
    axs[0].grid(True)
    axs[0].legend()

    # Gráfico de Fecha vs Flux[Ton/d]
    axs[1].plot(fechas_hora, flux_ton_dias, marker='o', linestyle='-', label='Flux[Kg/s] * 952397')
    axs[1].set_ylabel('Flux[Kg/s] * 952397')
    axs[1].set_xlabel('Fecha y Hora')
    axs[1].grid(True)
    axs[1].legend()

    axs[0].xaxis.set_major_locator(plt.MaxNLocator(10))
    axs[0].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')))
    
    # Guarda la gráfica
    nombre_grafica = f'Grafica_{datos[0][2]}_SO2.png'
    ruta_grafica = os.path.join(ruta_grafica, nombre_grafica)
    plt.savefig(ruta_grafica, bbox_inches='tight')
    print(f'Gráfica guardada en: {ruta_grafica}')
    plt.show()


if __name__ == "__main__":
    ruta_base = input("Ingrese la ruta del directorio base (por ejemplo, Pruebas/): ")
    nombre_serial = "FluxLog_2011050M1_"
    ruta_salida = input("Ingrese la ruta de salida para los datos consolidados: ")

    ruta_grafica = os.path.join(ruta_salida, 'Graficos')
    os.makedirs(ruta_grafica, exist_ok=True)

    # Procesar carpeta serial y guardar datos consolidados
    datos_consolidados = procesar_carpeta_serial(ruta_base, nombre_serial, ruta_salida)

    if datos_consolidados:
        # Graficar datos
        opcion_graficar = input("¿Desea graficar los datos? (Sí/No): ").lower()
        
        if opcion_graficar == 'sí' or opcion_graficar == 'si':
            opcion_rango_fechas = input("¿Quiere graficar por rango de fechas? (Sí/No): ").lower()

            if opcion_rango_fechas == 'sí' or opcion_rango_fechas == 'si':
                fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
                fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")
                graficar_datos(datos_consolidados, ruta_grafica, fecha_inicio, fecha_fin)
            else:
                graficar_datos(datos_consolidados, ruta_grafica)