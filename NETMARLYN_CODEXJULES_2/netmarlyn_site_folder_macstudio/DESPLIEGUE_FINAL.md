# GUÍA DE DESPLIEGUE DEFINITIVA (MAC MINI)
**PUERTO MAESTRO: 9300**
**TECNOLOGÍA: Python Nativo (http.server)**

Para que el sitio funcione siempre al 100% y no dé error 404 ni problemas de permisos:

### 1. Instrucciones de Actualización (Proceso Seguro)
Cada vez que traigas una carpeta nueva desde la Mac Studio:
1. **Detén el servidor actual** en la Mac Mini (presiona `Ctrl+C` en la terminal o cierra la ventana).
2. **Borra la carpeta vieja** por completo.
3. **Pega la carpeta nueva**.
4. **IMPORTANTE:** Abre una terminal en la Mac Mini, arrastra el archivo `AUTOSTART_NETMARLYN_SERVER.command` dentro de la terminal y presiona Enter.
   * *Opcional:* Si macOS dice que no tiene permisos, corre: `chmod +x *.command` dentro de la carpeta.

### 2. ¿Por qué 9300?
Cloudflare Tunnel está configurado para buscar el tráfico en `localhost:9300`. 
**NUNCA cambies el puerto a 8000**, o el sitio mostrará "404 Not Found".

### 3. Arreglo de Error "No module named 'openpyxl'"
Si al subir un Excel el servidor da error, ejecuta esto una sola vez en la Mac Mini:
`pip install openpyxl python-docx`

### 4. Watchdog / Auto-arranque
El archivo `AUTOSTART_NETMARLYN_SERVER.command` ahora es inteligente:
* Revisa si hay internet antes de arrancar.
* Limpia el puerto 9300 automáticamente.
* Asegura que el servidor sepa en qué carpeta está parado (CWD Guard).
* Inyecta cabeceras Anti-Caché para que los cambios se vean al instante en los celulares.
