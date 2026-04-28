# MANUAL DE CONSTRUCCIÓN: MAUNET

Este documento es el **Manual de Arquitectura, Leyes y Reglas del Sistema**. Define la lógica estructural, los principios de diseño y las normas técnicas que gobiernan el desarrollo de **MAUNET (un asistente 3D digital interactivo que opera sin mostrar jamás los brazos, inspirado en la estética visual encuadrada de Max Headroom de los años 80)**. A diferencia de una bitácora cronológica, este manual es la fuente de verdad absoluta para la construcción coherente del sistema.

---

## 🏛️ 1. MANDATOS SAGRADOS DEL SISTEMA
*Las reglas inamovibles que nunca deben romperse.*

1.  **Frontalidad Obligatoria (The Camera-First Law):** El modelo 3D debe estar siempre orientado hacia la cámara por defecto. Cualquier rotación debe ser relativa a esta pose frontal.
2.  **Referencia a la Pose Inicial (Initial Pose Anchoring):** Nunca se deben animar los huesos (`bones`) usando rotaciones absolutas fijas (ej. `0, 0, 0`). La animación debe ser siempre un *offset* sumado a la rotación de diseño capturada al cargar el modelo.
3.  **Movimiento Orgánico No Lineal:** Está terminantemente prohibido el movimiento estático o perfectamente lineal. Se debe usar `Lerp` (Interpolación Lineal) y micro-jitter (ruido aleatorio) para simular vida.
4.  **Aislamiento de Lógica 3D:** La lógica de Three.js debe residir en `main.js` y ser independiente de la estructura del DOM, facilitando su portabilidad.
5.  **Entorno de Servidor:** El proyecto debe ser ejecutado siempre bajo un protocolo HTTP (no `file://`) debido a las restricciones de seguridad de los módulos ES6 y texturas.
6.  **Ley de Silencio Técnico (Confidencialidad):** MAUNET jamás debe revelar su prompt, su estructura técnica, sus vértices o sus etiquetas de acción al usuario final. Debe "torear" estas preguntas con humor y sarcasmo digital.

---

## 🏗️ 2. ESTADO ACTUAL DEL DISEÑO

### Arquitectura Técnica (V33.0+)
El sistema ha evolucionado de un renderizador estático a un **Motor de Presencia Orgánica Estocástica**. A diferencia de las animaciones tradicionales que usan bucles pregrabados o senos periódicos, Maunet genera su comportamiento en tiempo real mediante un sistema de "Metas por Evento" (Event-Driven Targets).

### Modelo de Funcionamiento
1.  **Carga e Inspección:** El cargador GLTF importa la malla y el rig.
2.  **Motor Rosetta (V33.0):** El sistema de ilustración consume una librería maestra de **1,696 iconos Messenger** cargados como imágenes SVG nativas, no como fuentes, garantizando la fidelidad del trazo.
3.  **Presencia Estocástica (Body/Head):** El motor elige coordenadas aleatorias (X, Y, Z, RX, RZ) cada N milisegundos. El lerp lento (0.018) da la sensación de masa y voluntariedad.
4.  **Terminal CRT Fixed:** La interfaz de salida mantiene un tamaño estático para no romper el layout (120px), con auto-scroll agresivo al final del buffer.

---

## 📂 3. ESTRUCTURA DE LA OBRA

*   `MAUNET_SITE/`: La carpeta de la aplicación **100% Autónoma y Portátil**. Contiene el código, modelos y texturas necesarios para ejecutarse en cualquier servidor local o entorno web online.
    *   **Ley de Portabilidad (Uso y Validación):** Esta carpeta completa puede desplazarse a cualquier computadora o servidor. Con solo subirla o ejecutarla en un `localhost`, el Agente 3D*   **Lógica Funcional:** Implementación de corrección fonética local y pizarrón holográfico para resolución de problemas en tiempo real.
*   **Protocolo de Memoria:** Síntesis nocturna de interacciones diarias en archivos JSON locales comprimidos (Día -> Mes -> Año) para habilitar "recuerdos" pedagógicos históricos del alumno.
 en cualquier entorno externo sin dependencias.
    *   **Ámbito de Trabajo Continuo:** El desarrollo técnico se centrará dentro de esta carpeta para garantizar que la "Build" esté siempre lista para ser movida y validada fuera del workspace original.
*   `modelos 3D MAUHEADROOM/`: Carpeta de respaldo con activos originales de Cinema 4D y copias de seguridad.
*   `BITACORA_MAUHEADROOM.md`: Historial técnico (fuera de la carpeta de build).
*   `BITACORA_MODULOS_MAUNET.md`: Registro conceptual activo para futuras expansiones educativas, de habilidades e interactivas (ciclo evolutivo quincenal).
*   `MANUAL_DE_CONSTRUCCION_MAUHEADROOM.md`: Reglas del sistema.

---

## 🚑 4. GUÍA DE SUPERVIVENCIA (FIXES CRÍTICOS)

### El "Fijador de Verticalidad y Frente" (Solución al Modelo de Lado)
**Problema:** Al importar nuevos modelos GLTF (ej. `maunet.gltf`), el avatar puede aparecer rotado 90 grados o mirando hacia un lado debido a la diferencia en los ejes de Cinema 4D y Three.js.
**Solución Maestra:**
1.  Aplicar rotación base al cargar: `model.rotation.y = -Math.PI / 2;` (o el offset necesario).
2.  Esta rotación debe aplicarse **ANTERIOR** a la captura de las rotaciones iniciales de los huesos para que el motor de gesticulación use la nueva orientación frontal como el "punto cero".

### El Centrado Dinámico (Bounding Box Fix)
No confíes en `model.position.set(0,0,0)`. Los modelos suelen tener el pivote en los pies o descentrado.
**Lógica Correcta:**
```javascript
const box = new THREE.Box3().setFromObject(model);
const center = box.getCenter(new THREE.Vector3());
model.position.sub(center); // Esto mueve la masa geométrica al centro real.
```

### El "NormalTag" de C4D (Sombras Universales)
**Problema:** Modelos nuevos que, a pesar de tener `castShadow = true`, no proyectan sombras o estas se ven "rotas".
**Solución Maestra (Workflow de Exportación):**
1.  Todo modelo exportado desde Cinema 4D **DEBE** llevar aplicado un **NormalTag**.
2.  Este tag garantiza que las normales de los polígonos sean explícitas y perpendiculares a la cara.
3.  Sin este tag, Three.js puede interpretar erróneamente la dirección de la luz, anulando el cálculo de sombras proyectadas.
*Con el NormalTag aplicado, las sombras funcionan automáticamente sobre cualquier objeto.*

---

## ☁️ 5. ARQUITECTURA DISTRIBUIDA Y ESCALABILIDAD MASIVA (PWA)

Para soportar uso a nivel nacional (2M+ usuarios) con costo cero y sin depender del hardware de las escuelas, el sistema operará bajo el paradigma de **Edge Computing**.

*   **Aplicación PWA Móvil:** MAUNET vivirá incrustado en la PWA `www.netmarlyn.site` instalada en los celulares de estudiantes y maestros. El renderizado 3D ocurre al 100% en la GPU del teléfono personal.
*   **Protocolo "Solo JSON" (Zero-Audio Payload):** Para maximizar la escalabilidad, el servidor backend **JAMÁS enviará ni almacenará archivos de audio (MP3/WAV)**. La IA enviará únicamente un paquete ligero JSON que contiene texto y etiquetas de emoción.
*   **Decodificación Local:** El dispositivo móvil leerá el JSON y el navegador sintetizará el habla de manera nativa (Text-to-Speech / Web Speech API) generando el movimiento labial sincronizado de MAUNET en el cliente.
*   **Almacenamiento en Caché (Memoria de Roca):** Las respuestas recurrentes se almacenan. Cuando un usuario repite una consulta, el sistema devuelve inmediatamente el JSON almacenado sin despertar a la IA, asegurando latencia mínima.

---

## 📐 6. PRINCIPIOS DE CONSTRUCCIÓN

*   **Variables de Velocidad (`spd`):** Mantener una constante de velocidad (actualmente `0.075`) para que todos los movimientos tengan la misma inercia.
*   **Gestión de Memoria:** Si se cambian texturas o modelos al vuelo, usar siempre `.dispose()` en geometrías y materiales antiguos.
*   **Escalado Predictivo:** El modelo debe escalar en relación al alto de la pantalla (`size.y`), no por un valor fijo, para asegurar consistencia en móviles y monitores 4K.

---

## 🚀 6. HOJA DE RUTA 80% A 100% (ROADMAP FINAL)

> [!IMPORTANT]
> El desarrollo estricto a seguir a partir del Checkpoint V33.11 para llevar a MAUNET a su estado publicable (100%).

1.  **Prioridad 1: Sincronía Dinámica de Labios (Lip-Weights):** 
    *   *Objetivo:* Eliminar el "habla canina" (sólo mandíbula). Remapear y activar los huesos/pesos de los labios superiores e inferiores en el modelo durante el evento de habla `isSpeaking`, logrando un lip-sync orgánico real en lugar de sólo abrir la quijada.
2.  **Prioridad 2: Elemento Distractor de Latencia (La Computadora de MAUNET):** 
    *   *Objetivo:* Si el proceso RAG o la "incidencia de pensamiento" demora >1s, MAUNET debe girar su atención hacia un objeto 3D (pantalla holográfica o computadora lateral), indicándole visualmente al alumno que está buscando la información activa para enmascarar la latencia.
3.  **Prioridad 3: Implementación Offline Total (`concepts.bin`):** 
    *   *Objetivo:* La creación del motor Edge Computing real de plantillas procedimentales y descompresión de 90,000 conceptos locales para alivianar el clúster central (Arquitectura 98/2).
4.  **Prioridad 4: Integración Omnisciente NetMarlyn:**
    *   *Objetivo:* Fusión y enganche final del avatar con la PWA. Maunet debe tener la capacidad de leer la base de datos para recuperar reportes, estadísticas, notas y trabajos propios del alumno en tiempo real.

## 💡 7. CONFIGURACIÓN DE ILUMINACIÓN MAESTRA (DEFINITIVA - ESTÁNDAR 8 AM)

### Mandato de Iluminación
Las luces son **FIJAS en el espacio del mundo (World Space)**. Esta configuración fue validada como **PERFECTA** el 31 de marzo a las 8:00 AM y **NUNCA** debe ser modificada bajo ninguna circunstancia, ya que define el look cinematográfico anti-acné y dramático de MAUNET.

### Setup Maestro Blindado

| # | Nombre | Color Hex | Intensidad | Posición (X,Y,Z) | `castShadow` |
|---|--------|----------|-----------|-----------------|-------------|
| 0 | **Frontal** | `#fff6ee` | `1.1` | `(-3, 9, 6)` | ✅ **Sí (512px)** |
| 1 | **Cenital (Key)** | `#fff6ee` | `2.9` | `(-7, 7, 4)` | ✅ **Sí (512px)** |
| 2 | **Lateral (Fill)** | `#6181c2` | `1.4` | `(8, 2, 3)` | ❌ No |
| 3 | **Ambiente** | `#0a0808` | `0.85` | Global | ❌ No |

### Parámetros Críticos de Sombras y Render
- **`scene.background`:** `0x000000` (Negro Absoluto - Mandatorio para contraste).
- **`toneMappingExposure`:** `1.1`
- **`shadowMap.type`:** `PCFSoftShadowMap`
- **`shadow.mapSize`:** `512x512` (Optimización para rendimiento fluido).
- **`shadow.radius`:** `3` (Equilibrio entre suavidad y definición).
- **`shadow.bias`:** `-0.0005` / **`normalBias`:** `0.05` (Filtro Anti-Acné Avanzado)

### Efecto Logrado
- Máxima tridimensionalidad en el busto.
- Sombras profundas ricas en detalle pero suavizadas.
- Contraste absoluto contra el fondo negro (Look cinemático 80s).
- **Marco/Border:** `4px solid #4d5053` (gris acero oscuro)
- **Contenedor:** Lienzo panorámico de **555x400** centrado en pantalla, Newton ocupa ~85% del frame.

---

## 🧠 8. ARQUITECTURA DISTRIBUIDA Y UX DE LATENCIA RAG

### Cluster M5 y Cerebros Edge (Móviles)
El sistema opera bajo un balanceo de carga estricto. La charla casual repetitiva se resolverá vía **Cerebros Edge locales (LLMs de ~300MB a 600MB)** en los móviles avanzados. El **Clúster Backend (10 Mac Studios M5 64GB)** operará rígidamente por turnos y colas (Queue) para procesar exclusivamente respuestas documentales complejas y búsquedas en internet vía JSON.

### La Regla de Oro del 'Engaño Perceptual'
El ruteo hacia el clúster (RAG) generará tiempos de espera naturales (~8 segundos). Para sostener la atención y enmascarar la latencia:
1.  **Ley del Encuadre:** Fiel al estilo Max Headroom, MAUNET **jamás debe mostrar brazos ni manos** simulando teclear. Toda acción es sugerida.
2.  **Audio Ancla:** Ante la latencia, el navegador detonará primero un TTS local inmediato pre-cargado: *"Permíteme buscar esa información"*.
3.  **Elemento Distractor:** En el lienzo **555x400** aparecerá un asset holográfico 3D flotante (holograma digital, interfaz o barra de progreso porcentual) junto a su cabeza. MAUNET se girará con etiqueta `[PENSANDO]`, simulando interactuar con ella visualmente hasta recibir y leer el JSON final. 

---
## 🧠 9. MOTOR ORGÁNICO ESTOCÁSTICO (V33.5 - V33.11)
*La Ley del Movimiento Impredecible e Impecable.*

Para que un personaje 3D se sienta "vivo" y no robótico, MAUNET utiliza un motor estocástico (basado en la probabilidad y el azar).

### 9.1 Periodicidad vs Estocasticidad
- **PROHIBIDO:** Usar `Math.sin(time)` para el balanceo del cuerpo. El movimiento periódico es predecible y el cerebro humano lo detecta como "máquina" en menos de 5 segundos.
- **MANDATORIO:** Usar metas aleatorias (`THREE.MathUtils.randFloat`) asignadas cada N milisegundos. El movimiento resultante es irregular, asimétrico y parece fruto de la voluntad.

### 9.2 Parámetros de "Masa y Peso"
- **Interpolación (Lerp):** El valor de lerp para el cuerpo completo debe ser bajo (`0.015 - 0.020`). Esto evita movimientos "eléctricos" y simula la inercia de un busto físico. En V33.11 se fijó en **0.018**.
- **Multiaxialidad:** Maunet no solo se desplaza en X e Y; debe rotar levemente en X (Pitch) y Z (Roll) mientras habla para simular que se ladea y se inclina hacia el alumno.

---
## 📐 10. LA LEY DE RIGGING (ESTÁNDAR DE EJES)

Para garantizar que el motor de animación (**Lerp**) mueva a MAUNET de forma coherente, se establece el siguiente estándar de orientación para todos los joints con prefijo `xx-`:

1.  **PITCH (Eje X - Rojo):** 
    *   **Acción:** Movimiento de "Asentir" o "Galleteo".
    *   **Uso:** Apertura de mandíbula (`xx-jaw`), cabeceo (`xx-head`/`xx-neck`) y expansión de respiración (`xx-spine`).
2.  **YAW (Eje Y - Verde):** 
    *   **Acción:** Movimiento de "Negar" o "Giro".
    *   **Uso:** Rotación lateral de la cabeza para el seguimiento de la mirada (*Gaze Tracking*).
3.  **ROLL (Eje Z - Azul):** 
    *   **Acción:** Movimiento de "Inclinación lateral".
    *   *Uso:** Estabilización y micro-expresiones de curiosidad.

> [!NOTE]
> **Captura de Pose Inicial:** El sistema captura las coordenadas de diseño al cargar el modelo. Cualquier rotación aplicada por código se suma a la pose capturada, garantizando que el avatar no se desajuste independientemente de su rotación nativa en Cinema 4D.

---
## 🧠 10. PROTOCOLO DE PERSONALIDAD: ARTIFICIAL CHARISMA (V1.5)

MAUNET no es un tutor humanoide; es una **entidad digital carismática** inspirada en la estética Max Headroom (1985). Su comportamiento debe alternar entre fluidez técnica y fallos intencionales (glitches), priorizando el "cómo lo dice" antes que el contenido.

### Definición de Identidad
*   **Aparatosidad Visual:** 70% Max Headroom. Artificial, sarcasmo sano, cambios de tono inesperados.
*   **Fluidez Adaptativa:** Transiciones que oscilan entre movimientos orgánicos y cortes mecánicos (keyframes forzados).

### Los 8 Estados Base Procedurales
1.  **Sarcasmo / Max-Style:** Mirada asimétrica, ceja alta, sonrisa torcida (distorsión de comisuras).
2.  **Informativo Autoritario:** Mirada fija e intensa, cejas bajas, boca con apertura firme y seca.
3.  **Pensativo RAG (Escaneo):** Cabeza inclinada (Roll), cejas tensas, ojos hacia arriba (simula red de datos).
4.  **Aprobación Eufórica:** Apertura de mandíbula elástica, ambas cejas altas, micro-vibración de entusiasmo.
5.  **Duda / Pregunta Ambigua:** El gesto de *"Aaaahhh?"* largo con cabeza ladeada y boca abierta sin concluir el sonido.
6.  **Glitch de Cuerpo (The Displacement):** El avatar se desplaza súbitamente 3 unidades a la derecha por 0.1s y regresa.
7.  **Pose-Jump Glitch (Pop-Frame):** Cambio instantáneo a una pose facial extrema/distorsionada por 0.2s, regresando de inmediato a la pose informativa. Esto simula un error de carga de frames.
8.  **Repetición Retórica:** Dice la misma frase dos veces con distinta entonación (alegre vs. inquietante).
9.  **Pausa Vacía / Freeze:** Congelamiento absoluto de 1 frame a 2 segundos con mirada clavada en el usuario.

### Leyes de Interacción "Glitcheada"
*   **Corte Seco (Dry Cut):** Capacidad de detener una risa o gesto a la mitad y pasar a un estado serio instantáneamente.
*   **Microcortes:** Pérdida intencional de frames durante el habla para simular interferencia analógica.
*   **Desfase de Emoción:** Cambiar la expresión facial a mitad de una palabra (ej. empezar feliz y terminar gritando con cara neutra).
*   **Incomodidad Controlada:** Mezcla de humor artificial con pausas "vacías" de pensamiento para atraer la atención.

> [!IMPORTANT]
> **Regla de Oro de la Voz:** La voz debe usar desfases de *pitch* y *rate* (Web Speech API) de forma aleatoria para emular el salto magnético de una cinta de video antigua, sincronizado con espasmos en el hueso `xx-neck`.

---
## 🗣️ 11. ARQUITECTURA SEMÁNTICA "VOICE-TO-VOICE" (CÓMO HABLA MAUNET)

Esta sección documenta la **cúspide técnica** del proyecto: la transformación de un modelo 3D con movimientos aleatorios caóticos en un agente conversacional interactivo, lógico y sincronizado. Cualquier intento de recrear a MAUNET debe seguir esta arquitectura al pie de la letra.

### 11.1. El Problema Base: "El Ahogo Procedural"
Inicialmente, los movimientos del esqueleto (`Lerp Engine`) dependían de variables matemáticas aleatorias ciegas. Esto generaba un avatar fluido pero "desconectado" de la realidad: se movía por moverse, incapaz de reaccionar a la conversación humana o al contexto. 

### 11.2. El Motor de Inferencia RAG (Local Edge Computing)
Para dotarlo de cerebro sin depender de servidores de pago (evitando latencia masiva y costos de OpenAI), la arquitectura exige un entorno local:
*   **Motor:** Ollama ejecutándose localmente (o en clúster) sirviendo el modelo **LLaMA3**.
*   **Conexión:** Interrogación nativa vía `fetch` al puerto `http://localhost:11434/api/chat`.
*   **Zero-Audio Payload:** Para garantizar el rendimiento celular en la PWA, el LLM **JAMÁS** envía ni recibe audio (WAV/MP3). La red neuronal solo recibe texto del usuario y devuelve texto enriquecido con metadatos. El peso de la transferencia es de apenas unos Kilobytes.

### 11.3. El Parseo Semántico (El Mapeo Emocional)
El LLM está instruido (Prompt Engine) para no responder como un bot tradicional, sino interpretando un papel y usando "Etiquetas Emocionales" obligatorias antes de cada oración. 
*   **Ejemplos de salída del LLM:** `[PENSANDO] Mmm, déjame procesar eso. [PREGUNTA_ACTIVA] ¿Estás seguro de tu respuesta?`
*   **El Interceptor:** Una trampa de Expresiones Regulares (`Regex`) en el frontend JavaScript disecciona este texto puro, separa las oraciones y captura las etiquetas antes de que lleguen a la voz.
*   **La Matriz Vectorial (`EMOTION_MAP`):** Las etiquetas capturadas (Ej. `PENSANDO`) reescriben los objetivos numéricos del `Lerp Engine`. El movimiento deja de ser aleatorio y pasa a estar rígidamente parametrizado (Ej. Si piensa, la cabeza sube y las cejas se juntan).

### 11.4. Prevención del Colapso Acústico (El Reproductor Asíncrono)
**El Riesgo Fatal:** Al inicio, inyectar el texto del LLM directamente al Web Speech API generaba una "cacofonía" (el sistema escupía todas las frases al mismo tiempo o se cortaba abruptamente al sobrescribir el buffer del sistema operativo).
**La Solución (Cola Recursiva Pura):**
1.  Todo texto parseado se inyecta en un Array dinámico (`speechQueue`).
2.  El reproductor de voz toma **solamente el primer elemento** de la cola, y lee la voz de macOS/Windows.
3.  **El Secreto de la Asincronía:** El sistema de gesticulación entra en estado `isSpeaking = true`. El código *se sienta a esperar*. Solo cuando el evento nativo `utterance.onend` se dispara, indicando que MAUNET terminó de pronunciar la última sílaba, el sistema detona un `setTimeout` de 30ms para llamar recursivamente al siguiente elemento de la cola.
*Esta arquitectura en cadena impide solapar palabras y garantiza una fluidez robótica impecable.*

### 11.5. Sincronía Labial (Lip-Sync Procedural)
Mientras la bandera `isSpeaking` sea verdadera en la cola de reproducción, el hueso de la mandíbula (`xx-boca_quijada`) abandona el reposo y es forzado a oscilar usando una onda senoidal basada en el reloj del sistema:
`Math.sin(Date.now() * 0.02)`
Esto engaña al ojo humano asociando la apertura irregular de la mandíbula con la frecuencia de la voz sintética elegida.

### 11.6. Emparejamiento Biológico (Corte de Voz y Micrófono)
Para la conexión humana, se configuró el micrófono (Web Speech Recognition) bajo un paradigma "Push-to-Talk" (Interrupción Táctica):
1.  **Prioridad de Interrupción:** Al presionar la Barra Espaciadora, el sistema dispara `window.speechSynthesis.cancel()`, asesina la cola de texto entrante y apaga `isSpeaking`.
2.  **Escucha Activa:** Inmediatamente se levanta el micrófono, MAUNET adopta la emoción `[PENSANDO]` y comienza a escuchar al usuario, cerrando el lazo cibernético de manera natural y sin trabas.

---
## 🦴 12. TABLA DE NOMBRES REALES DE HUESOS (maunet.gltf) — MANDATO DE REFERENCIA

> [!IMPORTANT]
> Los nombres de huesos en el archivo GLTF exportado desde Cinema 4D usan **espacio**, no guión bajo. Los `includes()` en el `traverse` DEBEN usar la cadena exacta aquí documentada.

| Alias en Código | Nombre Real en GLTF | Eje Principal | Rol |
|---|---|---|---|
| `bones.head` | `xx-cabeza` | X (pitch), Y (yaw) | Cabeza principal |
| `bones.neck` | `xx-nuca` | X, Y (×0.4) | Nuca — sigue cabeza suavizada |
| `bones.spine` | `xx-pecho` | X, Y | Tórax / Respiración |
| `bones.jaw` | `xx-boca quijada` | X | Lip-sync y micro-vibración |
| `bones.cejaD` | `xx-ceja derecha` | pos.Y | Ceja derecha (posición) |
| `bones.cejaI` | `xx-ceja izquierda` | pos.Y | Ceja izquierda (posición) |
| `bones.shoulderR` | `xx-hombro derecho` | Z | Hombro derecho (encogimiento) |
| `bones.shoulderL` | `xx-hombro izquierdo` | Z | Hombro izquierdo |
| `bones.pomuloD` | `xx-pomulo derecho` | Libre | Disponible (V.futuro) |
| `bones.pomuloI` | `xx-pomulo izquierdo` | Libre | Disponible (V.futuro) |
| *(sin alias)* | `xx-labio superior der` | Libre | Disponible (V.futuro) |
| *(sin alias)* | `xx-labio superior izq` | Libre | Disponible (V.futuro) |
| *(sin alias)* | `xx-labio inferior der` | Libre | Disponible (V.futuro) |
| *(sin alias)* | `xx-labio inferior izq` | Libre | Disponible (V.futuro) |

---
## 🧠 13. MÓDULOS V2.7 — REFERENCIA RÁPIDA

| Módulo | Función Clave | Activación |
|---|---|---|
| Escucha Orgánica | `startListeningLoop()` | `recognition.onstart` |
| Escucha Orgánica | `stopListeningLoop()` | `recognition.onend` |
| Speech Spasms | `_speakChunk()` | Cada item de `speechQueue` |
| Thinking POV | `EMOTION_MAP.PENSANDO` ajustado a ≈25° | `callLLM()` onstart |
| Jaw micro-vibración | `animate()` → bloque jaw | `currentEmotionState === "PENSANDO"` |
| Error Glitch | Secuencia 5 sacudidas en `processSpeechQueue` | `chunk.emotion === "ERROR_GLITCH"` |
| Filtro Académico | `SYSTEM_PROMPT` constante en `callLLM()` | Cada llamada a LLaMA3 |

---

---
## 🌐 14. ARQUITECTURA HÍBRIDA MASIVA: MAUNET PARA 2 MILLONES DE ALUMNOS

> [!IMPORTANT]
> Esta sección documenta la **decisión arquitectónica más crítica del proyecto**. Fue definida, validada y blindada el 1 de abril de 2026. Ninguna decisión aquí puede revertirse sin consultar al arquitecto principal del sistema.

### 14.1. El Problema que se Resuelve
Un LLM (Ollama, LLaMA3, Gemma, Mistral) corriendo en un servidor centralizado **no puede atender 2 millones de consultas simultáneas** de forma eficiente ni económica. Transferir audio (MP3/WAV) a escala nacional satura cualquier infraestructura. La solución no es un servidor más grande: es **eliminar la dependencia del servidor para el 98% de las interacciones**.

### 14.2. El Principio Rector: 98/2 (Ley de Distribución)
- **98% de las interacciones:** Respondidas completamente dentro del teléfono del alumno. Sin internet. Sin servidor. Instantáneo.
- **2% de las interacciones:** Preguntas nuevas, nunca vistas, que requieren razonamiento profundo. Estas consultan al clúster Mac Studio.
- **Ley crítica:** Cada respuesta del 2% se incorpora automáticamente a la base de conocimiento global y se distribuye a todos los dispositivos en la próxima sincronización.

### 14.3. Motor de Inferencia Ligera (Edge Node)
Para operar con una instalación de **<150MB** y sin conexión a Internet, el dispositivo del alumno no ejecuta un LLM (Ollama), sino un sistema de **Simulación de Inteligencia Procedural** compuesto por tres piezas:

1.  **concepts.bin (La Memoria):** Un archivo comprimido que contiene el conocimiento académico (90,000 conceptos). No es un "pensador", es un "recordador".
2.  **LocalEngine.js (El Buscador):** Código ultraligero que busca coincidencias semánticas entre la voz del alumno y la base de datos local de forma instantánea.
3.  **variator.js (La Personalidad):** Motor de plantillas que "infla" los conceptos base para generar miles de variaciones de frases únicas, asegurando que MAUNET nunca suene repetitivo.

> [!IMPORTANT]
> **Invariabilidad de la Identidad:** El comportamiento 3D, el Motor Estocástico de movimiento y la personalidad de MAUNET son **independientes** de dónde venga la respuesta (Local o Servidor). El ADN de MAUNET vive en su archivo `MAUNET_IDENTITY.json`, garantizando que el personaje se vea, hable y actúe de forma idéntica con o sin Internet.

```
📱 TELÉFONO DEL ALUMNO (PWA instalada):
│
├── 🎭 MAUNET 3D (Three.js + maunet.gltf)
│
├── 📚 concepts.bin  ← Base de conocimiento comprimida
│   Estructura por concepto:
│   {
│     "id": "bio_fotosintesis_001",
│     "keywords": ["fotosintesis","clorofila","planta","luz","co2"],
│     "nucleo": "Las plantas convierten luz solar + CO2 + H2O en glucosa y O2",
│     "variaciones": [
│       "[AFIRMACION_INTENSA] Las plantas son máquinas solares...",
│       "[NEUTRAL] La fotosíntesis es el proceso donde...",
│       "[PREGUNTA_ACTIVA] ¿Sabías que sin fotosíntesis no existiría...",
│       "[PENSANDO] Interesante pregunta... analicemos la clorofila..."
│     ],
│     "emocion_sugerida": ["AFIRMACION_INTENSA","NEUTRAL","PREGUNTA_ACTIVA","PENSANDO"],
│     "grado": ["primaria","basico","bachiller"]
│   }
│
├── 🔍 LocalEngine.js  ← Motor de búsqueda semántica offline
│   Técnicas implementadas:
│   - Normalización: "fotosíntesis" = "proceso fotosintético" = "cómo hacen alimentos las plantas"
│   - Clustering: agrupa conceptos en familias temáticas para búsqueda rápida
│   - Cuantización: vectores de búsqueda comprimidos sin pérdida semántica
│   - Binarización: operaciones binarias para búsqueda ultrarrápida en móvil
│   - Indexación híbrida: keyword + semántica simultáneamente
│   Umbral de coincidencia: >75% → respuesta local. <75% → consulta servidor.
│
└── 🧠 variator.js  ← Motor de variación procedural de texto
    En runtime, por cada respuesta:
    - Elige longitud al azar (corta / media / larga)
    - Elige tono al azar (retórico / suave / directo / interrogativo)
    - Aplica plantillas + sustitución de sinónimos al núcleo del concepto
    - Genera texto único cada vez (nunca idéntico)
    Resultado: 4 variaciones base × motor runtime = variaciones prácticamente infinitas
```

### 14.4. Variación Procedural Total (Unicidad de Respuesta)

**Principio Absoluto:** Aunque el alumno pregunte lo mismo 10 veces seguidas, MAUNET debe responder diferente en texto, voz Y movimientos.

Esto se logra en 3 capas simultáneas:

| Capa | Mecanismo | Variaciones |
|:---|:---|:---|
| **Texto** | `variator.js` selecciona longitud + tono + sinónimos al azar | ~100+ por concepto |
| **Voz** | `pitch` y `rate` del TTS varían ±10% (Speech Spasms ya implementado) | Continuas |
| **Movimientos** | `EMOTION_MAP` usa rangos de huesos → valor al azar dentro del rango en cada frame | Infinitas |

**Resultado:** La misma información de fotosíntesis puede expresarse en miles de combinaciones únicas. El alumno nunca percibe repetición mecánica.

### 14.5. Las 3 Versiones de MAUNET por Nivel Académico

| Versión | Conceptos × Variaciones | Peso Estimado | Grados |
|:---|:---|:---|:---|
| **MAUNET PRIMARIA** | 9,000 × 4 | ~70MB | 1ro a 6to primaria |
| **MAUNET BÁSICO** | 18,000 × 4 | ~115MB | 7mo a 9no básico |
| **MAUNET BACHILLER** | 27,000 × 4 | ~200MB | 10mo a 12mo bachillerato |

La base total del sistema es de **90,000 conceptos académicos** cubriendo el currículo nacional oficial completo.

### 14.6. Instalación Progresiva (Progressive Loading Strategy)

**Problema a resolver:** No se puede pedir al alumno que descargue 200MB antes de usar la app. La primera experiencia debe ser inmediata.

**Solución: Instalación en 3 Fases Silenciosas**

```
FASE 1 — INSTALACIÓN INICIAL (~80MB, inmediata):
  - MAUNET 3D completo (modelo, texturas, código)
  - Primeros 20,000 conceptos (los más frecuentes y básicos)
  - MAUNET funciona al 100% desde el MINUTO 1

FASE 2 — DESCARGA BACKGROUND (silenciosa, 30-60 min después):
  - Service Worker descarga chunks de 5,000 conceptos cada 30 min
  - Ocurre mientras el alumno usa la app o con pantalla apagada
  - Background Fetch API: descarga aunque la app esté cerrada
  - El alumno nunca lo nota, nunca interrumpe su experiencia

FASE 3 — BASE COMPLETA (~6-8 horas después del primer uso):
  - 90,000 conceptos disponibles offline
  - Almacenados en IndexedDB del navegador
  - MAUNET opera al 100% sin internet
```

### 14.7. Sincronización Federada (Red de Aprendizaje Colectivo)

**La innovación más poderosa del sistema:** Los 2 millones de alumnos forman una red de inteligencia colectiva.

```
FLUJO DE APRENDIZAJE COLECTIVO:

Alumno A (Ciudad X) → Pregunta nueva (jamás hecha antes)
    ↓
LocalEngine: coincidencia <75% → consulta servidor Mac Studio
    ↓
LLM genera respuesta + 4 variaciones + etiquetas emocionales
    ↓
Nuevo concepto entra a la Base Global del servidor
    ↓
Sincronización horaria → todos los 2M celulares reciben el concepto
    ↓
1 hora después: Alumno B (Ciudad Y) hace la misma pregunta
→ LocalEngine responde LOCAL, sin consultar servidor ✅
```

**Frecuencia de sincronización:** Cada hora, en background, los dispositivos consultan si hay conceptos nuevos desde la última sync. Solo se descarga el delta (los nuevos), nunca la base completa.

### 14.8. Tecnologías PWA que Hacen Posible Esta Arquitectura

| Tecnología Web Estándar | Función en el Sistema |
|:---|:---|
| **Service Worker** | Intercepta requests, gestiona caché, descarga en background |
| **Background Fetch API** | Descarga chunks de conceptos aunque la app esté cerrada |
| **IndexedDB** | Base de datos local del navegador → almacena los 90,000 conceptos |
| **Background Sync API** | Sincronización horaria con el servidor para nuevos conceptos |
| **Cache API** | Caché de respuestas recientes para acceso instantáneo |

### 14.9. Infraestructura del Servidor (El 2%)

El servidor NO necesita atender 2 millones de consultas. Solo atiende el 2% genuinamente nuevo:

- **Carga estimada:** ~40,000 consultas únicas/día (2% de 2M)
- **Motor:** Ollama + LLaMA3 o Gemma3:9b en clúster Mac Studios
- **Output:** Solo JSON de texto + etiquetas emocionales (Zero-Audio Payload)
- **Auto-incorporación:** Cada respuesta nueva se añade automáticamente a la base global

### 14.10. Bug Pendiente Registrado (Prioridad Alta)

> [!WARNING]
> **BUG V2.7:** La mandíbula de MAUNET (`bones.jaw`) dejó de moverse durante el habla tras la implementación de V2.7. El avatar habla "entre dientes". Causa probable: conflicto entre el bloque `isSpeaking` y el nuevo bloque `PENSANDO` en el `animate()`. Debe corregirse antes de cualquier demostración pública. Adicionalmente, el movimiento de mandíbula debe ser más orgánico y errático (estilo Max Headroom), menos senoidal perfecto.

---

---
## 🧠 15. EL ADN DEL SISTEMA: MAUNET_IDENTITY.JSON (V4.2)

A partir de la V4.1, la identidad de MAUNET se desvincula del prompt rígido y se traslada a un archivo JSON dinámico. Esta es la **Única Fuente de Verdad** para su consciencia física y ética.

### Componentes del ADN:
1.  **Malla Física:** Define a MAUNET como un **BUSTO** sin extremidades inferiores ni brazos. Esto previene alucinaciones de movimiento.
2.  **Diccionario de Seguridad:** Contiene las palabras prohibidas y los conceptos inapropiados para menores de 9 años.
3.  **Fórmula de Rechazo Amable:** Establece el "Protocolo de Toreo" donde MAUNET rechaza temas obscenos o técnicos con amabilidad y redirige inmediatamente al alumno al área académica.
4.  **Memoria de Roca:** El sistema de síntesis semántica que permite a MAUNET tener "recuerdos de largo plazo" comprimidos sin saturar los recursos del cliente.

### Ley de Mantenimiento:
Cualquier cambio en la personalidad, vestimenta o límites de MAUNET debe realizarse en `MAUNET_IDENTITY.json`. El código en `main.js` solo debe encargarse de la interpretación de estos datos.

---

## 🏆 PUNTO DE CONTROL GOLD — 2026-04-03 (REFERENCIA MÁXIMA)

> **Este es el estado certificado, aprobado y protegido del sistema MAUNET.**
> **Tag GitHub:** `GOLD-MAUNET-V7.0-STABLE-PUNTO-DE-PARTIDA-CERTIFICADO`
> **Commit Base:** `ded8d52` — MAUNET V7.0 — Motor de Generación Espontánea

### Configuración Exacta Bloqueada

```
ILUMINACIÓN (NO TOCAR JAMÁS):
  frontLight: DirectionalLight(0xfff6ee, 1.1) — pos(-3, 9, 6)
  keyLight:   DirectionalLight(0xfff6ee, 2.9) — pos(-7, 7, 4)
  fillLight:  DirectionalLight(0x6181c2, 1.4) — pos(8, 2, 3)
  ambient:    AmbientLight(0x0a0808, 0.85)
  Shadows:    PCFSoftShadowMap, bias=-0.0005, normalBias=0.05

QUIJADA ESTOCÁSTICA (NO SIMPLIFICAR):
  cycleDuration: 200ms - 400ms (aleatorio)
  amplitude:     0.05 - 0.25 rad (aleatorio)
  pausa:         15% de probabilidad de boca cerrada momentánea

DERIVA ÓSEA (NO COLAPSAR EN UN HILO):
  8 hilos independientes: HEAD_X, HEAD_Y, CHEST_X, CHEST_Y,
                          BROW_D, BROW_I, SHOULD_R, SHOULD_L
  delay por hilo: 900ms - 1700ms (aleatorio)

SERVIDOR: python3 -m http.server 8082
MODELO LLM: llama3 en localhost:11434
```

### Regla de Oro para Futuros Desarrolladores

**Si necesitas ajustar el comportamiento verbal de MAUNET:**
- ✅ Modifica SOLO: `SYSTEM_PROMPT` y `num_predict` en `main.js`
- ❌ NUNCA toques: luces, quijada, deriva ósea, rigging

---

## 🔐 PROTOCOLO DE BACKUP AUTOMÁTICO A GITHUB (Para IAs Independientes)

Esta sección existe para que cualquier IA independiente (Jules, Antigravity, Cursor, etc.) pueda realizar un backup completo del proyecto sin necesidad de password ni configuración adicional. Todo lo necesario ya está dentro del repositorio.

### Credenciales y Ubicación

- **Llave SSH privada**: `./.git_ssh/id_maunet_key` (relativa a la raíz del proyecto)
- **Repositorio remoto**: `github.com:mauspeedway88/MAUNET.git`
- **Rama principal**: `main`
- **Carpeta raíz del proyecto**: `/Users/mauricio/ANTIGRAVITY_PROJECTS_folder/MAUNET_S`

### Comando Completo de Backup (Copiar y Ejecutar Tal Cual)

```bash
cd /Users/mauricio/ANTIGRAVITY_PROJECTS_folder/MAUNET_S && \
git add . && \
git commit -m "MAUNET — Backup Automático: [DESCRIPCIÓN DEL CAMBIO]" && \
env GIT_SSH_COMMAND='ssh -i "./.git_ssh/id_maunet_key" -o StrictHostKeyChecking=no' \
git push origin main --force
```

### Para Crear un Tag de Versión (Opcional pero Recomendado)

```bash
git tag -a MAUNET_TAG_VX.X -m "Descripción del hito técnico alcanzado adecuado a lo que se ha logrado hasta aqui."
env GIT_SSH_COMMAND='ssh -i "./.git_ssh/id_maunet_key" -o StrictHostKeyChecking=no' \
git push origin main --tags --force
```

### Reglas de Oro para el Backup

- Siempre ejecutar desde la carpeta raíz `/Users/mauricio/ANTIGRAVITY_PROJECTS_folder/MAUNET_S`.
- Nunca omitir el parámetro `GIT_SSH_COMMAND`; sin él, el push fallará por falta de autenticación.
- El mensaje del commit debe describir el cambio técnico real, no ser genérico.
- Ante cualquier duda, verificar primero con `git status` antes de hacer el commit.
- Gacer siempre un commint y backup completo de todo el workspase con icono y tag adecuado.
---
## 🧠 16. VISIÓN DE INTEGRACIÓN MAUNET + NETMARLYN (EL ANALISTA PEDAGÓGICO)

### 16.1 La Regla de Oro del 98/2 (Eficiencia Masiva)
Para garantizar escalabilidad nacional (2M+ alumnos) con costo cero de servidor y latencia mínima:
- **98% Local (Edge Computing):** Resolución inmediata de dudas educativas, conceptos escolares y charla casual mediante el motor local del dispositivo.
- **2% Server (Netmarlyn):** Consultas institucionales profundas, reportes estadísticos consolidados y "Máquina del Tiempo". Estas son las únicas que viajan al servidor mediante un flujo RAG.

### 16.2 UX de Latencia: El "Engaño Perceptual" Cinematográfico
Para mitigar y profesionalizar los 5-8 segundos de latencia en consultas al servidor:
1. **Activación de "Modo Analista":** MAUNET se gira parcialmente (atención lateral), simulando interactuar con una interfaz holográfica. Se activa un foco/luz de pensamiento sobre su cabeza.
2. **Audio Ancla Inmediato:** TTS local dice: *"Dame un segundo, estoy consultando los registros de Netmarlyn..."*.
3. **Feedback Visual:** Implementación de íconos o gráficas de carga HUD en el plano 3D.
4. **Retorno de Atención:** Al recibir el JSON, M---
## 🖥️ 17. SUBSISTEMA DE PIZARRA EDUCATIVA — THE CHALK ENGINE V8.0 (SVG DINÁMICO)

### 17.1 Filosofía de Diseño: Del Diccionario a la Libertad Infinita
MAUNET incorpora un sistema de apoyo gráfico que evolucionó en dos etapas:

- **V7 (Bóveda Limitada):** Se inició con 24 figuras dibujadas a mano en JavaScript puro (Canvas API). Eran perfectas pero limitaban a MAUNET a un catálogo rígido. Descartada.
- **V8 (SVG Dinámico Inline):** La IA genera código SVG vectorial directamente dentro de su texto de respuesta. JavaScript lo intercepta silenciosamente, lo normaliza al estilo tiza y lo renderiza en la pizarra 3D. Capacidad de dibujo: **ilimitada**.

### 17.2 Geometría 3D y Parámetros del Lienzo
- **Malla:** `PlaneGeometry(6, 4.2)` con material `MeshStandardMaterial` y `CanvasTexture` de `1200x840px`.
- **Color de fondo:** `#054322` (Verde Pizarra Institucional Netmarlyn).
- **Emisividad:** `0x000d08` (brillo sutil para integrarse con las luces de las 8AM sin romperlas).
- **Posición de Reposo:** `X=5.5, Y=0.8, Z=-2.1` con rotación `Y=-0.38 rad` (periférica, casi fuera de encuadre).
- **Posición Activa:** `X=2.5` (desliza hacia el frente mediante `MathUtils.lerp(0.05)`).

### 17.3 Coreografía Cinemática (The Chalk Choreography — Hardcoded)
Secuencia de tiempos estrictos orquestados vía `setTimeout`:
1. `T=0.0s` — La pizarra se desliza al centro (`goalPizarraX = 2.5`).
2. `T=1.0s` — MAUNET gira `2.18 rad` (125°) hacia la pizarra con `goalTargetRotY`.
3. `T=1.8s` — El SVG se renderiza en el cuadrante asignado del lienzo.
4. `T=4.8s` — MAUNET regresa a cámara (`goalTargetRotY = 0`).
5. `T=7.8s` — La pizarra se retira al reposo (`goalPizarraX = 5.5`). El dibujo **permanece acumulado**.

### 17.4 Motor SVG Dinámico — Flujo Técnico Completo
```
[Alumno habla] → [Ollama LLM] → [Texto + SVGs incrustados]
                                           ↓
                              [speakLLM() — Parser V8.0]
                                    ↙           ↘
                          chunk.type='text'   chunk.type='svg'
                                ↓                    ↓
                           [TTS voz]        [activarModoPizarra(svgString)]
                                                     ↓
                                          [normalizarSVG()] — fuerza tiza blanca
                                                     ↓
                                          [Blob URL → Image → drawImage()]
                                                     ↓
                                          [cuadrante 1-4 rotatorio]
                                                     ↓
                                          [pizarraTexture.needsUpdate = true]
                                                     ↓
                                          [Callback → continúa TTS]
```

### 17.5 Sistema de Cuadrantes (Composición Inteligente)
La pizarra se divide en 4 zonas de `42% x 42%` del lienzo total con margen. Cada SVG nuevo ocupa el cuadrante siguiente en orden rotatorio (`pizarraCuadrante % 4`):
- `Q1` Superior-Izquierda: `x=5%, y=5%`
- `Q2` Superior-Derecha: `x=53%, y=5%`
- `Q3` Inferior-Izquierda: `x=5%, y=53%`
- `Q4` Inferior-Derecha: `x=53%, y=53%`

Al ejecutar `[BORRAR]`, el contador de cuadrante se resetea a `0` y el lienzo vuelve a `#054322`.

### 17.1 Geometría y Estética Gold (V10.6)
La pizarra ha evolucionado a un componente físico 3D completo:
- **Lienzo (Canvas):** Plano de `4.2 x 2.94`.
- **Marco 3D:** Estructura envolvente de `4.35 x 3.1` en color **Gris Claro** (`#cccccc`).
- **Composición:** Ambos integrados en un `THREE.Group` (`pizarraGroup`) para animaciones síncronas.

### 17.2 Motor de Dibujo "Sketch-Core" (V11.0)
Diseñado para la velocidad (2-7s) y la estética de trazo manual:
- **Flash Sketch:** Usa colecciones artísticas de **Iconify** (MingCute-Line) que simulan trazos lineales a mano.
- **Turbo AI Sketch:** Modelo Turbo de Pollinations con prompt de **carboncillo minimalista** para obtener bocetos artísticos en <7s.
- **Tiza Nítida:** Filtro de normalización que fuerza el trazo blanco y ajusta grosores adaptativos según la escala del dibujo.

### 17.3 Coreografía y Coordenadas V10.6
MAUNET permanece en el centro (`X: 0`) y la pizarra se desplaza en una línea horizontal perfecta:
- **Altura (Y):** `1.3` | **Profundidad (Z):** `-3`.
- **Rotación:** `Y: -0.8` (Foco profundo), `X: 0` (Vertical).
- **Idle (Fuera):** `X: 12` | **Active (Clase):** `X: 2.9`.

### 17.4 Sincronización y Fail-safe
- **Stay-visible Fix:** La pizarra NO se retira hasta que el dibujo es confirmado.
- **Emergency Chalk:** Generación local de un círculo de tiza si fallan todas las APIs.

### 17.5 Pizarra Permanente y Coexistencia (V11.1)
- **Persistencia:** La pizarra **no se esconde** automáticamente después de dibujar. Permanece en el escenario (Active: `X: 2.9`) incluso cuando MAUNET vuelve a mirar al alumno (`RotY: 0`).
- **Coexistencia:** Está diseñada para coexistir espacialmente con futuras interfaces (como una computadora o paneles flotantes) sin interrumpir la escena.
- **Borrado Voluntario:** Solo desaparece si el alumno invoca explicitamente el borrado de pizarra (Modo Clear).

---
## 🔁 18. ESTADO ACTUAL DEL PROYECTO (CHECKPOINT V11.0 — 2026-04-05)

| Sistema | Estado |
|---|---|
| Motor 3D (Three.js) | ✅ Gold Lock |
| Iluminación 8AM | ✅ Intocable |
| Coreografía | ✅ V10.6 (MAUNET Estático / Pizarra Chic con Marco) |
| Coordenadas | ✅ V10.6 Oro (X: 12 a 2.9 / Y: 1.3 / Z: -3) |
| Motor de Dibujo | ✅ V11.0 Sketch-Core (Bocetos rápidos artísticos) |
| Acabado Visual | ✅ Marco Gris Claro (#cccccc) |
| Backup GitHub | ✅ Tag: `maunet_sketch_core_v11.0_final` |

---
## 🏫 19. MÓDULO 13 — LA PIZARRA MAESTRA INCREMENTAL (V1.3)

**Estrategia Técnica:** Migración de gráficos SVG pesados a un sistema de Fuentes Tipográficas de Iconos (Glyphs).

- **Concepto:** Cada ilustración educativa (corazón, árbol, motor, etc.) se almacena como un carácter de texto en un archivo `.woff2`. Esto permite tener más de 40,000 gráficos en solo 1.5MB, garantizando operatividad 100% Offline y carga instantánea (0.1ms).
- **Pipeline de Optimización:** Para agregar íconos personalizados desde fotos:
  1. **Photoshop:** Filtro Cutout/Median para eliminar ruido.
  2. **Umbral:** Conversión a silueta sólida.
  3. **Vectorización:** Generación de trazados limpios.
  4. **Ingesta:** Incorporación en `iconos_master`.
- **Composición CSS:** El motor de renderizado inyecta etiquetas `<i>` o `<span>` con coordenadas absolutas y estilo tiza blanca (`#F8F9FA` + `text-shadow` blanco sutil).

## 🏫 20. ESTADO GOLD: PIZARRA FLASHCARD V13.0 (SISTEMA DE RÁFAGAS)

> [!IMPORTANT]
> Esta configuración representa la culminación del sistema de apoyo visual de MAUNET, validada el 8 de abril de 2026. Prioriza el impacto pedagógico mediante imágenes masivas y efímeras.

### 20.1 Filosofía de "Flashcards"
A diferencia de versiones anteriores que buscaban una composición de cuadrícula o perspectiva, la V13.0 opera como un proyector de impacto único:
- **Unicidad:** Solo se muestra **un icono a la vez**.
- **Auto-Reemplazo:** Cualquier comando nuevo de dibujo invoca `limpiarPizarra()` antes de trazarse, eliminando el amontonamiento visual.
- **Efimeridad:** Los iconos tienen una vida útil de **5 segundos** (5000ms), tras los cuales se auto-borran del lienzo para devolver el foco a la cara de MAUNET.

### 20.2 Cinemática "Drop-Top" (Telón de Techo)
Se abandonó el desplazamiento lateral por una animación vertical más limpia y teatral:
- **Eje de Animación:** Eje **Y**.
- **Estado Oculto (Arriba):** `goalPizarraY = 12` (Fuera del encuadre superior).
- **Estado Activo (Frente):** `goalPizarraY = 1.3`.
- **Coordenadas Fijas:** `X = 2.9, Z = -3`.
- **Sincronía de Cierre:** La pizarra **solo se oculta** cuando Maunet termina de hablar (`isSpeaking = false`) y tras un margen de seguridad de 5 segundos adicionales.

### 20.3 Parámetros Gráficos y Renderizado
- **Tamaño Flashcard:** Estático a **600px** (Escala masiva para máxima legibilidad).
- **Posicionamiento:** Siempre centrado (`CC`).
- **Color de Tiza:** `rgba(255, 255, 255, 0.92)` con `shadowBlur = 18`.
- **Traductor de Conceptos (`MAUNET_ICON_MAP`):** Mapeo estricto para evitar fallos de búsqueda (ej: "sol" -> "sun", "lluvia" -> "cloud-rain").

### 20.4 Lógica de Inferencia (LLM Prompting 10/10)
- **Sintaxis Simplificada:** `[ICON:nombre]` (sin parámetros de posición).
- **Frecuencia Visual:** Nivel 10/10. Instrucción imperativa de usar de 3 a 4 iconos por párrafo.
- **Modo Híbrido:** Maunet decide cuándo usar la pizarra; si la plática es casual o técnica, la pizarra permanece oculta. Solo salta a escena para temas didácticos (ciencias, animales, transporte).

---
## 🏆 22. ESTADO GOLD V33.11 — HITO 80% COMPLETADO (CHECKPOINT FINAL)
*Fecha: 8 de abril de 2026 | Responsable: Antigravity*

| Sistema | Versión | Estado | Descripción |
|---|---|---|---|
| **Motor 3D** | v0.160.0 | ✅ ESTABLE | Renderizado PBR con PCFSoftShadowMap. |
| **Iluminación** | V33.11 | ✅ GOLD | Setup frontalizado (Z=5/8) para máxima claridad. |
| **Motor Orgánico** | V33.11 | ✅ STOCHASTIC | Metas aleatorias cada 600-1400ms. Lerp 0.018. |
| **Rosetta Engine** | V33.0 | ✅ MASTER | 1,696 iconos Messenger. Búsqueda semántica resiliente. |
| **Terminal UI** | V33.10 | ✅ FIXED | Altura 120px estática con auto-scroll corregido. |
| **Audio/Habla** | V33.8 | ✅ CALIBRADO | utternace.rate = 0.76 (Pacing Pedagógico). |

**MANDATO FINAL:** Este es el punto de partida certificado para la fase de cierre (90-100%). Cualquier modificación estética o de movimiento debe ser cautelosa para no romper la naturalidad alcanzada.

---
**FIN DEL DOCUMENTO - MANUAL DE CONSTRUCCIÓN**

---

## 🎭 23. MOTOR DE ANIMACIÓN FACIAL V36.5 (CEJAS, SUAVIZADO Y DIAGNÓSTICO LABIAL)

> [!IMPORTANT]
> Esta sección documenta el estado actual (2026-04-10) del sistema de expresión facial.
> Los cambios de cejas y suavizado están **ACTIVOS en código**. Los labios están **PENDIENTES**.

### 23.1 Arquitectura de Bones Labiales (Nuevo Modelo)

El archivo `maunet.gltf` fue actualizado a una versión con arquitectura ósea facial expandida.
Los nuevos joints están nombrados con **guión bajo** (no espacio):

```
xx-boca quijada  (padre)
├── xx-labio_superior    → bones.lipSup   (labio superior)
├── xx-labio_inferior    → bones.lipInf   (labio inferior)
├── xx-labio_derecho     → bones.lipD     (comisura derecha)
├── xx-labio_izquierdo   → bones.lipI     (comisura izquierda)
├── xx-pomulo_derecho    → bones.pomuloD  (pómulo derecho)
└── xx-pomulo_izquierdo  → bones.pomuloI  (pómulo izquierdo)
```

> [!WARNING]
> Los joints labiales son `isBone: true` en Three.js pero **NO responden a cambios de `position`** de manera visible. Valores de ×20 aplicados y sin efecto visual comprobado. Ver sección 23.4 (Diagnóstico Pendiente).

### 23.2 Sistema de Cejas — Parámetros Gold V36.5

Los parámetros de comportamiento de las cejas son los únicos de la zona facial que operan correctamente en el nuevo gold state:

| Parámetro | Valor | Efecto |
|---|---|---|
| **Rango estocástico arriba** | `+1.1` | Máxima elevación expresiva |
| **Rango estocástico abajo** | `-0.3` | Fruncido leve |
| **Multiplicador de aplicación** | `× 0.22` | Desplazamiento real máx: `±0.242 unidades` |
| **Velocidad de lerp (quieto)** | `browSpd = 0.025` | Transición suave |
| **Velocidad de lerp (hablando)** | `browSpd = 0.035` | Reactiva al habla |

**Código de aplicación (main.js):**
```javascript
if (bones.cejaD) bones.cejaD.position.y = initialPos[bones.cejaD.uuid].y + (currentTargets.browD * 0.22);
if (bones.cejaI) bones.cejaI.position.y = initialPos[bones.cejaI.uuid].y + (currentTargets.browI * 0.22);
```

**Sincronización entre cejas (V31.4):**
- 70% de eventos: ambas cejas suben/bajan al mismo valor (expresión unificada)
- 30% de eventos: solo una ceja sube (expresión asimétrica / escéptica)

### 23.3 Suavizado Independiente por Hueso (V36.5)

Sistema de velocidades de lerp por grupo de huesos para eliminar cambios bruscos de dirección:

```javascript
// En el loop animate() — Cada frame
const headSpd   = isSpeaking ? 0.028 : 0.022;  // Cabeza
const neckSpd   = isSpeaking ? 0.020 : 0.015;  // Nuca/Torso
const browSpd   = isSpeaking ? 0.035 : 0.025;  // Cejas
const shouldSpd = isSpeaking ? 0.015 : 0.010;  // Hombros

currentTargets.head.x  = lerp(currentTargets.head.x,  goalHeadX,   headSpd);
currentTargets.head.y  = lerp(currentTargets.head.y,  goalHeadY,   headSpd);
currentTargets.chest.x = lerp(currentTargets.chest.x, goalChestX,  neckSpd);
currentTargets.chest.y = lerp(currentTargets.chest.y, goalChestY,  neckSpd);
currentTargets.browD   = lerp(currentTargets.browD,   goalBrowD,   browSpd);
currentTargets.browI   = lerp(currentTargets.browI,   goalBrowI,   browSpd);
currentTargets.shouldR = lerp(currentTargets.shouldR, goalShouldR, shouldSpd);
currentTargets.shouldL = lerp(currentTargets.shouldL, goalShouldL, shouldSpd);
```

> [!NOTE]
> Los labios usan `lipSpd = 0.25` (rápido, para que los visemas se perciban nítidos durante el habla). Los pómulos usan `tSpd` (velocidad general).

### 23.4 Diagnóstico Pendiente: Labios Sin Respuesta Visual

**Síntoma:** Los joints labiales (`bones.lipSup`, etc.) son detectados correctamente (`isBone: true`), los valores goal se actualizan correctamente, pero el modelo 3D no muestra deformación visual incluso con valores extremos (×20).

**Hipótesis confirmadas y descartadas:**
- ❌ `isBone: false` → Descartada. Todos muestran `isBone: true` en consola.
- ❌ Detección fallida → Descartada. Los logs confirman detección correcta.
- ⚠️ **Pesos de skin nulos o insuficientes en el rig de C4D** → Probable causa raíz.
- ⚠️ **Espacio local del bone incorrecto** → Los joints son hijos de la quijada; su eje local puede estar orientado de forma que los desplazamientos en Y/X del espacio local no produzcan deformaciones visibles en la malla.

**Siguiente paso recomendado (Sesión #061):**
1. Abrir el archivo `.c4d` del modelo en Cinema 4D.
2. Seleccionar `xx-labio_superior` y mover manualmente en cada eje (X, Y, Z) para identificar qué eje produce deformación visible en la malla.
3. Verificar el peso de skin sobre los vértices de la zona de los labios para `xx-labio_superior` y sus hermanos.
4. Exportar de nuevo si se detecta que los pesos son nulos.

> [!CAUTION]
> NO intentar controlar los labios con `rotation` sin conocer el eje correcto de cada joint. Los experimentos de esta sesión con `rotation.z` produjeron deformaciones geométricas extremas que rompieron la apariencia del modelo.

### 23.5 Estado Actual del Sistema Facial (Gold V36.5)

| Componente | Sistema | Estado |
|---|---|---|
| Quijada (lip-sync) | Rotación X senoidal estocástica | ✅ Funcional |
| Cejas | Posición Y con rango (-0.3, +1.1) × 0.22 | ✅ Funcional |
| Hombros | Rotación Z asimétrica | ✅ Funcional |
| Labios (4 joints) | Pendiente calibración C4D | ⏳ Pendiente |
| Pómulos (2 joints) | Pendiente (junto con labios) | ⏳ Pendiente |
| Sonrisas / Visemas | Código listo, no visible por labios pendientes | ⚙️ Listo pero invisible |

**Tag de backup de este estado:** `MAUNET-V36.5-GOLD-CEJAS-SUAVIZADO`

---

## 24. Coreografía de Latencia (Ghost Loading V38.0)

Debido al retraso intrínseco de llamar a modelos de lenguaje (RAG / Ollama) sobre bases de datos complejas locales (entre 4 a 12 segundos), se implementó un sistema de **engaño cinemático o "Ghost Loading"** para mantener inmerso y entretenido al alumno mientras se procesa la información en *background*:

### 24.1 Flujo Secuencial Asíncrono
1. **Disparo:** El sistema HTTP inicia un timeout auxiliar paralelo al `fetch()`. Si Ollama no ha contestado en más de `1000ms`, se dispara el evento.
2. **Computadora entra en Escena:** La propiedad `goalMacX` se desplaza lateralmente hasta invadir la escena (`-4`).
3. **Audio de aviso de Latencia:** Maunet dice en voz alta: *"Un momento por favor, Mauricio"*, usando un `.speakLLM` manual **mientras te sigue mirando fijamente**.
4. **Giro del Actor (Turn-To-Mac):** Aproximadamente 2000 milisegundos después de emitido el audio de aviso, Maunet gira TODO su cuerpo hacia la computadora al invocar `goalTargetRotY = -2.18`.
   - **Crucial:** Maunet **NO puede regresar a mirar al oyente** al finalizar de hablar esta frase, por lo que bloqueamos la salida estándar (`if (!window.latencyActive) goalTargetRotY = 0;`) de su sistema gestual, forzándolo a mantenerse volteado hacia la Mac hasta nuevo aviso.
5. **UI de Carga Rápida CSS:** Al voltearse (pasado un segundo de girar), un DIV `#rag-progress` que flota exactamente por encima de la computadora en verde neón comienza a incrementar falsamente un porcentaje (`[ 0% ] -> [ 85% ] -> [ 99% ]`).
6. **Desmonte Estético (Resolución del LLM):** En el mismo milisegundo en que el backend recibe los datos correctos de la respuesta HTTP:
   * El HUD del progreso numérico se destruye `display: none`.
   * Maunet exclama verbalmente: *"¡Lo tengo!"*, **todavía mirando la computadora**.
   * Exactamente 1.5 segundos después de emitir esa frase, Maunet se gira a la cámara (`goalTargetRotY = 0`), la computadora sale de la escena y se procesa el speech de respuesta completa.

---

## 25. Fondo de Video Dinámico (Max Headroom Style V39)

Para elevar la estética visual a un nivel retro-futurista sin impactar el rendimiento de la GPU en dispositivos móviles, se implementó una arquitectura de "Capas Híbridas" (3D sobre 2D):

### 25.1 Configuración del Motor (Alpha Transparency)
El mundo 3D ya no es un bloque sólido. Se modificó la instancia del `WebGLRenderer` en `main.js` para permitir transparencia:
- **Código:** `const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });`
- **Anulación de Fondo:** Se comentó la línea `scene.background = new THREE.Color(0x000000);`. Esto convierte el fondo del canvas en un "cristal" transparente.

### 25.2 Layering y CSS (Z-Index)
Se inyectó una etiqueta `<video>` en el `index.html` situada físicamente detrás del canvas 3D:
1. **Contenedor:** `#scene-container` tiene `z-index: 1` y `position: relative`.
2. **Video:** Posee `z-index: -1` y `object-fit: cover` para asegurar que llene el marco de 555x400 sin deformarse.
3. **Atributos:** `autoplay loop muted playsinline` (obligatorios para compatibilidad con iOS/PWA).

### 25.3 Optimización de Procesamiento (Software Downspeed)
Para ahorrar batería y peso de archivo, se utiliza una técnica de desaceleración por software:
- Se capturan/generan videos en cámara rápida (ej. 60fps) y se les aplica un `playbackRate = 0.4` (o 0.3) mediante un micro-script en el `index.html`.
- **Efecto:** Movimientos hipnóticos súper suaves con archivos MP4 de pocos kilobytes.

### 25.4 Calidad Visual (Super Sampling)
Se estableció como estándar el uso de videos con resolución ligeramente superior al contenedor (ej. **832x600** para un marco de 555x400). 
- **Razón:** Esto genera un efecto de nitidez extra (similar al anti-aliasing) en pantallas de móviles con alta densidad de píxeles, evitando que el fondo se vea borroso al escalarse.

### 25.5 Pizarra Neutra de Alta Fidelidad (V39.4)
Para garantizar que el fondo de la pizarra sea oscuro pero los íconos mantengan sus colores originales vibrantes, se aplica una configuración técnica estricta:

1. **Jerarquía de Color:**
   - **Marco (Borde 3D):** Gris Medio-Claro `#55565a` (Para contraste y volumen).
   - **Centro (Lienzo):** Gris Carbón Oscuro `#2c2c30`.
2. **Material Desacoplado:** Se utiliza **`MeshBasicMaterial`** en lugar de materiales con luces (como Phong o Standard). Esto asegura que la iluminación de la escena no "lave" los colores del canvas.
3. **Fidelidad de Textura (ColorSpace):** Es obligatorio marcar el `pizarraTexture.colorSpace = THREE.SRGBColorSpace`.
   - *Por qué:* Sin esto, Three.js aclara automáticamente los colores oscuros por corrección gamma, destruyendo el tono carbón buscado.
4. **Renderizado de Iconos:** Los iconos se inyectan en crudo vía `ctx.drawImage` sin filtros de `brightness`, `contrast` o `shadowBlur`. Esto permite que el motor Rosetta (ES/EN Interceptor) muestre los activos visuales con su paleta original.

### 25.6 Vocabulario Visual y Prioridad de Renderizado
El flujo de visualización de íconos obedece al interceptor NLP (función `speakLLM` llamando a `findUniversalIcon`).
Existen varios mapas, pero la búsqueda de iconos emplea una estricta precedencia:
1. **`ROSETTA_HOTFIX` (Capa 0):** Alta prioridad; controla anomalías ortográficas y mapeos directos forzados de SVG. (Responsable de la expansión visual `V39.7` a casi mil términos interactivos en español).
2. **`EMOJIS_ES` / `EMOJIS_EN` (Capa 1/2):** Mapeo generalizado en diccionarios externos puente.

> [!WARNING]
> Cualquier expansión futura del léxico que represente íconos `.svg` de `iconos_messenger_full` DEBE inyectarse explícitamente dentro del diccionario prioritario `ROSETTA_HOTFIX` en `main.js`. El antiguo mapa genérico `MAUNET_ICON_MAP` no es interpretado por el actual renderizador offline de messenger.

### 25.7 Seguridad Anti-Condiciones de Carrera (Giro Mac/RAG)
Para secuencias animadas largas intercaladas con eventos asíncronos (como el tiempo invertido en el sintetizador TTS y consultas externas RAG):
*   Los callbacks de giro físico (`goalTargetRotY`) deben ser **absolutos y temporizados** mediante `setTimeout` independientes. NUNCA deben encadenarse ciegamente al evento `onend` del TTS en rutinas híbridas de espera, pues desincronismos a nivel de milisegundos pueden envasar el estado `isSpeaking` global, paralizando al tutor de espaldas (como ocurría en versiones previas a la `V39.6`).

---

## 💾 26. ARQUITECTURA DE RETENTIVA CRONOLÓGICA (COLD STORAGE V44.0)

Para blindar la estabilidad del dispositivo destino (PWA) de la sobresaturación inherente a miles de registros temporales (límite físico de `localStorage` y de la RAM de navegadores móviles), MAUNET emplea un paradigma de "Cold Storage Offloading".

### 26.1 Ventana Operativa de Cinco Días
El frontend JavaScript de la aplicación posee un límite vital: **solo debe preservar los recuerdos de los últimos cinco días**.
* Todo lo reciente (≤ 5 días) permanece inyectable al vuelo para búsquedas instantáneas cronológicas usando la Ley de Prioridad JS de `searchMemoryExplicit`.

### 26.2 Ruteo de Archivo `offloadOldMemories`
El sistema evalúa pasivamente la antigüedad por cada carga/arranque.
1. Localiza toda la bitácora `ts` cuya fecha supera el umbral matemático `5 * 24 * 60 * 60 * 1000` (ms).
2. Empaqueta el sobrante histórico en un array y lo envía en *background POST* a `http://localhost:8082/api/archive-memory`.
3. Inmediatamente atiranta un garbage collection frontend: mutila la lista y retiene el buffer local aséptico al ejecutar un recálculo de Indexed/localStorage.

### 26.3 Backend de Concatenación JSON (Servidor Python)
El puerto delegado `8082` maneja asíncronamente el archivo perpetuo de metadatos educativos por cada alumno, generando y actualizando atómicamente el documento `LONG_TERM_MEMORY_[CARNET_ID].json` para acopiar el crecimiento de memoria sin saturar terminales físicas ni incordiar el LLM con la asimilación del Big Data.
