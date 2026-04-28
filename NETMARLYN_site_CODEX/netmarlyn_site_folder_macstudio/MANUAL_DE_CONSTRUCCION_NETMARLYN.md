# 🚀 MANUAL DE CONSTRUCCIÓN NETMARLYN (IA SYNC)

> [!CAUTION]
> ### 🔴 MANDATO SAGRADO PARA LA IA (ANTIGRAVITY / JULES)
> **NO IGNORES ESTO SI NO QUIERES ROMPER EL SITIO.**
> 1. **PROTOCOLO HTTP:** Jamás pongas `send_header` antes de `send_response` en el servidor Python. Se ha implementado un blindaje estructural en `netmarlyn_server.py` que NO DEBES QUITAR.
> 2. **ARRANQUE:** Nunca lances el servidor manualmente. El ÚNICO método oficial es ejecutar `./AUTOSTART_NETMARLYN_SERVER.command`. Este script limpia puertos y reconstruye el LaunchAgent.
> 3. **ACTUALIZACIÓN:** No borres archivos a ciegas. Si el usuario sustituye la carpeta, ejecuta el script de autostart y todo volverá a la vida.
> 4. **REGLA DE ORO (LA MAC MINI MANDA):** Queda terminantemente prohibido tocar o modificar los archivos externos al workspace que controlan el arranque y la estabilidad en producción:
>    - `MASTER_NETMARLYN_LAUNCHER.command` (El cerebro en el Home).
>    - `com.netmarlyn.server.plist` (En la librería de agentes).
>    - `com.netmarlyn_watchdog.plist` (El perro guardián).
>    **Si necesitas tocarlos, DEBES PEDIR PERMISO EXPLÍCITO.** Si se alteran sin aviso, el sitio se caerá en cada reemplazo del folder del proyecto.
> 5. **CONVERSIÓN DE AUDIO LOCAL (MÁQUINA DEL TIEMPO):** Queda terminantemente prohibido enviar archivos de audio (.mp3, .wav, etc.) al servidor Mac Mini. La PWA debe realizar la conversión **Audio → Texto (Speech-to-Text)** localmente en el dispositivo del maestro. Al servidor solo viajará un JSON con el texto y metadatos. El audio debe ser destruido tras la conversión.
> 6. **LÍMITE TERRITORIAL:** La IA solo trabajará dentro del folder `@netmarlyn_site_folder_macstudio`. No se harán cambios fuera de este territorio bajo ninguna circunstancia sin autorización.
7. **PLANTILLA UNIVERSAL (AGILIDAD):** Se establece el uso de una plantilla de lista única y reutilizable para todo el ecosistema. Cada institución llenará exclusivamente los campos que necesite (ej. solo Sección A de un grado), dejando el resto libres. Esto asegura que el mismo patrón sea compatible con cualquier escuela o colegio, agilizando el despliegue masivo.

## 📍 ESTADO ACTUAL (Sesión 011 - Marzo 2026)
El sistema ha evolucionado a una **Arquitectura de Silos Masivos**. El sitio web (`netmarlyn_website_00`) ahora es agnóstico a los datos; toda la información institucional vive en una carpeta paralela llamada `folder_colegios_full`.
La prioridad actual es la **Seguridad Master de Alto Nivel** y la preparación de los módulos de Infografía y Maquetas 3D dentro de cada silo institucional.

### 🏛️ ARQUITECTURA DE DOBLE NATURALEZA (Público vs Privado)
> [!IMPORTANT]
> **REGLA ARQUITECTÓNICA DE ACCESO Y AISLAMIENTO:**
> El sitio web `netmarlyn.site` tiene una dualidad estricta que no debe romperse jamás:
> 1. **La Cara Pública (Comercial):** Es un portal abierto y de libre acceso. Sirve para marketing, mostrar videos, precios, e interactuar con una versión limitada de **Maunet Public (Agente de Ventas)** conectado al botón "TRY ME".
>    - Maunet Public reside en `MAUNET_PUBLIC_2`. Su única función es explicar qué es NetMarlyn y tiene restricciones de 10 temas, respuestas de 40 palabras, y límites de tiempo por sesión.
> 2. **La Cara Privada (Bóvedas Escolares):** Cada colegio es un "Silo" hermético y aislado.
>    - **Maunet Alumnos:** El Maunet original y completo (`MAUNET_SITE_SS_2`) solo es accesible desde la sección "Soporte" para alumnos. Queda PROHIBIDO alterarlo al modificar al Maunet Público.
>    - **Acceso Manual:** Si un usuario entra por la web y selecciona su colegio, se le exige la "Trinidad de Seguridad": **Nombre + PIN + Contraseña**. Sin esto, es imposible cruzar el muro.
>    - **Acceso por QR (Teletransporte):** Si el maestro/alumno escanea su carnet QR con la cámara nativa, el sistema lee la llave única y lo teletransporta *directamente* al interior de su bóveda privada de NetMarlyn sin pedir credenciales, logrando un acceso mágico y seguro.
>    - **Aislamiento Total:** Ningún usuario de un colegio puede ver, cruzar, o interactuar con la información de otro colegio bajo NINGUNA circunstancia.

---

## ✅ LO QUE YA FUNCIONA PERFECTAMENTE (¡NO TOCAR!)

### 1. El Servidor Local (Motor de Python)
* **Archivo:** `netmarlyn_server.py`
* **Logro:** El servidor sabe leer la base de datos `visitas_detalladas.json` tanto en formato moderno (`JSON Array`) como en su formato legado (`NDJSON` o líneas separadas) sin dar Error 500 y crashear.
* **Filtro Cero-Ruido:** Ignora las peticiones internas de la propia API o cargas de recursos estáticos (`.css`, `.js`, imágenes). Solo registra visitantes en `/api/visitas`.
* **Pathing Local Dinámico:** Todas las llamadas a `/` se re-enrutan limpiamente a `/netmarlyn_website_00/index.html` para servir la web.

### 2. El Interceptor (Cloudflare Worker)
* **Archivo:** `worker_cloud/worker.js`
* **Logro:** Actúa como aduana (Gatekeeper). Intercepta al visitante, extrae sus Headers, IP, OS, Geografía, e inyecta una Cookie "Sello" (`netmarlyn_uid`) para saber si es un visitante Recurrente o Nuevo.
* **Filtro:** Igualmente configurado para hacer bypass a las rutas de archivos pasivos y endpoints de la API, evitando loops de telemetría inútil.

### 3. La Telemetría Visual (TELEMETRÍA AL 90% - ESTABLE PARA ALTA CONCURRENCIA)
* **Archivo:** `netmarlyn_website_00/js/visualizers_v3.js` (Y `style.css` base)
* **Logro:** El motor de telemetría está consolidado al 90% usando una arquitectura robusta de "Escudo Térmico" con Cloudflare.
* **Mecánica Estricta:** Se usa polling pasivo asíncrono (500ms) leyendo el JSON. ESTÁ ESTRICTAMENTE PROHIBIDO inyectar parámetros como `?nocache=` en la URL del cliente, ya que rompen el enrutamiento absoluto del servidor Python.
* **Escala Masiva (El Secreto):** Con un `Edge TTL = 1 segundo` en la caché de Cloudflare, la Mac Mini está protegida. Aunque 1.3 millones de usuarios hagan polling a 500ms, el servidor físico solo recibe **1 petición por segundo**.
* **Matemática de Ráfagas (Apilado Visual):** La animación CSS dura 0.3s. El espaciado de ráfagas múltiples está ajustado matemáticamente a esto para no atropellar el renderizado visual y crear la ilusión de latidos independientes.
* **Scroll Restoration:** Modificamos el DOM en `index.html` para obligar al navegador (`history.scrollRestoration = 'manual'`) a ir a la posición `0,0` en cada refresh.

### 4. El Diseño Base CSS y PWA Starter
* **Archivo:** `netmarlyn_website_00/style.css` y la jerarquía base HTML.
* **Logro:** Está 100% responsivo para móviles, modo panorámico con estrellas y el logo del astronauta. Totalmente estático sin frameworks pesados ni React/Angular (Prohibidos por diseño).

---

## ✅ MÓDULO 7: Portal Listas (Director Login + Matriz de Aulas)
* **Archivo:** `netmarlyn_website_00/listas.html`
* **Logro:** Sistema de login de doble campo (Código 4 caracteres + Password) con validación estricta en frontend. Al ingresar credenciales correctas, el DOM se re-pinta dinámicamente mostrando la Matriz de Aulas completa (Prekínder → 2do Bachillerato) sin saltar a otra página.
* **Credenciales de Demo:** `A123/pepino1` → Colegio San Isidro | `B456/pepino2` → Colegio Los Andes
* **UI:** Botón de aula (66% ancho) + Indicador de estado rojo/verde (33% ancho) centrados con Flexbox. Ícono 👁️ de toggle de contraseña. Envío con tecla ENTER habilitado.
* **Menú:** Se actualizó la opción "videos" por "**acciones**" en todas las páginas del sitio.

---

## ✅ MÓDULO 8: Ingesta "Cajón Mágico" (Marzo 12, 2026)
* **Archivo:** `netmarlyn_website_00/listas.html` y `netmarlyn_server.py`
* **Logro:** Se implementó el panel de ingesta inteligente para alumnos.
* **Formatos Soportados:** 
    * **Manual:** Copiar y pegar directamente.
    * **Texto Plano:** `.txt` y `.csv` (lectura en el navegador).
    * **Ofimática:** `.docx` (Word) y `.xlsx` (Excel). El servidor Python usa `python-docx` y `openpyxl` para extraer el texto y devolverlo a la UI.
    * **Foto:** Detección de dispositivo móvil para activar la cámara y tomarle foto a la lista física.
* **UI/UX Premium:**
    * Botones personalizados usando `assets/boton_netmarlyn_general.png` con texto blanco superpuesto y efectos de hover/active.
    * **Persistencia:** Al subir una lista, se guarda en `localStorage` del navegador que el aula está completa. Al recargar la página (con auto-login), los indicadores se pintan de verde ✅ automáticamente.
* **Filosofía de Plantilla Universal (v4.8):** El sistema está diseñado para que una sola matriz de aulas sea válida para cualquier institución. Si un colegio no cuenta con secciones B o C, simplemente ignora esos campos en la ingesta. El motor es lo suficientemente inteligente para renderizar solo lo que tiene datos, permitiendo una reutilización total del código base sin importar el tamaño del colegio.
    * **Navegación Intuitiva:** Sistema de Scroll automático que lleva al usuario al Cajón al abrirlo y vuelve al píxel 0 (arriba) al cancelar.
    * **Robustez:** URLs de API corregidas a `http://127.0.0.1:8000` para evitar errores de red cuando se abre el archivo localmente.

---

## ✅ MÓDULO 9: Portal de Acciones (Marzo 12, 2026)
* **Archivo:** `netmarlyn_website_00/acciones.html`
* **Logro:** Se construyó el portal de Acciones protegido con la misma lógica de Login estricto que el portal de Listas.
* **Flujo:** 
    * El menú principal cambió la pestaña "videos" por "**acciones**".
    * Al ingresar, se exige Código de Institución y Contraseña (ej: A123 / pepino1).
    * Tras validación, se oculta el login y se muestra un **grid de 2x2** con cuatro botones interactivos (generados con la imagen oficial `assets/boton_netmarlyn_general.png`):
        1. TOMAR FOTOS
        2. SOS ESTOY
        3. REPORTES
        4. LISTAS

---

## ✅ MÓDULO 10: Generación de Identidades QR y Panel de Fotos (ONLINE)
- [x] Crear portal `fotos.html` para asignación masiva de imágenes.
- [x] Endpoint `/api/subir_foto` para procesar Base64 y guardar JPGs.
- [x] Marcado dinámico de botones verdes al capturar foto.
- [x] **MEJORA DE PERSISTENCIA:** Implementado `/api/obtener_estado_grados`. Ahora la página web pregunta al servidor el estado real al cargar, evitando que los botones se vuelvan rojos al cerrar el navegador.
- **Resultado:** ✅ Orden total. El proyecto cumple con la jerarquía original. El servidor es capaz de servir el sitio correctamente sin tener archivos regados por todo el workspace.

---

### SESIÓN-017 — Establecimiento de la Regla de Oro y Límites Territoriales
- **Fecha:** 16 de Marzo 2026 — 14:50 hrs (UTC-6)
- **Objetivo:** Blindar los archivos de sistema de la Mac Mini y definir el área de trabajo estricta de la IA.
- **Acciones realizadas:**
    1. **Inscripción de la Regla de Oro:** Se documentó la prohibición absoluta de tocar `MASTER_NETMARLYN_LAUNCHER.command`, `com.netmarlyn.server.plist` y `com.netmarlyn_watchdog.plist`.
    2. **Limitación de Workspace:** Se aceptó formalmente que el trabajo de la IA se limita exclusivamente al interior del folder `netmarlyn_site_folder_macstudio`.
    3. **Protocolo de Respeto:** Cualquier cambio fuera del workspace debe ser consultado y aprobado previamente para evitar caídas del sistema en despliegues vía AirDrop.
- **Resultado:** ✅ Seguridad de despliegue garantizada. La IA reconoce su territorio y respeta el sistema de arranque de la Mac Mini.
- [ ] Generación de Carnet Digital Completo (QR + Foto + Datos).
- [ ] Pruebas de escaneo desde dispositivo externo.

---
> [!IMPORTANT]
> **REQUERIMIENTO TÉCNICO EN MAC MINI:**
> Para que el botón "SUBIR ARCHIVO" funcione con Excel y Word desde el móvil, es obligatorio ejecutar en la terminal de la Mac Mini:
> `pip install openpyxl python-docx`
* **Flujo:** 
    * El botón "TOMAR FOTOS" de Acciones dirige ahora a `fotos.html` (interfaz idéntica al portal de Listas pero orientada a alumnos).
    * Al hacer clic en un grado con lista subida (ej. Prekínder B), se consume un nuevo endpoint `/api/obtener_lista`.
    * El backend Python abre el JSON, detecta alumnos sin ID y les genera en milisegundos una **Identidad Digital Única** con el formato exacto requerido (`XXXXXXX-XXXX`, ej. `3847211-F7K2`). Luego sobreescribe y guarda.
    * El UI (`fotos.html`) pinta en pantalla una interfaz de filas con cada alumno, su respectivo número de lista, su ID digital autogenerado, y un botón "📷 TOMAR FOTO" (o "✅ FOTO OK").
    * Bug de Storage (COLE) solucionado: El código de la institución ahora- El servidor genera automáticamente el código matricial único (`7 dígitos - 4 letras`) al procesar las listas por primera vez.
- **Identificación en Escaneo:** El endpoint `/api/identificar_alumno` realiza una búsqueda global en todos los colegios y devuelve identidad + foto + grado en tiempo real.

---

## 🛠 GUÍA DE SUPERVIVENCIA: FIX RÁPIDO PARA SITIO CAÍDO
Si el sitio da **Error 404** o **Malformed HTTP Status** en Cloudflare, esta es la cura:

### 1. Puerto Maestro 9300
El túnel de Cloudflare en la Mac Mini está programado para buscar el puerto **9300**. 
- **Error Típico:** Cambiar el puerto en `netmarlyn_server.py` a 8000 por error.
- **Solución:** Verificar que `PORT = 9300` en el código.

### 2. Error de Protocolo (Malformed Status Code)
- **Causa:** Enviar cabeceras `send_header()` antes del `send_response(200)`.
- **Cura:** El servidor siempre debe enviar primero la respuesta de éxito y luego los parámetros de caché. Cloudflare rechaza respuestas desordenadas.

### 3. Guardia CWD (Current Working Directory)
Para que el servidor no dé error de "File Not Found" al actualizar la carpeta:
- El código incluye `os.chdir(os.path.dirname(os.path.abspath(__file__)))`. Esto ancla el servidor a su carpeta real sin importar cómo se lance.

### 4. Limpieza de procesos Zombis
Si el puerto está bloqueado:
- Usar `AUTOSTART_NETMARLYN_SERVER.command` el cual ejecuta `lsof -ti:9300 | xargs kill -9` antes de arrancar.

## ✅ MÓDULO 10.1: Mandato de Escalabilidad (Millones de Archivos)
- **Desafío:** 50,000 maestros generando 1 infografía cada 50 minutos = **Millones de archivos**.
- **Solución Obligatoria:** Las infografías **NUNCA** se guardarán en una carpeta plana. Se usarán los **Silos de Colegio** (`folder_colegios_full/CODIGO_Colegio/maquina_tiempo/`).
- **Razón Técnica:** Repartir la carga entre miles de carpetas evita que el sistema de archivos de macOS se vuelva lento. 5 millones de archivos en una carpeta rompen el disco; 5 millones repartidos en 10,000 silos es pan comido para el Mac Mini.
- **Ubicación:** Todo el ecosistema de datos vive en la raíz del proyecto (`@netmarlyn_site_folder_macstudio`), asegurando que sea fácil de comprimir y mover vía Airdrop.

---

## ✅ MÓDULO 11: Registro Master y Silos 10X (ESTADO ACTUAL)
- **Logro:** El Administrador Master puede crear nuevos colegios.
- **Acción:** El servidor genera una carpeta única con el formato `NM-ID_Nombre` y dentro crea 10 subcarpetas de silos: `listas`, `fotos`, `infografias`, `maquetas_3d`, `giroscopio`, `maquina_tiempo`, `reportes`, `geofencing`, `seguridad`, `trabajos_grupos`.

---

### 🚀 FLUJO DE DESARROLLO Y DESPLIEGUE (MAC STUDIO → MAC MINI)

Debido a que la programación activa se realiza en la **Mac Studio** (Entorno de Desarrollo) y el sitio corre "al aire" en la **Mac Mini** (Entorno de Producción), se establece el siguiente protocolo obligatorio de sincronización:

1.  **Edición en Mac Studio:** Todo el código nuevo se escribe y valida localmente en la Mac Studio (folder `@netmarlyn_site_folder_macstudio`).
2.  **Empaquetado:** Se comprime el folder completo `@netmarlyn_site_folder_macstudio` una vez finalizados los cambios de la sesión.
3.  **Transferencia Vía Airdrop:** Se envía el archivo comprimido a la **Mac Mini**.
4.  **Sustitución Total:** En la Mac Mini, se debe **reemplazar/sustituir** el folder anterior por este nuevo para asegurar que no queden archivos huérfanos.
5.  **Reinicio de Motor:** Se ejecuta `AUTOSTART_NETMARLYN_SERVER.command` en la Mac Mini para aplicar los cambios del backend (`netmarlyn_server.py`).

---

**UI:** Grilla dinámica (3xN en Desktop / 2xN en Móvil) de botones oficiales de Netmarlyn con nombres optimizados.

---

## ✅ SECCIÓN 14: ARQUITECTURA HÍBRIDA MASIVA: MAUNET PARA 2 MILLONES DE ALUMNOS

> [!IMPORTANT]
> **REGLA ESTRUCTURAL (Hive Mind & Edge Sync):** La infraestructura central de la Mac Mini M1 NO DEBE procesar los 2 millones de chats (LLM) concurrentemente, pues se produciría un colapso físico por *timeouts* (Límite de procesamiento secuencial de Ollama). La carga se transfiere a los 2 millones de celulares mediante una arquitectura "98/2".

### 1. INSTALACIÓN FRACCIONADA (El Starter Pack)
Para asegurar que las instalaciones en dispositivos móviles sean ultraligeras y accesibles, la PWA descarga un "Starter Pack" de ~90MB. Este paquete inicial incluye:
- El motor funcional de NetMarlyn y la PWA.
- Maunet Básico (El asistente offline).
- **Únicamente el 5% del JSON Maestro** de conceptos escolares. 
Esto permite que el alumno comience a interactuar casi al instante.

### 2. DESCARGA INCREMENTAL (Network-Aware Fetch)
Los ~20MB restantes del `concepts.json` (hasta alcanzar los 90,000 conceptos) se descargan de forma imperceptible en segundo plano, condicionados por la red detectada:
- **Red Wi-Fi ilimitada:** Descarga acelerada en 2 o 3 etapas (aprox. 30 minutos).
- **Red de Datos Limitados (Móvil):** Descarga agresivamente fraccionada en 10 a 20 micro-etapas (aprox. 1 a 2 días), protegiendo la economía de datos del usuario y evitando el sobrecalentamiento de celulares gama baja o media-baja.

### 3. MOTOR EDGE AUTÓNOMO (El 98%)
Cuando un estudiante hace una pregunta (ej. "¿Qué es la fotosíntesis?"), el buscador local JavaScript intercepta la consulta contra su IndexedDB de 90,000 conceptos. Al encontrarlo, aplica plantillas procedimentales para responder.
- **Impacto en Servidor:** 0%.
- **Resolución:** El 98% del tráfico nacional se atiende directamente con el procesador del celular del alumno.

### 4. EL EFECTO "ENJAMBRE NACIONAL" (El 2%)
La genialidad del sistema radica en su retroalimentación evolutiva:
1. **La Falla del JSON:** El alumno realiza una pregunta compleja o inédita que no se encuentra en sus 90,000 conceptos locales (el 2%).
2. **Consulta a la Mac Mini:** La PWA deriva excepcionalmente esa pregunta al servidor de la Mac Mini (`/api/chat`).
3. **Inscripción Inteligente (El Aprendizaje):** La Mac Mini responde al estudiante y, de inmediato, **inscribe (incrementa inteligentemente)** este nuevo concepto en el `concepts.json` Maestro del servidor.
4. **Sincronización Desfasada:** Durante las siguientes horas, los 2 millones de celulares se conectan a NetMarlyn (cada uno en minutos y segundos diferentes, distribuyendo la carga de manera orgánica). Al detectar que el archivo Maestro creció, descargan **solo el incremento** (delta).
5. **Resultado:** El cerebro de Maunet se enriquece, entrena y expande colaborativamente en todo el país de forma automática.

### 5. DIRECTOR CINEMATOGRÁFICO DE CARGA (Zero-Wait UX)
Dado que el tiempo real de carga de Maunet (Modelo 3D + Procesamiento LLM local) toma de 7 a 15 segundos, es **ESTRICTAMENTE PROHIBIDO** usar pantallas congeladas. Para evitar que el alumno perciba latencia y garantizar un enganche visual continuo, se implementa una "Orquestación de Fases Cinematográficas":
1. **Pre-Fetching Oculto:** En el milisegundo cero (al escanear carnet o presionar botón), el cliente dispara en *background* peticiones paralelas masivas (carga 3D + LLM/Ollama Fetch). 
2. **Pantallas y Tiempos de Gracia:** Mientras el background trabaja duro, el frontend exhibe una coreografía visual:
   - Pantalla Negra (2s)
   - Barras aleatorias con velocidades procedimentales y frases hipnóticas de carga (4-6s)
   - Pantalla Negra (2s)
   - Ceder el control al usuario con "Toque la Pantalla" (esto desbloquea las políticas de audio del navegador móvil y gana 1s extra)
   - Negro Transicional Final (2-3s)
3. **El Engaño Perfecto:** Para cuando esta coreografía finaliza (~15 segundos), el pesado proceso en background ya culminó. Al desaparecer el negro, Maunet habla y responde *de forma instantánea*, entregando la percepción absoluta de un motor IA de 0ms de latencia.

---

## ✅ MÓDULO 12: Protocolo de Escaneo Masivo (OFFLINE-FIRST + NM-ID)

### 🔳 ARQUITECTURA DEL CÓDIGO QR (DOBLE PROPÓSITO)
> [!IMPORTANT]
> **REGLA DE ORO DEL QR (Velocidad extrema + Acceso Universal):**
> El código QR impreso en el carnet del alumno DEBE contener una URL extremadamente corta (Ej: `netmarlyn.site/a1b2c`, aprox 21 caracteres) para forzar la creación de un **QR Versión 1 o 2**.
> - **¿Por qué?** Un QR de baja densidad se escanea en < 0.2 segundos, vital para evitar cuellos de botella al pasar asistencia masiva con celulares de gama baja.
> - **Doble Comportamiento:**
>   1. **Alumno (Cámara Nativa):** Al escanear con su celular, la URL lo redirige directo a su perfil logueado en NetMarlyn (acceso instantáneo sin entrar a la web primero).
>   2. **Maestro/Guardia (Cámara PWA):** El escáner interno de NetMarlyn ignora el dominio, extrae solo el código `a1b2c`, lo cruza con IndexedDB (Offline) y registra la asistencia en milisegundos.

### 📱 GESTIÓN EN EL DISPOSITIVO (PWA)
1. **Identificación Previa del Maestro (Llave de Acceso):** Para evitar descargar la base de datos de 2 millones de alumnos, el maestro debe escanear **su propio carnet** al entrar a "Asistencia". El sistema lee su NM-ID y determina a qué colegio pertenece.
2. **Inicialización Fraccionada:** Una vez identificado el colegio del maestro, la PWA verifica la versión de la base local en **IndexedDB** ÚNICAMENTE para ese colegio. Un maestro jamás descarga la DB universal; como máximo descarga unos 3000 alumnos locales de su institución.
3. **Sincronización O(1):** Si es necesario, descarga el dataset incremental de su colegio específico y lo persiste indexado para búsquedas instantáneas.
4. **Modo Local Puro:** Una vez sincronizado, la cámara (jsQR) valida IDs contra la memoria local. **Latencia Cero.**
4. **Generación de Eventos con UUID:** Cada escaneo exitoso genera un JSON con: `event_id` (UUID único), `alumno_id`, `timestamp`, `GPS`, `device_fingerprint` y un `hash_integridad` (SHA-256).
5. **Cola FIFO Persistente:** Los eventos se guardan en IndexedDB con los flags: `verificado_local = true` y `procesable_servidor = true`.
6. **Motor de Sincronización (Background Sync):** El Service Worker detecta conectividad y envía batches (5-20 eventos) usando el `event_id` para garantizar **Idempotencia**.
7. **Estrategia de Envío:** Reintento con backoff exponencial. Solo se borra el evento local tras recibir el ACK del servidor `200 (recibido: true)`.

### 🐍 GESTIÓN EN NETMARLYN SERVIDOR LOCAL (INGESTA)
1. **Ingesta Masiva:** El servidor recibe eventos (individual o batch), valida estructura mínima + `event_id` + `hash`. Verifica idempotencia y responde ACK inmediato.
2. **Journaling / Escritura Segura:** Escribe el evento crudo en `/escaneos_recibidos/{colegio_id}/` usando técnica de escritura atómica (tmp → rename).
3. **Escritura Append-Only:** Cada evento se registra en un log de auditoría para permitir reconstrucción tras un crash.
4. **Workers de Procesamiento Controlado:**
    - **Worker Primario (Validación):** Toma el evento, revalida integridad y lo mueve a `/escaneos_procesar/{colegio_id}/`.
    - **Worker Secundario (Persistencia):** Consume la cola de procesamiento, normaliza datos e inserta en la base de datos definitiva con índices por alumno, colegio y fecha.
5. **Resiliencia Total:** Nunca se elimina un archivo de la cola sin confirmación de inserción en DB. Sistema particionado por colegio para evitar cuellos de botella globales. Capaz de escalar a **millones de registros concurrentes**.

---

---

## 📍 PRÓXIMOS MÓDULOS (ABRIL - MAYO)
1. **Infografías Dinámicas:** Generación de posters escolares desde datos JSON.
2. **Maquetas 3D Interactivas:** Sincronización de deltas JSON para colaboración multiplayer.
3. **Giroscopio y Radar:** Implementación del rastreo espacial dentro de los silos.
- El usuario va a probar el escaneo en vivo con un dispositivo real.
- El objetivo es que al escanear, el sistema devuelva los datos del perfil vinculado (nombre, colegio, grado, rol).

---

---

## 🔍 AUDITORÍA DEL SERVIDOR — 13 Marzo 2026 (Sesión Antigravity)

**Archivo auditado:** `netmarlyn_server.py` (528 líneas, 25KB)
**Resultado:** ✅ SERVIDOR BLINDADO Y CORRECTO

### Blindajes confirmados activos:

| Protección | Líneas | Estado |
|---|---|---|
| Override `send_response()` — Escudo HTTP | 29–38 | ✅ ACTIVO |
| `os.chdir(script_dir)` — Guardia CWD | 12–13 | ✅ ACTIVO |
| Fallback NDJSON para visitas_detalladas.json | 65–76 | ✅ ACTIVO |
| Puerto fijo 9300 | 15 | ✅ CORRECTO |
| Fotos guardadas como `{QR}.jpg` (sin prefijo) | 331 | ✅ CORRECTO |
| Ruta sitio → `netmarlyn_website_00/` | 512–514 | ✅ CORRECTO |
| CORS global en override (no en endpoints) | 38 | ✅ OK (hay 2 redundantes inofensivos en líneas 356 y 428) |

### Endpoints activos (NUNCA ELIMINAR):
- `POST /api/visitas` — Telemetría de visitantes
- `POST /api/subir_lista` — Guardar lista de alumnos
- `POST /api/obtener_lista` — Obtener lista + asignar IDs QR
- `POST /api/obtener_estado_grados` — Ver qué grados tienen listas
- `POST /api/identificar_alumno` — Buscar alumno por QR (búsqueda global)
- `POST /api/subir_foto` — Guardar foto Base64 como JPG
- `POST /api/leer_archivo` — Leer Word/Excel/CSV y extraer texto
- `GET  /api/live_stats` — Total de visitas para el ecualizador
- `GET  /api/ver_foto?qr=XXX` — Servir foto del alumno como imagen JPEG
- `OPTIONS *` — CORS preflight

### Nota de sesión:
El servidor está 100% listo para ser copiado y enviado via AirDrop a la Mac Mini.
El Guardia CWD garantiza que se ancle a su propia carpeta al arrancar.
El Escudo HTTP garantiza que Cloudflare no rechace ninguna respuesta.

---

## 🛠 REPORTE TÉCNICO DE ACTUALIZACIÓN INDESTRUCTIBLE (POST-MORTEM)
**Fecha:** 12 de Marzo, 2026
**Estatus:** ✅ SOLUCIONADO DE RAÍZ

### 🚨 EL PROBLEMA: ¿Por qué se caía el sitio al actualizar?
1. **Violación de Protocolo HTTP:** El servidor Python enviaba cabeceras de caché (`Cache-Control`) *antes* de enviar el código de estado (`200 OK`). Cloudflare detectaba este desorden como un "Malformed Status Code" y cortaba la conexión.
2. **Procesos Zombi:** Al sustituir la carpeta, el servidor viejo no moría, bloqueando el puerto 9300 e impidiendo que el nuevo arrancara.
3. **Pérdida de Configuración:** Al sobreescribir la carpeta completa, se perdían los "parches" manuales hechos en el servidor por la IA.

### 🛡️ LA SOLUCIÓN ESTRUCTURAL (EL BLINDAJE)
1. **Escudo en `netmarlyn_server.py`:** Se reprogramó el método `send_response`. Ahora es físicamente imposible que un programador o una IA envíe cabeceras antes del código de estado. El servidor ahora fuerza el orden correcto automáticamente.
2. **Motor de Autocuración (v4.0):** El archivo `AUTOSTART_NETMARLYN_SERVER.command` ahora hace 5 cosas críticas:
   - Limpia agresivamente el puerto 9300.
   - Instala librerías faltantes (`openpyxl`, `docx`) automáticamente.
   - Arranca el servidor Y el túnel en paralelo.
   - **Instala un LaunchAgent (Guardián):** Registra el sitio en macOS para que arranque solo al prender la computadora, incluso si se borra la carpeta original.

### 🧠 MEMORIA PERSISTENTE DE 90 DÍAS (Maunet Original) — PENDIENTE DE IMPLEMENTAR
**Aplica SOLO a Maunet Original (`MAUNET_SITE_SS_2`).** Maunet Público NO tiene esta funcionalidad.

**Arquitectura:**
- Cada alumno tiene un JSON incremental en el servidor NetMarlyn (`/api/memory/{carnet}`).
- Cada sesión se sintetiza en **una oración de ~25 palabras** con fecha/hora/ubicación/gps.
- La limpieza de entradas >90 días ocurre **en el mismo instante** en que se incrementa una nueva entrada, antes de hacer el POST al servidor.
- Tamaño estimado por alumno: ~5-90KB. Para 2 millones de alumnos: ~12-180GB total (manejable).

**Flujo:**
1. Alumno abre Maunet → JS descarga JSON del servidor → lo guarda en RAM (NO lo menciona, solo lo tiene disponible).
2. Alumno platica normalmente. Si pregunta del pasado → Maunet consulta el JSON. Si no pregunta → no lo toca.
3. Alumno cierra/sale → JS sintetiza en 25 palabras → agrega al JSON → limpia >90 días → envía con `sendBeacon`.
4. **Seguro extra IMPORTANTE:** Auto-sync cada 5 minutos por si el navegador muere sin disparar el cierre.

**Endpoints del servidor (`server.py`):**
- `GET /api/memory/{carnet}` → Devuelve el JSON del alumno.
- `POST /api/memory/{carnet}` → Recibe y guarda el JSON actualizado.

**Ejemplo de entrada en el JSON:**
```json
{
  "ts": "2026-04-24T10:30:00",
  "geo": "14.6349,-90.5069",
  "memo": "La sal se disuelve en agua, altera el entorno de peces causando asfixia, influye en conservación de carne y estrés modifica procesos biológicos y ambientales."
}
```

### ⚠️ MANDATOS PARA EL FUTURO (SOPORTE TÉCNICO)
- **A las IAs:** NUNCA inyectar `send_header` al inicio de una función. Usar siempre el portal seguro de `end_headers` o confiar en el `send_response` blindado.
- **Memoria a Corto Plazo (Sesión):** Para evitar la "amnesia de sesión", JAMÁS uses regex de señales de continuidad (ej. `CONTINUITY_SIGNALS`) para decidir si inyectar historial. Debes inyectar SIEMPRE un `slice(-16)` del `sessionConversationHistory` en cada `callLLM`, garantizando que el agente recuerde el flujo completo sin importar si el usuario cambia de tema.
- **Arquitectura de Memoria Dual (Evitar Confusiones de Temas):** El LLM tiene un límite de turnos para no saturarse (`SESSION_CONTEXT_MAX_TURNS`). Para evitar que olvide el primer tema tras hablar mucho, DEBES usar un registro PERMANENTE (`sessionTopicLog`) que almacene únicamente las preguntas del usuario. Este arreglo NUNCA se recorta y se inyecta como una lista numerada explícita en el prompt para que el modelo sepa exactamente los temas tratados, incluso si el texto completo ya fue recortado del historial.
- **Al Usuario:** Para actualizar, simplemente copia y pega los archivos. No necesitas borrar la carpeta anterior. Dale doble clic al comando de autostart y el sistema hará la cirugía de limpieza solo.

- **Pausa Cinemática de TTS (Bug del Ícono Vocalizado):** Si el motor TTS de macOS accidentalmente pronuncia el "tag" de un ícono inyectado (ej. "¡Lo tengo perro el ciclo..."), DEBES aislar los prefijos estáticos. Inyecta el texto puro del prefijo (acompañado de una coma para forzar la pausa natural del TTS) directamente a la cola `speechQueue.push({text: '¡Lo tengo!,'})` en lugar de concatenarlo. Así evitas que el NLP Interceptor inserte íconos entre la exclamación inicial y el inicio real de la respuesta.
- **Ley Anti-Alucinación (Prompting Estructural):** Para evitar que el LLM invente palabras, NUNCA utilices "ejemplos de palabras erróneas" en el System Prompt (como "no digas inclujjeendo"), ya que el modelo tenderá a imitar la estructura de la alucinación. En su lugar, utiliza un mandato algorítmico: oblígalo a realizar una *verificación interna de diccionario* antes de emitir cada token.
