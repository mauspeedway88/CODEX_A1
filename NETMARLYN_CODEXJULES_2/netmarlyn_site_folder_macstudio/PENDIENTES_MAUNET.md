# 🚀 LISTA DE TAREAS PENDIENTES — MAUNET (The Agent)

Este documento es el tablero de control de objetivos incrementales. A diferencia de la bitácora, aquí se registran las metas futuras y mejoras de comportamiento pendientes que debemos resolver sesión tras sesión.

---

## 📅 PENDIENTES CRÍTICOS (AGENDA PRÓXIMA SESIÓN)

1.  **[ ] MEJORAR TIEMPO DE RESPUESTA Y LIP SYNC (MAUNET PÚBLICO):**
    - Reducir el tiempo de latencia.
    - Arreglar el fallo en la sincronización de labios de Maunet Público.
2.  **[ ] ELIMINAR EL "FREEZE" INICIAL (7-12 SEGUNDOS DE SILENCIO):**
    - Evitar que Maunet se quede quieto y callado al inicio.
    - Implementar un saludo inmediato ("Hola") o preguntar el nombre del usuario al instante para registrarlo en la sesión.
    - Llamar al usuario por su nombre real registrado en lugar del genérico "Mauricio".
3.  **[x] GESTUALIDAD DE APROBACIÓN/NEGACIÓN:** ✅ COMPLETADO
    - Hacer que Maunet pueda decir físicamente "SÍ" (asentir, eje PITCH) y "NO" (negar, eje YAW).
    - Habilitarlo para que lo haga si el usuario se lo pide directamente, o que lo haga de forma orgánica al emitir respuestas afirmativas/negativas. 
2.  **[x] MODO "ESCUCHA ACTIVA" (LEAN-IN):** ✅ COMPLETADO
    - Cuando el usuario empiece a escribir o a hablar por el micrófono, Maunet debe acercarse a la cámara levemente ("lean in" sobre el eje Z / Scale).
    - Objetivo: Enfatizar que está prestando atención directamente al usuario de frente.
    - Levantar las cejas levemente en este estado.
    - Mantenerlo orgánico (fluido/estocástico), no una estatua rígida.
3.  **[ ] COMANDOS FÍSICOS A PETICIÓN (ACTION HOOKS):**
    - Si el usuario le pide explícitamente a Maunet que realice un movimiento ("levanta los hombros", "mueve la cabeza", etc.), detectar esa intención y ejecutar físicamente la acción en el canvas 3D.
4.  **[ ] ACTIVACIÓN ORGÁNICA DE HOMBROS:**
    - Hacer que Maunet mueva los hombros a lo largo de la rutina (estocástica y al hablar), ya que anteriormente se mantenían estáticos.
5.  **[ ] ASENTIMIENTO EDUCATIVO ORGÁNICO:**
    - Lograr que Maunet asienta con la cabeza (decir que "SÍ") orgánicamente unas 2 o 3 veces mientras está explicando un tema educativo.
6.  **[ ] PIZARRA INCREMENTAL (GRID SYSTEM):**
    - **CUADRICULAR LA PIZARRA:** Mapear y dividir la pizarra mediante coordenadas matemáticas/CSS para establecer un sistema de grillas sólido para la instancia de iconos tipográficos.
7.  **[x] MEMORIA DE CONVERSACIONES (SÍNTESIS JSON / MEMORIA DE ROCA V2.0):** ✅ COMPLETADO V40.0
    - Implementado sistema de persistencia incremental en `localStorage` con síntesis automática de keywords.
    - Evaluación proactiva de memoria + búsqueda explícita bajo demanda.
    - Persistencia triple: `beforeunload` + `visibilitychange` + autoguardado cada 3 min.
8.  **[ ] MOTOR DE CONCEPTOS EDUCATIVOS OFFLINE (JSON):**
    - Desarrollar la capacidad de leer un listado base de conceptos. Gracias a estas 3 o 5 palabras clave actualizadas por alumno, Maunet podrá generar y platicar de un tema educativo completo sin conectarse al servidor.

---

## ✅ METAS ALCANZADAS (LOGS DE ÉXITO)

-   **[x] RECALIBRACIÓN DE ILUMINACIÓN:** Luces desplazadas para limpiar sombras faciales. (V39.7)
-   **[x] OPTIMIZACIÓN DE MOVIMIENTOS 3D:** Suavizado de nuca y Jaw-Sync orgánico. (V39.7)
-   **[x] REFINAMIENTOS VISUALES:** Suavizado de mallas y balance de brillo finalizados (IA Externa).
-   **[x] AUTOCONSCIENCIA DIGITAL (AUTO-ID):** Maunet sabe que es un modelo 3D y reconoce su volumen. (V3.8)
-   **[x] INTERACTIVIDAD HUMANO-MÁQUINA:** Layout vertical y respuestas de Max Headroom integradas. (V3.8)
-   **[x] DEPURACIÓN NLP SEMÁNTICA:** Singularización heurística de plurales y tolerancia a expresiones compuestas en `findUniversalIcon()`. (V39.8)
-   **[x] MEMORIA DE ROCA V2.0:** Persistencia incremental por usuario con localStorage, síntesis automática de keywords, evaluación proactiva inteligente, saludo contextualizado. (V40.0)

---

## 📈 BACKLOG (PLANIFICACIÓN A LARGO PLAZO)

- [ ] Migrar localStorage a IndexedDB cuando el historial supere 5MB (Memoria de años). Base: Memoria de Roca V2.0 ya operativa.
- [ ] Optimizar el sistema para la PWA Netmarlyn (Carga progresiva).
- [ ] Refinar las sombras para dispositivos móviles de gama baja.

---
**Recuerda Jules:** Al iniciar cada sesión, lee este archivo primero y presenta estas tareas al Arquitecto.
