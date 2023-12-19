import os
import shutil

def buscar_y_copiar_archivos(ruta_origen, patron_archivo, ruta_destino):
    for directorio_actual, carpetas, archivos in os.walk(ruta_origen):
        for archivo in archivos:
            if archivo.startswith(patron_archivo) and archivo.endswith('.txt'):
                # Encuentra un archivo con el patrón deseado
                ruta_origen_archivo = os.path.join(directorio_actual, archivo)
                ruta_destino_archivo = os.path.join(ruta_destino, archivo)
                shutil.copy2(ruta_origen_archivo, ruta_destino_archivo)
                print(f"Se ha copiado {archivo} a {ruta_destino}")

if __name__ == "__main__":
    # Solicitar la ruta del directorio
    ruta_origen = input("Ingrese la ruta del directorio: ")

    # Patrón de archivo
    patron_archivo = "FluxLog_2011050M1_"

    # Solicitar la ruta de destino
    ruta_destino = input("Ingrese la ruta de destino: ")

    buscar_y_copiar_archivos(ruta_origen, patron_archivo, ruta_destino)


