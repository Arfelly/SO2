import subprocess

# Nombre del archivo .bat que deseas ejecutar
archivo_bat1 = "buscarDatos.bat"
archivo_bat2 = "unirArchivos.bat"
archivo_bat3 = "GraficadorSO2.bat"

# Ejecutar el primer archivo .bat
subprocess.run([archivo_bat1])

# Ejecutar el segundo archivo .bat
subprocess.run([archivo_bat2])

# Ejecutar el tercer archivo .bat
subprocess.run([archivo_bat3])