import subprocess
import time
from datetime import datetime

HOST = "8.8.8.8"
INTERVALO = 2
LOG_FILE = "registro_conexion.txt"

VERDE = "\033[92m"
ROJO = "\033[91m"
AMARILLO = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

internet_caido = False
hora_caida = None


def escribir_log(mensaje):
    with open(LOG_FILE, "a", encoding="utf-8") as archivo:
        archivo.write(mensaje + "\n")


def hay_conexion():
    resultado = subprocess.run(
        ["ping", "-c", "1", "-W", "2", HOST],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return resultado.returncode == 0


print(CYAN + "Monitoreando conexión a internet..." + RESET)
print(CYAN + f"Haciendo ping a {HOST} cada {INTERVALO} segundos." + RESET)
print(CYAN + "Presioná CTRL + C para detener.\n" + RESET)

escribir_log("========== INICIO DEL MONITOREO ==========")

try:
    while True:
        ahora = datetime.now()

        if hay_conexion():
            if internet_caido:
                hora_vuelta = ahora
                duracion = hora_vuelta - hora_caida

                mensaje = (
                    f"[{hora_vuelta.strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"CONEXIÓN RESTABLECIDA. Tiempo caído: {duracion}"
                )

                print(VERDE + "\n✅ INTERNET RESTABLECIDO" + RESET)
                print(VERDE + mensaje + "\n" + RESET)
                escribir_log(mensaje)

                internet_caido = False
                hora_caida = None
            else:
                mensaje = f"[{ahora.strftime('%Y-%m-%d %H:%M:%S')}] Conexión OK"
                print(VERDE + "✅ " + mensaje + RESET)

        else:
            if not internet_caido:
                internet_caido = True
                hora_caida = ahora

                mensaje = (
                    f"[{hora_caida.strftime('%Y-%m-%d %H:%M:%S')}] "
                    "ALERTA: SE CAYÓ INTERNET"
                )

                print(ROJO + "\n🚨🚨🚨 INTERNET CAÍDO 🚨🚨🚨" + RESET)
                print(ROJO + mensaje + "\n" + RESET)
                escribir_log(mensaje)
            else:
                mensaje = f"[{ahora.strftime('%Y-%m-%d %H:%M:%S')}] Internet sigue caído"
                print(ROJO + "❌ " + mensaje + RESET)

        time.sleep(INTERVALO)

except KeyboardInterrupt:
    print(AMARILLO + "\nMonitoreo detenido por el usuario." + RESET)
    escribir_log("========== MONITOREO DETENIDO ==========")
