import subprocess
import time
from datetime import datetime

HOST = "8.8.8.8"
INTERVALO = 5
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


def formato_hora(fecha):
    return fecha.strftime("%Y-%m-%d %H:%M:%S")


def hay_conexion():
    resultado = subprocess.run(
        ["ping", "-c", "1", "-W", "2", HOST],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return resultado.returncode == 0


print(CYAN + "Monitor de conexión iniciado." + RESET)
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
                    f"[{formato_hora(hora_vuelta)}] CONEXIÓN RESTABLECIDA. "
                    f"Tiempo caído: {duracion}"
                )

                print(VERDE + "\n✅ INTERNET RESTABLECIDO" + RESET)
                print(VERDE + mensaje + "\n" + RESET)
                escribir_log(mensaje)

                internet_caido = False
                hora_caida = None
            else:
                mensaje = f"[{formato_hora(ahora)}] OK - INTERNET CONECTADO"
                print(VERDE + "✅ " + mensaje + RESET)

        else:
            if not internet_caido:
                internet_caido = True
                hora_caida = ahora

                mensaje = f"[{formato_hora(hora_caida)}] ALERTA: SE CORTÓ INTERNET"

                print(ROJO + "\n🚨 INTERNET CORTADO 🚨" + RESET)
                print(ROJO + mensaje + "\n" + RESET)
                escribir_log(mensaje)
            else:
                mensaje = f"[{formato_hora(ahora)}] INTERNET SIGUE CORTADO"
                print(ROJO + "❌ " + mensaje + RESET)

        time.sleep(INTERVALO)

except KeyboardInterrupt:
    print(AMARILLO + "\nMonitor detenido por el usuario." + RESET)
    escribir_log("========== MONITOREO DETENIDO ==========")
