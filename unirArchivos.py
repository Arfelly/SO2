import os

def consolidar_archivos_txt(ruta_origen, archivo_destino):
    # Encabezado que se agregará al archivo consolidado
    encabezado = "scandate\tscanstarttime\tscanstoptime\tflux_[kg/s]\twindspeed_[m/s]\twinddirection_[deg]\twindspeedsource\twinddirectionsource\tplumeheight_[m]\tplumeheightsource\tcompassdirection_[deg]\tcompasssource\tplumecentre_[deg]\tplumeedge1_[deg]\tplumeedge2_[deg]\tplumecompleteness_[%]\tconeangle\ttilt\tokflux\ttemperature\tbatteryvoltage\texposuretime\n"

    # Lista para almacenar los datos consolidados
    datos_totales = []

    # Iterar sobre los archivos en la carpeta
    for archivo in os.listdir(ruta_origen):
        if archivo.endswith('.txt'):
            ruta_archivo = os.path.join(ruta_origen, archivo)
            with open(ruta_archivo, 'r') as f:
                # Leer todas las líneas desde la fila 5
                lineas = f.readlines()[4:]
                # Agregar los datos al conjunto total
                datos_totales.extend(lineas)

    # Escribir los datos consolidados en el archivo destino
    with open(archivo_destino, 'w') as f_destino:
        # Agregar el encabezado
        f_destino.write(encabezado)
        # Agregar los datos
        f_destino.writelines(datos_totales)

if __name__ == "__main__":
    # Solicitar la ruta del directorio
    ruta_origen = input("Ingrese la ruta del directorio que contiene los archivos .txt: ")

    # Solicitar el nombre del archivo de destino
    archivo_destino = 'datosSO2.txt'

    # Construir la ruta completa del archivo de destino
    ruta_destino = os.path.join(ruta_origen, archivo_destino)

    consolidar_archivos_txt(ruta_origen, ruta_destino)
    print(f"Se han consolidado los archivos en {ruta_destino}.")
