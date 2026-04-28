# 🛰 NETMARLYN — STATE SNAPSHOT v1.0
**Generado:** 13 de Marzo, 2026 | **Para:** Transferencia operativa de contexto IA-a-IA

---

## 1. PROJECT_ID
`NETMARLYN-PWA-LOCAL-CLOUDFLARE-2026`

---

## 2. PROJECT_OBJECTIVE
Sistema de **gestión escolar digital On-Premise** (PWA + servidor Python local en Mac Mini) accesible globalmente vía Cloudflare Tunnel. Permite subir listas de alumnos, asignar IDs QR únicas, capturar fotos, y verificar identidades en tiempo real mediante escaneo de cámara o código manual. Sistema operativo 24/7 sin instalación de apps.

---

## 3. USER_INTENT_MODEL
- **Operador:** Mauricio (no programador). Actualiza el sistema sustituyendo carpetas.
- **Usuarios finales:** Directores/maestros/guardias en colegios.
- **Meta real:** Escanear el QR del carnet de un alumno con el celular y ver en 2 segundos: foto + nombre + grado.
- **Restricciones clave:** Sin frameworks JS pesados. Sin cloud de pago. Sin instalación de apps.
- **Credenciales demo:** A123/pepino1 (San Isidro) · B456/pepino2 (Los Andes)

---

## 4. PROJECT_MATURITY_STAGE
`IMPLEMENTATION → OPTIMIZATION`

---

## 5. CORE_PROJECT_PRINCIPLES — REGLAS ABSOLUTAS
> ⛔ VIOLAR CUALQUIERA DE ESTAS REGLAS ROMPE EL SITIO INMEDIATAMENTE

1. **ESCUDO HTTP:** El método `send_response()` en `netmarlyn_server.py` está sobrescrito. Inyecta headers Anti-Cache y CORS DESPUÉS del status code. NUNCA agregar `send_header()` antes de `send_response()`. NUNCA quitar el override.
2. **PUERTO 9300:** Cloudflare Tunnel apunta aquí. No cambiar nunca.
3. **ARRANQUE OFICIAL:** Solo `./AUTOSTART_NETMARLYN_SERVER.command`. Nunca `python3 netmarlyn_server.py` directo.
4. **SIN FRAMEWORKS:** HTML + CSS + JS vanilla. Prohibido React, Vue, Angular, Tailwind.
5. **CARPETA ACTIVA:** `netmarlyn_website_00/`. Las carpetas `netmarlyn_website/` y `netmarlyn_website2/` son legacy/basura.
6. **FOTOS:** Se guardan como `{QR}.jpg` (NO `foto_{QR}.jpg`). Ruta: `colegios_data/{codigo}/fotos/{QR}.jpg`
7. **NUNCA BORRAR ENDPOINTS:** Solo agregar al servidor. Nunca eliminar los existentes.

---

## 6. TECHNICAL_CONTEXT

| Componente | Detalle |
|---|---|
| Servidor | Python 3 `http.server.SimpleHTTPRequestHandler` extendido |
| Puerto | 9300 |
| Host físico | Mac Mini (producción) |
| Desarrollo | Mac Studio (Mauricio) |
| Acceso externo | Cloudflare Tunnel → `www.netmarlyn.site` |
| Telemetría | Cloudflare Worker (`worker_cloud/worker.js`) |
| DB visitas | `visitas_detalladas.json` (JSON Array + fallback NDJSON) |
| Datos escolares | `colegios_data/{CODIGO}/listas/{aula}.json` + `/fotos/{QR}.jpg` |
| Deps Python | `openpyxl`, `python-docx` (auto-instaladas por autostart) |
| QR Scanning | jsQR v1.4.0 (CDN jsdelivr) |
| Auth frontend | Código institución + password hardcodeado en JS |
| ID formato | `XXXXXXX-XXXX` ej: `3847211-F7K2` |
| OS autostart | macOS LaunchAgent `com.netmarlyn.server.plist` |

**Archivos clave:**
```
netmarlyn_site_folder_macstudio/
├── netmarlyn_server.py                  ← Motor backend (BLINDADO)
├── AUTOSTART_NETMARLYN_SERVER.command   ← Arranque oficial v4.0
├── BITACORA_IA_NETMARLYN.md            ← Fuente de verdad del proyecto
├── NETMARLYN_STATE_SNAPSHOT.md         ← Este archivo
├── PROMPT_PARA_ANTIGRAVITY.txt         ← Mandatos para IAs
├── visitas_detalladas.json             ← DB de visitas
├── colegios_data/                      ← Datos escolares
└── netmarlyn_website_00/               ← Sitio ACTIVO
    ├── index.html, style.css, sw.js, manifest.json
    ├── escaneo.html     ← QR Scanner Android (PRIORIDAD)
    ├── fotos.html       ← Gestión fotos + carnets
    ├── listas.html      ← Cajón Mágico
    ├── acciones.html    ← Hub del maestro
    ├── colegios.html
    ├── js/visualizers_v3.js
    └── assets/
```

---

## 7. KNOWLEDGE_GENERATED

1. **Causa raíz "sitio caído":** Cloudflare exige `HTTP/1.1 200 OK` como primera línea absoluta. Llamar `send_header()` antes de `send_response()` enviaba texto de cabecera como si fuera el status code → Cloudflare rechazaba con "Malformed HTTP status code".

2. **Proceso zombi = puerto bloqueado:** Al sustituir la carpeta, el proceso Python viejo seguía corriendo invisible, bloqueando el puerto 9300. El nuevo proceso fallaba silenciosamente.

3. **Override de `send_response` es la solución definitiva:** Garantiza el orden HTTP estructuralmente, independiente de cómo codifique cualquier IA futura.

4. **Android A21s requiere HTTPS para cámara:** `getUserMedia()` bloqueado en HTTP. El usuario DEBE entrar por `https://www.netmarlyn.site`.

5. **`facingMode: { exact: "environment" }` puede fallar en Samsung:** Se implementó fallback: exacto → general de entorno.

6. **Ruta canónica de fotos:** `colegios_data/{codigo}/fotos/{QR}.jpg` (sin prefijo "foto_").

---

## 8. DEVELOPMENT_LOG (COMPRESSED)

| PHASE | ACTION | RESULT |
|---|---|---|
| Base | Servidor Python + HTML + Cloudflare Tunnel | Sitio funcional en producción |
| Telemetría | Worker JS → POST /api/visitas | Tracking activo |
| Visualización | visualizers_v3.js + math de ráfagas | Barra animada sin bugs |
| PWA | manifest.json + sw.js | Instalable como app |
| M7: Listas | Login director + Matriz de aulas | Grid de aulas funcional |
| M8: Cajón Mágico | Ingesta Word/Excel/TXT/manual | Multi-formato operativo |
| M9: Acciones | Hub 2x2 para maestros | 4 módulos accesibles |
| M10: QR + Fotos | Gen. ID auto + captura Base64 | IDs y fotos almacenadas |
| Scanner Real | jsQR + getUserMedia | Escaneo QR real |
| Critical Fix | Override send_response + autostart v4.0 | Servidor blindado |
| Merge | Fusión servidor Studio + Mini版 | Servidor unificado y optimizado |

---

## 9. TECHNICAL_DECISIONS

| DECISION | RATIONALE | IMPACT |
|---|---|---|
| Override `send_response()` | Garantiza orden HTTP estructuralmente | CRÍTICO: Elimina error Cloudflare |
| Puerto 9300 fijo | Sin conflictos con otros servicios | Cloudflare Tunnel hardcodeado |
| JSON plano + fallback NDJSON | Compatibilidad sin migración | Servidor nunca crashea por datos |
| Fotos como JPG físico | Evita JSON inflados | Performance en búsquedas |
| QR `XXXXXXX-XXXX` | Legible + entropía suficiente | ID única escaneable y manual |
| LaunchAgent macOS | Sobrevive reboots | Sistema autónomo 24/7 |
| jsQR v1.4.0 CDN | Sin instalación, universal | Escaneo real en cualquier browser |

---

## 10. REJECTED_APPROACHES

| APPROACH | WHY_REJECTED |
|---|---|
| React/Next.js | Contra principio no-frameworks |
| Hosting cloud | Costo + preferencia On-Premise |
| SQLite/PostgreSQL | Complejidad innecesaria |
| Fotos en Base64 dentro de JSON | Infla archivos dramáticamente |
| alert() para errores cámara | Bloqueante; reemplazado por mensajes inline |
| Override de end_headers() | Enviaba headers en orden equivocado |
| python3 directo | No limpia zombis ni registra LaunchAgent |

---

## 11. PROBLEMS_AND_RESOLUTIONS

| PROBLEM | CAUSE | SOLUTION |
|---|---|---|
| Sitio caído tras actualizar carpeta | Proceso zombi bloqueando puerto 9300 | `lsof -ti:9300 \| xargs kill -9` en autostart |
| Error Malformed HTTP / CF 502 | `send_header()` antes de `send_response()` | Override estructural de `send_response()` |
| Cámara no funciona Android A21s | HTTP bloqueado + facingMode exacto falla | HTTPS obligatorio + fallback constraints |
| jsQR no definido | CDN cargaba tarde | Guard `typeof jsQR === 'undefined'` |
| Foto no aparece en escaneo | Ruta inconsistente (foto_QR vs QR) | Unificado a `{QR}.jpg` |
| JSON decode error | NDJSON leído con json.load() | Try/except con fallback línea por línea |
| Alumno no identificado | QR no asignado (falta ir a fotos.html) | Mensaje claro al usuario |
| Cabeceras CORS duplicadas | send_response override + send_header individuales | Eliminadas instancias individuales |

---

## 12. ASSUMPTIONS_DETECTED

1. Cloudflare Tunnel autenticado en Mac Mini (`cloudflared tunnel run` sin args)
2. Python 3 disponible como `python3` en PATH
3. Auth hardcodeada es aceptable para contexto escolar actual
4. Normalización de aulas (`replace(' ', '_')`) es consistente en toda la app
5. Volumen &lt; 5000 alumnos por colegio (JSON plano suficiente)
6. LaunchAgent funciona en la versión de macOS de la Mac Mini (no confirmado aún)

---

## 13. CURRENT_PROJECT_STATE

| Módulo | Estado |
|---|---|
| Servidor Python (Motor + Escudo) | ✅ COMPLETED |
| Cloudflare Tunnel + Autostart v4.0 | ✅ COMPLETED |
| PWA Base + CSS + SW | ✅ COMPLETED |
| Telemetría de visitas | ✅ COMPLETED |
| Portal Listas + Cajón Mágico | ✅ COMPLETED |
| Portal Acciones | ✅ COMPLETED |
| Generación de IDs QR | ✅ COMPLETED |
| Captura y almacenamiento de fotos | ✅ COMPLETED |
| Portal Escaneo con cámara real | 🔄 IN_PROGRESS (pendiente prueba A21s) |
| Carnet Digital imprimible | ⬜ NOT_STARTED |
| Pruebas end-to-end producción | 🔄 IN_PROGRESS |
| Reportes / Analytics | ⬜ NOT_STARTED |
| Módulo SOS ESTOY | ⬜ NOT_STARTED |

---

## 14. UNCERTAINTIES

1. ¿El escaneo QR funciona en el A21s real? (código mejorado, no confirmado)
2. ¿`/api/ver_foto` sirve la foto correctamente de punta a punta?
3. ¿El LaunchAgent sobrevive reinicios reales de la Mac Mini?
4. ¿El Carnet Digital en `fotos.html` genera el QR como imagen visual?
5. ¿Se necesita auth más robusta si el sitio escala?

---

## 15. PRIORITIZED_NEXT_STEPS

| STEP | PURPOSE | PRIORITY |
|---|---|---|
| 1. Confirmar escaneo QR en A21s | Cámara → detección → display alumno | HIGH |
| 2. Flujo completo Lista→QR→Foto→Escaneo | End-to-end en producción | HIGH |
| 3. Modal Carnet Digital en fotos.html | QR visual + foto imprimible | HIGH |
| 4. Verificar /api/ver_foto en producción | Foto debe aparecer en tarjeta de escaneo | HIGH |
| 5. Prueba LaunchAgent tras reinicio | Confirmar autonomía real | MEDIUM |
| 6. Módulo SOS ESTOY | Geolocalización maestro/guardia | MEDIUM |
| 7. Módulo Reportes | Dashboard asistencia y escaneos | MEDIUM |
| 8. Auth más robusta | SHA-256 o tokens para producción real | LOW |
| 9. Carnet físico en PDF | Imprimir carnets de alumnos | LOW |

---

## 16. PROJECT_STATE_VECTOR

| Dimensión | Estado |
|---|---|
| OBJECTIVE_CLARITY | HIGH |
| TECHNICAL_DEFINITION | HIGH |
| IMPLEMENTATION_PROGRESS | HIGH |
| DECISION_STABILITY | HIGH |
| CONTEXT_COMPLETENESS | HIGH |

---

## 17. CONTEXT_LOAD_SUMMARY (120 palabras)

Netmarlyn es un sistema de identificación escolar On-Premise (Mac Mini + Cloudflare Tunnel, puerto 9300). Servidor Python con Escudo de Protocolo HTTP (override de send_response). Frontend PWA vanilla sin frameworks. Maestros suben listas (Excel/Word/texto), el sistema genera IDs QR únicos (`XXXXXXX-XXXX`), captura fotos con móvil, y un portal escanea QR en tiempo real con jsQR para identificar alumnos con foto + nombre + grado. Problema crítico resuelto: headers HTTP fuera de orden causaban Cloudflare 502. Autostart v4.0 limpia zombis, instala dependencias, registra LaunchAgent. Fotos guardadas como `{QR}.jpg`. Siguiente inmediato: validar escaneo real en A21s y completar módulo de carnet digital imprimible.

---

## 18. INSTRUCTION_FOR_NEXT_AI

Asume que este documento representa el estado completo del proyecto. No reinicies análisis ya resueltos. Continúa el proceso desde el estado actual. Respeta las decisiones técnicas existentes. Solicita aclaraciones al usuario antes de modificar arquitectura, objetivos o estrategias definidas.

---

## 19. HUMAN_READABLE_PROJECT_SUMMARY

**Netmarlyn** es una plataforma digital de gestión escolar que corre completamente en una Mac Mini local, accesible desde internet gracias a un túnel seguro de Cloudflare. No requiere servicios en la nube ni instalación de apps en los dispositivos de los usuarios.

El objetivo central es digitalizar la identificación estudiantil: los directores suben listas de alumnos (Excel, Word, texto), el sistema genera automáticamente un código QR único por alumno, los maestros toman las fotos con su celular, y el personal del colegio verifica identidades en tiempo real escaneando el carnet con la cámara del teléfono.

El problema más crítico durante el desarrollo fue la inestabilidad del sitio cada vez que se actualizaban los archivos: el servidor enviaba datos fuera del orden que exige el protocolo HTTP, causando que Cloudflare rechazara todas las conexiones. La solución fue implementar un "Escudo de Protocolo" estructural en el código y un sistema de arranque automático (v4.0) que limpia procesos viejos, instala dependencias y se reactiva solo al encender la Mac Mini.

El sistema está en estado operativo avanzado. Los módulos de ingesta de listas, generación de IDs QR, captura de fotos y escaneo con cámara real están implementados. El siguiente paso lógico es validar el escaneo end-to-end en hardware real (Samsung A21s) y completar el módulo de carnet digital imprimible, que permitirá generar los documentos físicos de identificación de cada alumno.

---

## 20. BOOTSTRAP_INSTRUCTION_FOR_NEXT_SESSION

```
Este documento representa el estado completo del proyecto.
Cárgalo como contexto operativo del sistema.
No repitas análisis ya resueltos.
Confirma que entendiste:
• objetivo del proyecto
• estado actual
• decisiones técnicas
• próximos pasos
Luego queda listo para continuar desde ese punto y espera mis instrucciones.
```
