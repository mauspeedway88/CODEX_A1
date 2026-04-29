# 🛠️ BITÁCORA DE FALLOS CRÍTICOS Y REPUESTOS — MAUNET 🛠️

Este documento es la "Caja Negra" técnica de MAUNET. Aquí se registran los errores críticos (Bugs) y sus soluciones exactas para evitar regresiones o colapsos totales del motor 3D.

---

## 🚨 BUG V6.5-CRASH-ASYMMETRY (EL GRAN APAGÓN)
- **SÍNTOMA**: El sistema carga la interfaz y el chat, pero el contenedor 3D se queda en negro absoluto.
- **CAUSA RAÍZ**: Error de referencia (`ReferenceError: goalShouldL is not defined`). Se intentaron usar hilos de animación independientes para el hombro izquierdo sin haber declarado las variables globales `goalShouldL` y `currentTargets.shouldL` al inicio de `main.js`.
- **REPARACIÓN (V6.7)**: 
    1. Declarar TODAS las variables de meta (`goal...`) al inicio del archivo.
    2. Implementar 'Null-Checks' en el bucle `animate()`: `if (bones.shoulderL && initialRots[bones.shoulderL.uuid])`. Esto evita que el motor Three.js colapse si un hueso aún no está listo.

---

## 🚨 FALLO DE CARGA DE ACTIVOS (MISSING MODEL)
- **SÍNTOMA**: El contenedor 3D muestra un recuadro negro o vacío tras un commit.
- **CAUSA RAÍZ**: Eliminación accidental de archivos binarios (`.gltf`, `.onnx`, `.c4d`) durante el proceso de Git.
- **PROTOCOLO DE RESCATE**: 
    - `git checkout HEAD~1 -- MAUNET_SITE_S/maunet.gltf`
    - `git checkout HEAD~1 -- MAUNET_SITE_S/voices/`

---

## 🚨 ERROR DE MAPEO DE ADN (PROCEDURAL GREETINGS)
- **SÍNTOMA**: MAUNET solo repite el mensaje de fallback ("sistema en línea") y no usa los saludos aleatorios del JSON.
- **CAUSA RAÍZ**: Referencia errónea en `main.js`. El código buscaba en `MAUNET_ID.logic_protocols` mientras que el JSON usaba la clave `safety_protocols`.
- **REPARACIÓN (V5.6)**: Sincronizar el nombre del objeto en el script con el del JSON de identidad.

---

## 🛠️ REGLAS DE ORO DE INGENIERÍA (PARA JULES):
- **ORDEN DE DECLARACIÓN**: Antes de usar un nuevo hueso en `startBoneDrift`, debe existir su `goal` y su `currentTarget` al inicio.
- **CONSTANTE DE MOVIMIENTO**: Para evitar que parezca "muerto", la velocidad de lerp (`tSpd`) debe ser baja (0.05) para que siempre esté en transición hacia su meta aleatoria.

---
**Ultima actualización: V6.7 — Blindaje de Hombros y Asimetría Genuina.**
