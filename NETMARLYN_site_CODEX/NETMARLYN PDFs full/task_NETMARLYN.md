# 🗺️ Master Plan: NetMarlyn + Maunet (Arquitectura Unificada)

## 🏁 Fase 0: Estabilización y Base (Completado)
- [x] **Tag 022:** Versión de producción certificada.
- [x] **Maunet Core (80%):** Entidad 3D estable, expresiones orgánicas, Zero-Audio Payload, sincronía labial básica.
- [x] **Infraestructura Base:** Servidor Python (Mac Mini), Cloudflare Tunnels y PWA funcional.
- [x] **Documentación Maestra:** Bitácora y Manual de Construcción actualizados.

## 📁 Eje 1: Identidad y Gestión Académica
- [/] **Módulo 1: Autenticación e Identidad Institucional** (Credenciales, permisos por colegio) `[40% avanzado]`.
- [/] **Módulo 3: Gestión e Ingesta de Listas** (Excel, Word, Foto) `[50% avanzado]`.
- [/] **Módulo 4: Generación de QR** (Identificadores únicos listos para impresión) `[70% avanzado]`.
- [/] **Módulo 5: Identidad Visual** (Registro fotográfico vinculado a ID Digital) `[49% avanzado]`.

## 📡 Eje 2: Operación Offline-First y Trazabilidad
- [ ] **Módulo 2: Sincronización Incremental** (Descarga local de base de alumnos) `[0% avanzado]`.
- [ ] **Módulo 6: Inicialización por Escaneo** (Activación de contexto dinámico) `[0% avanzado]`.
- [/] **Módulo 8: Control de Asistencia Masiva** (Validación local en milisegundos) `[10% avanzado]`.
- [ ] **Módulo 7: Trazabilidad Geoespacial** (Giroscopio/GPS en cada escaneo) `[0% avanzado]`.
- [ ] **Módulo 26: Seguridad y Emergencias SOS** (Alertas geolocalizadas) `[0% avanzado]`.

## ⚙️ Eje 3: Motor de Eventos y Backend
- [/] **Módulo 9: Registro Estructurado** (Generación de JSON con metadata completa) `[2% avanzado]`.
- [ ] **Módulo 10: Cola Offline y Resiliencia** (Persistencia local y reintentos) `[0% avanzado]`.
- [/] **Módulo 11: Ingestión en Servidor** (Validación de integridad y duplicados) `[0.01% avanzado]`.
- [/] **Módulo 12: Procesamiento y Auditoría** (Indexación cronológica) `[0.01% avanzado]`.
- [ ] **Módulo 13: Control de Duplicidad** (Bloqueo de accesos simultáneos) `[0% avanzado]`.
- [/] **Módulo 28: Infraestructura Distribuida** (Cluster de Mac Mini, balanceo) `[5% avanzado]`.

## 🧠 Eje 4: Inteligencia Maunet y Analítica
- [ ] **Módulo 16: Reportes Inteligentes Maunet** (Consultas naturales sobre asistencia/notas).
- [ ] **Módulo 18: Memoria Conversacional** (Historial persistente por alumno).
- [ ] **Módulo 15: Dashboards Avanzados** (Mapas de calor, KPIs institucionales).
- [ ] **Módulo 14: Notificaciones Inteligentes** (Alertas automáticas a padres/maestros).
- [ ] **Módulo 17: Interacción Individual** (Acceso personalizado para el alumno).

## 📚 Eje 5: Ecosistema Pedagógico y Gamificación
- [ ] **Módulo 21: Máquina del Tiempo** (Repositorio histórico de clases) `[0% avanzado]`.
- [/] **Módulo 22: Infografías Automáticas IA** (Audio maestro -> Contenido visual) `[4% avanzado]`.
- [ ] **Módulo 20: Entrega de Contenido Personalizado** (Recomendaciones IA).
- [ ] **Módulo 23: Entornos Colaborativos** (Monitoreo de participación grupal).
- [/] **Módulo 24: Maquetas 3D Interactivas** (Construcción colaborativa/Lego Digital) `[-1% avanzado (Rehacer)]`.
- [ ] **Módulo 27: Gamificación y Economía** (Puntos gestionados por Maunet).

## 🛠️ Eje 6: Módulos Especializados MAUNET
- [ ] **Idiomas** (Evaluación de pronunciación).
- [ ] **Matemáticas** (Resolución guiada).
- [ ] **Análisis Gráfico e Interpretación.**
- [ ] **Arte** (Corrección por cámara).
- [ ] **Oratoria y Simulación.**
- [ ] **Vocacional** (Evaluación de aptitudes).

---
**NOTA:** El desarrollo de las capacidades analíticas y estéticas de Maunet (Eje 4 y 6) está pausado temporalmente para priorizar la construcción de los Ejes 1, 2 y 3.

> [!IMPORTANT]
> **ARQUITECTURA QR APROBADA (Doble Comportamiento):**
> Todo QR generado (Módulo 4) debe ser obligatoriamente un enlace muy corto (ej: `netmarlyn.site/a1b2c`). Esto garantiza físicamente un QR Versión 1 o 2 (ultra rápido). La cámara PWA del maestro interceptará solo el código alfanumérico para registrar asistencia masiva offline a la velocidad de la luz, mientras que la cámara nativa del alumno usará el link completo para auto-loguearse directo en su portal web.
