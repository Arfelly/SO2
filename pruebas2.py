import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def leer_archivos_fluxlog(ruta):
    datos_totales = []
    for root, dirs, files in os.walk(ruta):
        for dir in dirs:
            if dir.startswith("2011050M1"):
                serial = "Vinagre3"
            elif dir.startswith("I2J7739"):
                serial = "Vinagre2"
            else:
                continue

            carpeta_serial = os.path.join(root, dir)
            for file in os.listdir(carpeta_serial):
                if file.startswith("FluxLog") and file.endswith('.txt'):
                    ruta_archivo = os.path.join(carpeta_serial, file)
                    with open(ruta_archivo, 'r') as f:
                        lines = f.readlines()[4:]
                        datos_totales.extend(lines)
    return datos_totales, serial

def escribir_archivo_consolidado(datos, nombre_archivo):
    encabezado = "Fecha\tHora\tFlux[Kg/s]\tFlux_multiplicado\n"
    with open(nombre_archivo, 'w') as f_destino:
        f_destino.write(encabezado)
        for line in datos:
            f_destino.write(line)

def procesar_archivo_consolidado(nombre_archivo):
    with open(nombre_archivo, 'r') as file:
        lines = [line.strip().split('\t') for line in file][1:]  # Excluye el encabezado

    lines[0].append('Fecha_Hora')
    for line in lines[1:]:
        date_time_str = f"{line[0]} {line[1]}"
        combined_datetime = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
        line.append(combined_datetime.strftime('%Y-%m-%d %H:%M:%S'))

    for line in lines:
        last_col = line[-1]
        del line[-1]
        line.insert(0, last_col)

    lines = sorted(lines[1:], key=lambda x: datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S'))

    with open(nombre_archivo, 'w') as file:
        for line in lines:
            file.write('\t'.join(line) + '\n')
'''
def filtrar_cero_y_multiplicar(datos, nombre_archivo):
    datos_filtrados = [line.split('\t') for line in datos]
    datos_filtrados = [[date, time, flux, str(float(flux) * 952397)] for date, time, flux in datos_filtrados if float(flux) != 0]
    datos_filtrados.insert(0, ['Fecha', 'Hora', 'Flux[Kg/s]', 'Flux_multiplicado'])

    with open(nombre_archivo, 'w') as f_destino:
        for line in datos_filtrados:
            f_destino.write('\t'.join(line) + '\n')

def graficar_datos(nombre_archivo, mostrar_rangos=False, fecha_inicio=None, fecha_fin=None):
    with open(nombre_archivo, 'r') as file:
        lines = [line.strip().split('\t') for line in file][1:]  # Excluye el encabezado

    if mostrar_rangos:
        fecha_inicio = datetime.strptime(fecha_inicio, '%d-%m-%y')
        fecha_fin = datetime.strptime(fecha_fin, '%d-%m-%y')
        lines = [line for line in lines if fecha_inicio <= datetime.strptime(line[0], '%Y-%m-%d') <= fecha_fin]

    fechas = [datetime.strptime(line[0], '%Y-%m-%d') for line in lines]
    flux_values = [float(line[2]) for line in lines]
    flux_multi_values = [float(line[3]) for line in lines]

    fig, axs = plt.subplots(2, 1, figsize=(10, 12), sharex=False)
    fig.suptitle(f'Grafica_SO2', y=0.92)

    axs[0].plot(fechas, flux_values, marker='o', linestyle='-', label='Flux[Kg/s]')
    axs[0].set_ylabel('Flux[Kg/s]')

    axs[1].plot(fechas, flux_multi_values, marker='o', linestyle='-', color='orange', label='Flux_multiplicado')
    axs[1].set_ylabel('Flux_multiplicado')

    axs[1].set_xlabel('Fecha')
    axs[1].xaxis.set_major_locator(plt.MaxNLocator(nbins=20))
    axs[1].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: fechas[int(x)].strftime('%d/%m/%Y')))

    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(f'Grafica_SO2_{fecha_inicio.strftime("%Y%m%d")}_{fecha_fin.strftime("%Y%m%d")}.png', bbox_inches='tight')
    plt.show()
'''
def main():
    ruta = input("Ingrese la ruta del directorio: ")
    #serial = input("Ingrese el serial a escoger (Vinagre3 o Vinagre2): ")
    nombre_archivo = input("Ingrese el nombre del archivo a guardar: ")


    datos, serial = leer_archivos_fluxlog(ruta)
    escribir_archivo_consolidado(datos, nombre_archivo)

    procesar_archivo_consolidado(nombre_archivo)

    '''filtrar_cero_y_multiplicar(datos, nombre_archivo)

    print(f"Se han consolidado y filtrado los archivos en {nombre_archivo}.")

    graficar = input("¿Desea graficar por rangos? (Sí/No): ").lower()
    if graficar == 'sí' or graficar == 'si':
        fecha_inicio = input("Ingrese la fecha de inicio (dd-mm-yy): ")
        fecha_fin = input("Ingrese la fecha de fin (dd-mm-yy): ")
        graficar_datos(nombre_archivo, True, fecha_inicio, fecha_fin)
    else:
        graficar_datos(nombre_archivo)'''

if __name__ == "__main__":
    main()
