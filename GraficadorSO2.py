import os
from datetime import datetime

# Ruta del archivo original
datos_so2 = input('Ingrese la ruta de los datos de SO2.txt: ') + '\datosSO2.txt'

# Lee el archivo .txt y obtén las líneas
with open(datos_so2, 'r') as file:
    lines = [line.strip().split('\t') for line in file]

# Añade un encabezado a la primera línea
lines[0].append('combined_datetime_formatted')

# Combina las columnas scandate y scanstarttime, elimina las columnas originales y agrega la nueva columna
for line in lines[1:]:
    date_time_str = f"{line[0]} {line[1]}"
    combined_datetime = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    line.append(combined_datetime.strftime('%Y-%m-%d %H:%M:%S'))

# Mueve la última columna a la posición 1
for line in lines:
    last_col = line[-1]
    del line[-1]
    line.insert(0, last_col)

# Ordena las líneas por la columna 'combined_datetime_formatted'
lines = sorted(lines[1:], key=lambda x: datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S'))

# Inserta la primera línea (encabezado) de nuevo
lines.insert(0, ['combined_datetime_formatted', 'scandate', 'scanstarttime', 'scanstoptime', 'flux_[kg/s]', 'windspeed_[m/s]', 'winddirection_[deg]', 'windspeedsource', 'winddirectionsource', 'plumeheight_[m]', 'plumeheightsource', 'compassdirection_[deg]', 'compasssource', 'plumecentre_[deg]', 'plumeedge1_[deg]', 'plumeedge2_[deg]', 'plumecompleteness_[%]', 'coneangle', 'tilt', 'okflux', 'temperature', 'batteryvoltage', 'exposuretime'])

# Ruta del nuevo archivo
ruta_nuevo_archivo = os.path.splitext(datos_so2)[0] + '_modificado.txt'

# Guarda las líneas modificadas en un nuevo archivo .txt
with open(ruta_nuevo_archivo, 'w') as file:
    for line in lines:
        file.write('\t'.join(line) + '\n')


import matplotlib.pyplot as plt
import datetime

# Ruta del archivo original
archivo_graficar = ruta_nuevo_archivo

# Lee el archivo .txt
with open(archivo_graficar, 'r') as file:
    lines = [line.strip().split('\t') for line in file]

# Pide al usuario las fechas de inicio y final
fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ") + ' 12:00:00'
fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ") + ' 23:00:00'

# Obtiene índices de las columnas
header = lines[0]
combined_datetime_index = header.index('combined_datetime_formatted')
flux_index = header.index('flux_[kg/s]')

# Filtra las líneas que estén dentro del rango de fechas proporcionado por el usuario

filtered_lines = [line for line in lines[1:] if fecha_inicio <= line[combined_datetime_index] <= fecha_fin]

# Extrae datos relevantes para el gráfico del rango seleccionado
dates = [datetime.datetime.strptime(line[combined_datetime_index], '%Y-%m-%d %H:%M:%S') for line in filtered_lines]
flux_values = [float(line[flux_index]) for line in filtered_lines]

# Grafica la columna combined_datetime_formatted y flux_[kg/s]
plt.figure(figsize=(10, 6))
plt.plot(dates, flux_values, marker='o', linestyle='-')
plt.title('Flujo en función de la fecha y hora')
plt.xlabel('Fecha y Hora')
plt.ylabel('Flujo [kg/s]')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Muestra la gráfica
plt.show()



##    import matplotlib.pyplot as plt
##    import datetime
##    import pandas as pd
##    
##    # Ruta del archivo original
##    archivo_graficar = ruta_nuevo_archivo
##    
##    # Lee el archivo .txt
##    with open(archivo_graficar, 'r') as file:
##        lines = [line.strip().split('\t') for line in file]
##    
##    # Pide al usuario las fechas de inicio y final
##    fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ") + ' 12:00:00'
##    fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ") + ' 23:00:00'
##    
##    # Obtiene índices de las columnas
##    header = lines[0]
##    combined_datetime_index = header.index('combined_datetime_formatted')
##    flux_index = header.index('flux_[kg/s]')
##    
##    # Filtra las líneas que estén dentro del rango de fechas proporcionado por el usuario
##    filtered_lines = [line for line in lines[1:] if fecha_inicio <= line[combined_datetime_index] <= fecha_fin]
##    
##    # Extrae datos relevantes para el gráfico del rango seleccionado
##    dates = [datetime.datetime.strptime(line[combined_datetime_index], '%Y-%m-%d %H:%M:%S') for line in filtered_lines]
##    flux_values = [float(line[flux_index]) for line in filtered_lines]
##    
##    # Calcula los valores máximos de flujo para cada día
##    df = pd.DataFrame({'Fecha': dates, 'Flujo': flux_values})
##    df['Fecha'] = pd.to_datetime(df['Fecha'])
##    df_diario_max = df.groupby(df['Fecha'].dt.date)['Flujo'].max().reset_index()
##    
##    # Grafica la columna combined_datetime_formatted y flux_[kg/s]
##    plt.figure(figsize=(10, 6))
##    
##    # Grafica la serie temporal
##    plt.plot(dates, flux_values, label='Flujo Diario', marker='o', linestyle='-')
##    
##    # Grafica los valores máximos de flujo para cada día
##    plt.scatter(df_diario_max['Fecha'], df_diario_max['Flujo'], color='red', label='Máximo diario', marker='x')
##    
##    plt.title('Flujo en función de la fecha y hora con Máximos Diarios')
##    plt.xlabel('Fecha y Hora')
##    plt.ylabel('Flujo [kg/s]')
##    plt.xticks(rotation=45)
##    plt.legend()
##    plt.grid(True)
##    plt.tight_layout()
##    
##    # Muestra la gráfica
##    plt.show()