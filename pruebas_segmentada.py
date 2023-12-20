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
        nombre_archivo_salida = f'Datos_Procesados_Vinagre3.txt'
        ruta_archivo_salida = os.path.join(ruta_salida, nombre_archivo_salida)

        with open(ruta_archivo_salida, 'w') as file_salida:
            file_salida.write("Fecha\tHora\tFlux[Kg/s]\tFlux[Ton/d]\n")

            for linea in datos_totales:
                fecha_hora = f"{linea[0]} {linea[1]}"
                combined_datetime = datetime.strptime(fecha_hora, '%Y-%m-%d %H:%M:%S')
                flux_ton_dias = '{:.2f}'.format(float(linea[2]) * 952397)
                file_salida.write(f"{linea[0]} {linea[1]}\t{linea[2]}\t{flux_ton_dias}\n")

        print(f'Datos consolidados guardados en: {ruta_archivo_salida}')
        return ruta_archivo_salida
    else:
        print(f'No se encontraron datos para {nombre_serial}')
        return None

if __name__ == "__main__":
    ruta_base = input("Ingrese la ruta del directorio base (por ejemplo, Pruebas/): ")
    nombre_serial = "FluxLog_2011050M1_"
    ruta_salida = input("Ingrese la ruta de salida para los datos consolidados: ")

    ruta_grafica = os.path.join(ruta_salida, 'Graficos')
    os.makedirs(ruta_grafica, exist_ok=True)

    # Procesar carpeta serial y guardar datos consolidados
    datos_consolidados = procesar_carpeta_serial(ruta_base, nombre_serial, ruta_salida)