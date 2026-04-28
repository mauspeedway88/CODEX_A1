# GUÍA DE FUSIÓN Y MIGRACIÓN: TELEMETRÍA (MAC STUDIO) A PRODUCCIÓN (MAC MINI)
**Proyecto:** NETMARLYN SAFE-PASS Server

## ACERCA DE ESTA MIGRACIÓN (LEER EXCACTAMENTE)
Esta guía instruye cómo integrar el nuevo **Motor de Telemetría (Fase 1.1 y 1.2)** creado en la Mac Studio, dentro del servidor de Producción que ya existe en la Mac Mini.
Se debe respetar la arquitectura actual de la Mac Mini definida en el documento `Transferencia.pdf`.

### 1. EL "GATEKEEPER" (Ya en la Nube - NO TOCAR)
El script de Cloudflare Worker (`worker_cloud/worker.js`) **YA ESTÁ ALOJADO** en la red de Cloudflare interceptando todo el tráfico de `*netmarlyn.site/*`.
* Su función es doble: Mostrar la imagen en Base64 de mantenimiento si hay caídas, y extraer muchísima data (Lat/Lon, ISP, Continente, ZIP, OS, Browser, TLS).
* Envía toda esta data mediante un `POST` a la ruta remota `https://www.netmarlyn.site/api/visitas`. 

### 2. LA TAREA DE FUSIÓN DEL SERVIDOR (ACCIÓN REQUERIDA PARA LA OTRA IA)
La Mac Mini actualmente ejecuta su propio servidor en **Flask sobre el Puerto 9300** impulsado por el bash script `AUTOSTART_NETMARLYN.command`, el cual incluye reglas anti-caché críticas de fuerza bruta.
En la Mac Studio se creó un servidor crudo (`netmarlyn_server.py`) en el puerto 8000 que atrapa y guarda el `POST` en el archivo `visitas_detalladas.json`. 

**La instrucción para ti (El Antigravity de la Mac Mini) es FUSIONAR AMBOS MUNDOS:**
1. NO uses el `netmarlyn_server.py` que viene en esta carpeta importada.
2. Abre el verdadero `netmarlyn_server.py` de producción (el de Flask en el puerto 9300).
3. Inyéctale un nuevo endpoint `/api/visitas` (`@app.route('/api/visitas', methods=['POST'])`).
4. Haz que este nuevo endpoint atrape la data JSON enviada por el Gatekeeper de Cloudflare y la guarde/acumule en el archivo `visitas_detalladas.json`.
5. Asegúrate de mantener absolutamente intactas las reglas de cabeceras Anti-Caché descritas en *Transferencia.pdf*.

### 3. CONTINUACIÓN DEL DESARROLLO (LO QUE SIGUE EN MAC STUDIO Y MINI)
Una vez que el servidor Flask en la Mac Mini esté modificado y atrapando las visitas guardándolas en el `.json` correctamente, **el desarrollo de diseño visual continuará bifurcado en la Mac Studio**, comenzando con:
- 1.3 Menú de Navegación del sitio con UX de gama alta.
- 1.4 Directorio de Instituciones (Logos de colegios y "Mini-Métricas").

Toda confirmación de éxito en guardar los datos debe ser reportada por ti (IA de la Mac Mini) al usuario para que vuelva tranquilo a terminar la Fase 1.3 aquí en la Mac Studio.
