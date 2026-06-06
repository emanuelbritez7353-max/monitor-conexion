# Monitor de conexión a internet

Script en Python para monitorear la conexión a internet haciendo ping a 8.8.8.8 cada 2 segundos.

## Funciones

- Muestra conexión activa en la terminal.
- Alerta cuando se cae internet.
- Avisa cuando vuelve la conexión.
- Calcula cuánto tiempo estuvo caído el servicio.
- Guarda eventos en `registro_conexion.txt`.

## Ejecutar

```bash
python3 monitor_conexion.py
