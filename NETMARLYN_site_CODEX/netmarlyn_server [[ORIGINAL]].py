import http.server
import socketserver
import json
import os
import sys
import urllib.parse
import cgi
import hashlib
from datetime import datetime

# Librerías opcionales para ingesta Word/Excel (MANDATO v4.0)
try:
    from docx import Document
except ImportError:
    Document = None

try:
    import openpyxl
except ImportError:
    openpyxl = None

# --- GUARDIA DE DIRECTORIO (CWD) ---
# Asegura que el servidor siempre sepa dónde está parado,
# incluso si macOS lo arranca desde el Watchdog o Automator.
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Permitir anulación de puerto para pruebas locales (MANDATO DUAL SERVER)
try:
    PORT = int(sys.argv[1])
except (IndexError, ValueError):
    PORT = 9300

DATA_FILE = "visitas_detalladas.json"

# Asegurar que el archivo de base de datos exista
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

# --- CONFIGURACIÓN DE COLEGIOS Y SEGURIDAD MASTER ---
COLEGIOS_BASE_DIR = "folder_colegios_full"
if not os.path.exists(COLEGIOS_BASE_DIR):
    os.makedirs(COLEGIOS_BASE_DIR)

# Usuarios con autoridad máxima para crear colegios
MASTER_USERS = {
    "admin": "master123",
    "mauricio": "net1234",
    "soporte": "marlyn99"
}

# Estructura obligatoria de 10 carpetas por cada Silo de Colegio
ESTRUCTURA_SILO = [
    "listas",
    "fotos",
    "infografias",
    "maquetas_3d",
    "giroscopio",
    "maquina_tiempo",
    "reportes",
    "geofencing",
    "seguridad",
    "trabajos_grupos"
]

class NetmarlynTrackerHandler(http.server.SimpleHTTPRequestHandler):
    # ==========================================================
    #  ESCUDO DE PROTOCOLO HTTP (BLINDAJE ESTRUCTURAL)
    # ==========================================================
    # Este override asegura que NUNCA se envíen headers antes del Status Code.
    # Es la solución definitiva al error de 'Malformed HTTP Status' en Cloudflare.
    def send_response(self, code, message=None):
        # 1. Enviar primero la línea de estado (ej: HTTP/1.1 200 OK)
        super().send_response(code, message)
        
        # 2. Inyectar cabeceras globales inmediatamente después del éxito
        # Estas cabeceras se enviarán en TODAS las respuestas del servidor.
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '-1')
        self.send_header('Access-Control-Allow-Origin', '*')

    def end_headers(self):
        # El super().end_headers() enviará la línea en blanco que termina el bloque
        super().end_headers()

    def do_POST(self):
        # 1. Escuchar SÓLO en la ruta oficial /api/visitas
        if self.path == '/api/visitas':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # 2. Atrapar los datos JSON enviados por Cloudflare "The Gatekeeper"
                telemetry_data = json.loads(post_data.decode('utf-8'))
                
                # ¡FILTRO CRÍTICO! Ignorar telemetría si es el propio polling de la barra o archivos estáticos
                visit_path = telemetry_data.get('path', '')
                if visit_path.startswith('/api/') or visit_path.endswith(('.css', '.js', '.png', '.jpg', '.ico', '.json')):
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"status": "ignored", "message": "Telemetria de background ignorada"}')
                    return

                # 3. Leer la base de datos actual (soportando formato antiguo NDJSON)
                db = []
                try:
                    with open(DATA_FILE, "r") as f:
                        db = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    # Fallback para archivos NDJSON (línea por línea)
                    with open(DATA_FILE, "r") as f:
                        for line in f:
                            if line.strip():
                                try:
                                    db.append(json.loads(line))
                                except:
                                    pass
                
                # 4. Inyectar el nuevo registro al listado de la base de datos
                db.append(telemetry_data)
                
                # 5. Guardar el archivo JSON actualizado (Identado y ordenado)
                with open(DATA_FILE, "w") as f:
                    json.dump(db, f, indent=4, ensure_ascii=False)
                
                # Responder a Cloudflare indicando que todo se guardó perfecto
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "success", "message": "Telemetria Registrada Exitosa"}')
                
                # Mostrar en la pantalla negra de la consola local que llegó alguien
                ip = telemetry_data.get('ip', 'N/A')
                city = telemetry_data.get('city', 'N/A')
                os_type = telemetry_data.get('os', 'N/A')
                is_new = "NUEVO" if telemetry_data.get('is_new') else "RECURRENTE"
                print(f"[{datetime.now().strftime('%H:%M:%S')}] RASTREO: {is_new} VISITANTE DESDE {ip} ({city}) USANDO {os_type}")
                
            except Exception as e:
                # Si llega error por mal enrutamiento
                self.send_response(400)
                self.end_headers()
                print(f"[ERROR] Datos invalidos recividos: {e}")
                
        elif self.path == '/api/peticion_infografia':
            # ===================================================
            # ENDPOINT: Recibir texto de infografía + metadatos
            # ===================================================
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                datos = json.loads(post_data.decode('utf-8'))
                codigo = datos.get('colegio', '').strip().upper()
                texto = datos.get('texto', '').strip()
                
                if not codigo or not texto:
                    raise ValueError("Faltan campos obligatorios: colegio o texto")

                # MODO DEMO: Guardar todo en netmarlyn_website_00/infografias_full
                carpeta_ia = os.path.join("netmarlyn_website_00", "infografias_full")
                os.makedirs(carpeta_ia, exist_ok=True)
                
                # Nombre de archivo basado en timestamp para unicidad
                import datetime as dt
                ts_clean = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
                nombre_archivo = f"peticion_{ts_clean}.json"
                ruta_peticion = os.path.join(carpeta_ia, nombre_archivo)

                # Guardar JSON
                with open(ruta_peticion, "w", encoding="utf-8") as f:
                    json.dump(datos, f, indent=4, ensure_ascii=False)

                log_entry = f"[{dt.datetime.now().strftime('%H:%M:%S')}] PETICIÓN INFOGRAFÍA RECIBIDA: {codigo} -> {nombre_archivo} (Simulando IA...)\n"
                print(log_entry, end="")
                with open("server.log", "a", encoding="utf-8") as lf:
                    lf.write(log_entry)

                # --- MODO SIMULADOR IA: Generar el HTML visual al instante ---
                self.simular_procesamiento_ia(carpeta_ia, ts_clean, texto)

                respuesta = json.dumps({"status": "ok", "msg": "Infografía generada con éxito"})
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(respuesta)))
                self.end_headers()
                self.wfile.write(respuesta.encode('utf-8'))

            except Exception as e:
                print(f"[ERROR] /api/peticion_infografia: {e}")
                err_body = json.dumps({"status": "error", "msg": str(e)})
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(err_body.encode('utf-8'))

        elif self.path == '/api/subir_lista':
            # ===================================================
            # ENDPOINT: Recibir y guardar lista de alumnos por aula
            # Espera JSON: { "codigo": "A123", "aula": "Prekinder_A", "texto": "..." }
            # ===================================================
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                datos = json.loads(post_data.decode('utf-8'))
                codigo_colegio = datos.get('codigo', '').strip().upper()
                aula           = datos.get('aula', '').strip().replace(' ', '_').replace('°', 'grado')
                texto_crudo    = datos.get('texto', '').strip()

                if not codigo_colegio or not aula or not texto_crudo:
                    raise ValueError("Faltan campos: codigo, aula o texto")

                # Parsear nombres: cada línea es un alumno (quitar números, puntos, bullet)
                import re
                lineas = texto_crudo.split('\n')
                alumnos = []
                for linea in lineas:
                    nombre = re.sub(r'^[\d\.\-\)\s]+', '', linea).strip()
                    if nombre:
                        alumnos.append({"nombre": nombre.upper(), "foto": None, "qr": None})

                # Buscar Silo dinámico en folder_colegios_full
                target_dir = None
                for d in os.listdir(COLEGIOS_BASE_DIR):
                    if d.startswith(codigo_colegio + "_") or d == codigo_colegio:
                        target_dir = os.path.join(COLEGIOS_BASE_DIR, d)
                        break
                
                if not target_dir:
                    # Si no existe, lo creamos (Legacy support o directo)
                    target_dir = os.path.join(COLEGIOS_BASE_DIR, f"{codigo_colegio}_Colegio")
                    os.makedirs(target_dir, exist_ok=True)

                if target_dir:
                    carpeta_listas = os.path.join(target_dir, "listas")
                    os.makedirs(carpeta_listas, exist_ok=True)
                    # Guardar JSON de la lista con timestamp
                    archivo_lista = os.path.join(carpeta_listas, f"{aula}.json")
                payload = {
                    "colegio": codigo_colegio,
                    "aula": aula,
                    "total_alumnos": len(alumnos),
                    "fecha_subida": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "alumnos": alumnos
                }
                with open(archivo_lista, 'w', encoding='utf-8') as f:
                    json.dump(payload, f, indent=4, ensure_ascii=False)

                print(f"[{datetime.now().strftime('%H:%M:%S')}] LISTA GUARDADA: {codigo_colegio}/{aula} — {len(alumnos)} alumnos")

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                resp = json.dumps({"status": "ok", "total": len(alumnos), "archivo": f"{aula}.json"})
                self.wfile.write(resp.encode('utf-8'))

            except Exception as e:
                print(f"[ERROR] /api/subir_lista: {e}")
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "msg": str(e)}).encode('utf-8'))

        elif self.path == '/api/archive-memory':
            # ===================================================
            # ENDPOINT: Guardar memoria a largo plazo de Maunet
            # ===================================================
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                carnet = data.get('carnet', 'UNKNOWN')
                offloaded_records = data.get('records', [])
                
                if offloaded_records:
                    # Guardar memorias en la carpeta de maunet dentro de la web root
                    mem_dir = os.path.join("netmarlyn_website_00", "maunet_site")
                    os.makedirs(mem_dir, exist_ok=True)
                    file_name = f"LONG_TERM_MEMORY_{carnet}.json"
                    file_path = os.path.join(mem_dir, file_name)
                    
                    archive_data = {"carnet": carnet, "archived_interactions": []}
                    if os.path.exists(file_path):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            try:
                                archive_data = json.load(f)
                            except:
                                pass
                        
                    archive_data["archived_interactions"].extend(offloaded_records)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(archive_data, f, indent=4, ensure_ascii=False)
                        
                respuesta = json.dumps({"status": "success", "archived_count": len(offloaded_records)})
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(respuesta.encode('utf-8'))
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] MAUNET MEMORY: {len(offloaded_records)} registros guardados para {carnet}")

            except Exception as e:
                print(f"[ERROR] /api/archive-memory: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

        elif self.path == '/api/chat':
            # ===================================================
            # ENDPOINT: PROXY LOCAL HACIA OLLAMA (11434)
            # ===================================================
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                import urllib.request
                req = urllib.request.Request("http://127.0.0.1:11434/api/chat", data=post_data, headers={'Content-Type': 'application/json'})
                with urllib.request.urlopen(req) as response:
                    resp_data = response.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(resp_data)
            except Exception as e:
                print(f"[ERROR] Proxy Ollama Falló: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

        elif self.path == '/api/obtener_lista':
            # ===================================================
            # ENDPOINT: Obtener lista de clase y asignar QRs a alumnos nuevos
            # ===================================================
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                datos = json.loads(post_data.decode('utf-8'))
                codigo_colegio = datos.get('codigo', '').strip().upper()
                aula           = datos.get('aula', '').strip().replace(' ', '_').replace('°', 'grado')

                if not codigo_colegio or not aula:
                    raise ValueError("Faltan campos: codigo o aula")

                # Buscar Silo dinámico
                target_dir = None
                for d in os.listdir(COLEGIOS_BASE_DIR):
                    if d.startswith(codigo_colegio + "_") or d == codigo_colegio:
                        target_dir = os.path.join(COLEGIOS_BASE_DIR, d)
                        break
                
                if not target_dir:
                    raise ValueError(f"No existe silo para el colegio {codigo_colegio}")

                archivo_lista = os.path.join(target_dir, "listas", f"{aula}.json")
                if not os.path.exists(archivo_lista):
                    raise ValueError(f"No existe lista para el aula {aula}")

                # Leer JSON actual
                with open(archivo_lista, 'r', encoding='utf-8') as f:
                    payload = json.load(f)

                alumnos = payload.get("alumnos", [])
                modificado = False
                import random, string

                # Protocolo de Identidad Netmarlyn: [CODIGO]-[HASH7]
                import hashlib, time

                for alumno in alumnos:
                    if not alumno.get("qr"):
                        modificado = True
                        seed = f"{codigo_colegio}{aula}{alumno['nombre']}{time.time()}"
                        h = hashlib.sha256(seed.encode()).hexdigest()
                        # Protocolo NM: [CODIGO]-[HASH7]
                        alumno["qr"] = f"{codigo_colegio}-{h[:7].upper()}"

                if modificado:
                    # Guardar JSON actualizado
                    payload["alumnos"] = alumnos
                    with open(archivo_lista, 'w', encoding='utf-8') as f:
                        json.dump(payload, f, indent=4, ensure_ascii=False)
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] QRs ASIGNADOS: {codigo_colegio}/{aula}")

                # Obtener colores institucionales del config.json
                color_p = "#001342"
                color_s = "#00e5ff"
                color_3 = "#ffffff"
                color_4 = "#d8ff00"
                config_path = os.path.join(target_dir, "config.json")
                if os.path.exists(config_path):
                    try:
                        with open(config_path, 'r', encoding='utf-8') as cf:
                            c_json = json.load(cf)
                            color_p = c_json.get('color_primario', color_p)
                            color_s = c_json.get('color_secundario', color_s)
                            color_3 = c_json.get('color_3', color_3)
                            color_4 = c_json.get('color_4', color_4)
                    except: pass

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                resp = json.dumps({
                    "status": "ok", 
                    "alumnos": alumnos,
                    "color_primario": color_p,
                    "color_secundario": color_s,
                    "color_3": color_3,
                    "color_4": color_4
                }, ensure_ascii=False)
                self.wfile.write(resp.encode('utf-8'))

            except Exception as e:
                print(f"[ERROR] /api/obtener_lista: {e}")
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "msg": str(e)}).encode('utf-8'))

        elif self.path == '/api/obtener_estado_grados':
            # ===================================================
            # ENDPOINT: Consultar qué grados ya tienen listas
            # ===================================================
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                datos = json.loads(post_data.decode('utf-8'))
                codigo = datos.get('codigo', '').strip().upper()
                
                if not codigo:
                    raise ValueError("Falta código de colegio")

                # Buscar Silo dinámico
                target_dir = None
                for d in os.listdir(COLEGIOS_BASE_DIR):
                    if d.startswith(codigo + "_") or d == codigo:
                        target_dir = os.path.join(COLEGIOS_BASE_DIR, d)
                        break
                
                if not target_dir:
                    # Fallback si aún no existe silo
                    directorio = os.path.join(COLEGIOS_BASE_DIR, f"{codigo}_Colegio", "listas")
                else:
                    directorio = os.path.join(target_dir, "listas")
                completos = []
                
                if os.path.exists(directorio):
                    for file in os.listdir(directorio):
                        if file.endswith(".json"):
                            nombre_limpio = file.replace(".json", "")
                            completos.append(nombre_limpio)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "grados": completos}).encode('utf-8'))

            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "msg": str(e)}).encode('utf-8'))

        elif self.path.split('?')[0].rstrip('/') == '/api/identificar_alumno':
            # ===================================================
            # ENDPOINT: Buscar alumno por su QR (Búsqueda Global)
            # ===================================================
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                datos = json.loads(post_data.decode('utf-8'))
                qr_buscado = datos.get('qr', '').strip().upper()
                
                if not qr_buscado:
                    raise ValueError("Falta código QR")

                # --- VALIDACIÓN MASTER (NM-v5.0) ---
                if qr_buscado.upper() == "MASTER-2026-NM":
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    resp = json.dumps({
                        "status": "ok",
                        "alumno": {
                            "nombre": "ADMINISTRADOR CENTRAL",
                            "rol": "MASTER",
                            "colegio": "NETMARLYN HQ",
                            "grado": "CONTROL TOTAL",
                            "color_primario": "#001342",
                            "color_secundario": "#00e5ff"
                        }
                    }, ensure_ascii=False)
                    self.wfile.write(resp.encode('utf-8'))
                    return

                resultado = None
                # Búsqueda exhaustiva en todos los colegios y listas del nuevo folder_colegios_full
                if os.path.exists(COLEGIOS_BASE_DIR):
                    for silo_folder in os.listdir(COLEGIOS_BASE_DIR):
                        if not os.path.isdir(os.path.join(COLEGIOS_BASE_DIR, silo_folder)): continue
                        
                        path_listas = os.path.join(COLEGIOS_BASE_DIR, silo_folder, "listas")
                        if os.path.exists(path_listas):
                            for archivo in os.listdir(path_listas):
                                if archivo.endswith(".json"):
                                    try:
                                        with open(os.path.join(path_listas, archivo), "r", encoding="utf-8") as f:
                                            data_lista = json.load(f)
                                            for alumno in data_lista.get("alumnos", []):
                                                if alumno.get("qr") == qr_buscado:
                                                    nombre_grado = archivo.replace(".json", "").replace("_", " ")
                                                    if "Personal Institucion" in nombre_grado:
                                                        nombre_grado = "PERSONAL DOCENTE/ADM"
                                                    
                                                    # Obtener colores para este carnet específico
                                                    c_p = "#001342"
                                                    c_s = "#00e5ff"
                                                    c_3 = "#ffffff"
                                                    c_4 = "#d8ff00"
                                                    config_silo = os.path.join(COLEGIOS_BASE_DIR, silo_folder, "config.json")
                                                    if os.path.exists(config_silo):
                                                        try:
                                                            with open(config_silo, 'r', encoding='utf-8') as cf:
                                                                cj = json.load(cf)
                                                                c_p = cj.get('color_primario', c_p)
                                                                c_s = cj.get('color_secundario', c_s)
                                                                c_3 = cj.get('color_3', c_3)
                                                                c_4 = cj.get('color_4', c_4)
                                                        except: pass

                                                    resultado = {
                                                        "nombre": alumno["nombre"],
                                                        "grado": nombre_grado,
                                                        "colegio": data_lista.get("colegio", "COLEGIO " + silo_folder),
                                                        "foto": alumno.get("foto"), # Base64
                                                        "color_primario": c_p,
                                                        "color_secundario": c_s,
                                                        "color_3": c_3,
                                                        "color_4": c_4
                                                    }
                                                    break
                                        if resultado: break
                                    except: continue
                        if resultado: break

                if resultado:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "ok", "alumno": resultado}).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "error", "msg": "Alumno no identificado"}).encode('utf-8'))

            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "msg": str(e)}).encode('utf-8'))

        elif self.path == '/api/subir_foto':
            # ===================================================
            # ENDPOINT: Guardar foto del alumno (Base64)
            # ===================================================
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                datos = json.loads(post_data.decode('utf-8'))
                codigo = datos.get('codigo', '').strip().upper()
                aula = datos.get('aula', '').strip()
                qr_id = datos.get('qr', '').strip()
                base64_str = datos.get('foto_base64', '')

                if not codigo or not aula or not qr_id or not base64_str:
                    raise ValueError("Faltan campos: codigo, aula, qr o foto_base64")

                # Limpiar header de base64 si existe (data:image/jpeg;base64,xxxx)
                if ',' in base64_str:
                    base64_str = base64_str.split(',', 1)[1]

                import base64
                img_data = base64.b64decode(base64_str)

                # Buscar Silo dinámico para guardar foto
                target_dir = None
                for d in os.listdir(COLEGIOS_BASE_DIR):
                    if d.startswith(codigo + "_") or d == codigo:
                        target_dir = os.path.join(COLEGIOS_BASE_DIR, d)
                        break
                
                if not target_dir:
                    # Legacy fallback
                    target_dir = os.path.join(COLEGIOS_BASE_DIR, f"{codigo}_Colegio")
                    os.makedirs(target_dir, exist_ok=True)

                # Directorio de fotos
                carpeta_fotos = os.path.join(target_dir, "fotos")
                os.makedirs(carpeta_fotos, exist_ok=True)
                
                nombre_archivo = f"{qr_id}.jpg"
                ruta_foto = os.path.join(carpeta_fotos, nombre_archivo)

                # Guardar JPG
                with open(ruta_foto, "wb") as fh:
                    fh.write(img_data)

                # Actualizar JSON del aula dentro del Silo
                archivo_lista = os.path.join(target_dir, "listas", f"{aula}.json")
                if os.path.exists(archivo_lista):
                    with open(archivo_lista, 'r', encoding='utf-8') as f:
                        payload = json.load(f)
                    
                    for alumno in payload.get('alumnos', []):
                        if alumno.get('qr') == qr_id:
                            alumno['foto'] = nombre_archivo
                            break
                    
                    with open(archivo_lista, 'w', encoding='utf-8') as f:
                        json.dump(payload, f, indent=4, ensure_ascii=False)

                print(f"[{datetime.now().strftime('%H:%M:%S')}] FOTO ASIGNADA: {codigo} / {qr_id}")

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "archivo": nombre_archivo}).encode('utf-8'))
                
            except Exception as e:
                print(f"[ERROR] /api/subir_foto: {e}")
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "msg": str(e)}).encode('utf-8'))

        elif self.path == '/api/leer_archivo':
            # ===================================================
            # ENDPOINT: Leer archivo Word/Excel y extraer texto
            # Recibe multipart/form-data con campo 'archivo'
            # ===================================================
            try:
                import cgi, tempfile
                content_type = self.headers.get('Content-Type', '')
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)

                # Parsear multipart manualmente usando cgi module
                environ = {
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': content_type,
                    'CONTENT_LENGTH': str(content_length),
                }
                import io
                form = cgi.FieldStorage(
                    fp=io.BytesIO(body),
                    headers=self.headers,
                    environ=environ
                )

                archivo_field = form['archivo']
                nombre_archivo = archivo_field.filename.lower()
                datos_binarios = archivo_field.file.read()

                texto_extraido = ""

                if nombre_archivo.endswith('.docx'):
                    # Leer Word con python-docx
                    from docx import Document
                    import io as sysio
                    doc = Document(sysio.BytesIO(datos_binarios))
                    lineas = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
                    texto_extraido = "\n".join(lineas)

                elif nombre_archivo.endswith('.xlsx') or nombre_archivo.endswith('.xls'):
                    # Leer Excel con openpyxl
                    import openpyxl, io as sysio
                    wb = openpyxl.load_workbook(sysio.BytesIO(datos_binarios), read_only=True, data_only=True)
                    ws = wb.active
                    lineas = []
                    for row in ws.iter_rows(values_only=True):
                        linea = " ".join(str(c) for c in row if c is not None).strip()
                        if linea:
                            lineas.append(linea)
                    texto_extraido = "\n".join(lineas)

                elif nombre_archivo.endswith('.txt') or nombre_archivo.endswith('.csv'):
                    texto_extraido = datos_binarios.decode('utf-8', errors='ignore')

                else:
                    raise ValueError(f"Formato no soportado: {nombre_archivo}")

                num_lineas = len([l for l in texto_extraido.split('\n') if l.strip()])
                print(f"[{datetime.now().strftime('%H:%M:%S')}] LEER_ARCHIVO: {nombre_archivo} — {num_lineas} líneas extraídas")

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                resp = json.dumps({"status": "ok", "texto": texto_extraido, "lineas": num_lineas}, ensure_ascii=False)
                self.wfile.write(resp.encode('utf-8'))

            except Exception as e:
                print(f"[ERROR] /api/leer_archivo: {e}")
                self.send_response(400)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "msg": str(e)}).encode('utf-8'))

        elif self.path == '/api/registrar_colegio':
            # ===================================================
            # ENDPOINT: Registrar Colegio y crear Silo de 10 folders
            # ===================================================
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                payload = json.loads(post_data.decode('utf-8'))

                m_user = "MASTER_BYPASS"

                import random, string as str_lib

                prefijo = payload.get('prefijo', '').strip().upper()
                nombre_limpio = payload.get('nombre', '').strip().replace(" ", "_")

                if not prefijo or len(prefijo) != 2:
                    raise ValueError("Falta el prefijo o no tiene 2 caracteres.")
                if not nombre_limpio:
                    raise ValueError("El nombre del colegio es obligatorio.")

                # ─────────────────────────────────────────────────
                # PROTOCOLO NM-4: Genera un código de 4 chars único
                # Tú pones 2 (prefijo), el sistema genera los 2 finales
                # Verifica que no exista ningún silo con ese código
                # ─────────────────────────────────────────────────
                CHARS = str_lib.ascii_uppercase + str_lib.digits
                codigo = None
                max_intentos = 50
                silos_existentes = set(os.listdir(COLEGIOS_BASE_DIR)) if os.path.exists(COLEGIOS_BASE_DIR) else set()
                codigos_existentes = set()
                for silo in silos_existentes:
                    # El código es la parte antes del primer "_"
                    codigos_existentes.add(silo.split("_")[0].upper())

                for _ in range(max_intentos):
                    sufijo = ''.join(random.choices(CHARS, k=2))
                    candidato = prefijo + sufijo  # Formato: LAXX (exactamente 4 chars)
                    if candidato not in codigos_existentes:
                        codigo = candidato
                        break

                if not codigo:
                    raise ValueError(f"No fue posible generar un código único con el prefijo '{prefijo}'. Intenta con otro prefijo.")

                # Crear Silo en folder_colegios_full/LAXX_NombreColegio
                nombre_carpeta = f"{codigo}_{nombre_limpio}"
                silo_path = os.path.join(COLEGIOS_BASE_DIR, nombre_carpeta)

                os.makedirs(silo_path)
                for sub in ESTRUCTURA_SILO:
                    os.makedirs(os.path.join(silo_path, sub))

                config = {
                    "id": codigo,
                    "nombre": payload.get('nombre'),
                    "gps": payload.get('gps'),
                    "admin_contacto": payload.get('admin_contacto'),
                    "admin_telefono": payload.get('admin_telefono'),
                    "color_primario": payload.get('color_primario', '#001342'),
                    "color_secundario": payload.get('color_secundario', '#00e5ff'),
                    "color_3": payload.get('color_3', '#ffffff'),
                    "color_4": payload.get('color_4', '#d8ff00'),
                    "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                with open(os.path.join(silo_path, "config.json"), "w", encoding="utf-8") as f:
                    json.dump(config, f, indent=4, ensure_ascii=False)

                # Si se adjuntó el LOGO FLAT(svg) desde el Front, lo guardamos para futuras Infografías y Diplomas
                logo_svg = payload.get('logo_svg')
                if logo_svg:
                    svg_path = os.path.join(silo_path, "infografias", "logo_frente.svg")
                    with open(svg_path, "w", encoding="utf-8") as svg_file:
                        svg_file.write(logo_svg)
                    print(f" -> Guardado logo vectorial (SVG Flat) en {svg_path}")

                print(f"[{datetime.now().strftime('%H:%M:%S')}] NUEVO COLEGIO: {nombre_carpeta} | Prefijo: {prefijo} → Código: {codigo}")


                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "codigo": codigo, "msg": f"Silo '{codigo}' creado correctamente"}).encode('utf-8'))

            except Exception as e:
                print(f"[ERROR] /api/registrar_colegio: {e}")
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "msg": str(e)}).encode('utf-8'))


        elif self.path == '/api/validar_colegio':
            # ===================================================
            # ENDPOINT: Validar credenciales de un colegio (Login)
            # ===================================================
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    post_data = self.rfile.read(content_length)
                    datos = json.loads(post_data.decode('utf-8'))
                else:
                    datos = {}
                
                codigo = datos.get('codigo', '').strip().upper()
                password = datos.get('password', '').strip()

                if not codigo or not password:
                    raise ValueError("Falta código o contraseña")

                resultado = None
                if os.path.exists(COLEGIOS_BASE_DIR):
                    for folder in os.listdir(COLEGIOS_BASE_DIR):
                        path_folder = os.path.join(COLEGIOS_BASE_DIR, folder)
                        if os.path.isdir(path_folder):
                            config_path = os.path.join(path_folder, "config.json")
                            if os.path.exists(config_path):
                                with open(config_path, "r", encoding="utf-8") as f:
                                    config = json.load(f)
                                    if config.get('id') == codigo and config.get('password_portal') == password:
                                        resultado = {
                                            "status": "ok",
                                            "nombre": config.get('nombre'),
                                            "codigo": config.get('id')
                                        }
                                        break
                
                if resultado:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(resultado).encode('utf-8'))
                else:
                    self.send_response(401)
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "error", "msg": "Credenciales inválidas"}).encode('utf-8'))
            except Exception as e:
                print(f"[ERROR] /api/validar_colegio: {e}")
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "msg": str(e)}).encode('utf-8'))

        else:
            # Si alguien intenta hacer POST a otro lugar que no sea la API, rechazar
            self.send_response(403)
            self.end_headers()

    def do_OPTIONS(self):
        # Necesario para permitir peticiones desde cualquier origen (CORS)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def translate_path(self, path):
        # Mapear las peticiones web al folder sagrado 'netmarlyn_website_00'
        # solo si no es un endpoint de API
        WEBSITE_ROOT = "netmarlyn_website_00"
        
        if not path.startswith('/api/'):
            if path == '/':
                path = '/index.html'
            
            clean_path = path.lstrip('/')
            if not clean_path.startswith(WEBSITE_ROOT + '/'):
                path = f'/{WEBSITE_ROOT}/{clean_path}'
        
        return super().translate_path(path)

    # Manejar las solicitudes GET normales (para servir la página y telemetría)
    def do_GET(self):
        # Extraer ruta limpia sin parámetros de consulta para comparaciones robustas
        url_parsed = urllib.parse.urlparse(self.path)
        clean_path = url_parsed.path
        params = urllib.parse.parse_qs(url_parsed.query)

        # --- ENDPOINT LISTAR INFOGRAFIAS (MODO DEMO) ---
        if clean_path == '/api/listar_infografias':
            try:
                # Buscar la carpeta infografas_full con múltiples fallbacks (Mac Mini compatible)
                posibles_carpetas = [
                    os.path.join("netmarlyn_website_00", "infografias_full"),
                    "infografias_full",
                    "/Users/mauricio/ANTIGRAVITY_PROJECTS_folder/NETMARLYN_site_websitefoldermake/netmarlyn_site_folder_macstudio/netmarlyn_website_00/infografias_full",
                    "/Users/mauricio/Desktop/infografias_full"
                ]
                
                folder = ""
                for p in posibles_carpetas:
                    if os.path.exists(p):
                        folder = p
                        print(f"[DEBUG GALERIA] Carpeta encontrada en: {p}")
                        break
                
                archivos = []
                if folder:
                    # Fase 1: Recolectar todas las peticiones JSON (Las nuevas grabaciones)
                    for f in sorted(os.listdir(folder), reverse=True):
                        if f.endswith(".json") and f.startswith("peticion_"):
                            try:
                                with open(os.path.join(folder, f), 'r', encoding='utf-8') as jf:
                                    data = json.load(jf)
                                    texto = data.get("texto", "Información IA")
                                    titulo = texto[:40].capitalize() + "..."
                                    archivos.append({
                                        "id": f,
                                        "titulo": f"✨ {titulo}",
                                        "fecha": "IA PROCESADA"
                                    })
                            except: pass
                            if len(archivos) >= 150: break

                    # Fase 2: Recolectar infografías HTML de referencia (Corazón, Volcán, Agua)
                    for f in sorted(os.listdir(folder)):
                        if f.endswith(".html") and f.startswith("infografia_"):
                            id_base = f.replace("infografia_", "").replace(".html", "")
                            peticion_id = f"peticion_{id_base}.json"
                            
                            ya_existe = any(a["id"] == peticion_id for a in archivos)
                            if not ya_existe:
                                title_pretty = id_base.replace("_", " ").capitalize()
                                archivos.append({
                                    "id": peticion_id,
                                    "titulo": f"📚 {title_pretty}",
                                    "fecha": "DIAGRAMA IA"
                                })
                                print(f"  [+] Añadiendo ejemplo de referencia: {title_pretty}")
                
                print(f"[DEBUG GALERIA] Total final listado: {len(archivos)} elementos.")
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                log_msg = f"[{datetime.now().strftime('%H:%M:%S')}] API: Listando {len(archivos)} infografías para la galería.\n"
                with open("server.log", "a", encoding="utf-8") as lf:
                    lf.write(log_msg)
                
                self.wfile.write(json.dumps(archivos).encode('utf-8'))
                return
            except Exception as e:
                self.send_error(500, str(e))
                return

        # --- NUEVO: ROMPEDOR DE CACHÉ RADICAL GLOBAL (v5.3.3) ---
        # Si es una página HTML y no trae la versión de seguridad 8813, forzamos redirección.
        clean_path = self.path.split('?')[0]
        if clean_path == '/' or clean_path.endswith('.html'):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            if params.get('v') != ['8813']:
                new_path = clean_path if clean_path != '/' else '/index.html'
                self.send_response(302)
                self.send_header('Location', f"{new_path}?v=8813")
                self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
                self.end_headers()
                return

        # --- ENDPOINT LISTAR COLEGIOS (GET) ---
        if self.path == '/api/listar_colegios':
            try:
                colegios = []
                if os.path.exists(COLEGIOS_BASE_DIR):
                    for folder in os.listdir(COLEGIOS_BASE_DIR):
                        path_folder = os.path.join(COLEGIOS_BASE_DIR, folder)
                        if os.path.isdir(path_folder):
                            config_path = os.path.join(path_folder, "config.json")
                            if os.path.exists(config_path):
                                with open(config_path, "r", encoding="utf-8") as f:
                                    colegios.append(json.load(f))
                
                # Ordenar por fecha de registro (descendente)
                colegios.sort(key=lambda x: x.get('fecha_registro', ''), reverse=True)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "colegios": colegios}).encode('utf-8'))
                return
            except Exception as e:
                print(f"[ERROR] /api/listar_colegios: {e}")
                self.send_response(500)
                self.end_headers()
                return

        # --- ENDPOINT LIVE STATS (Mejorado) ---
        if self.path == '/api/live_stats':
            try:
                db = []
                if os.path.exists(DATA_FILE):
                    try:
                        with open(DATA_FILE, "r") as f:
                            db = json.load(f)
                    except:
                        # Fallback NDJSON
                        with open(DATA_FILE, "r") as f:
                            for line in f:
                                if line.strip():
                                    try: db.append(json.loads(line))
                                    except: pass
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"total_visitas": len(db)}).encode('utf-8'))
                return
            except:
                self.send_response(500)
                self.end_headers()
                return

        # --- ENDPOINT VER FOTO (Búsqueda Optimizada) ---
        if self.path.startswith('/api/ver_foto'):
            from urllib.parse import urlparse, parse_qs
            query = parse_qs(urlparse(self.path).query)
            qr = query.get('qr', [None])[0]
            if not qr:
                self.send_response(404)
                self.end_headers()
                return

            foto_path = None
            if os.path.exists(COLEGIOS_BASE_DIR):
                # BÚSQUEDA INSTANTÁNEA: El primer segmento del QR es el ID del colegio
                if "-" in qr:
                    prefix = qr.split("-")[0]
                    # Buscamos directamente el silo que empieze con ese prefijo
                    for silo in os.listdir(COLEGIOS_BASE_DIR):
                        if silo.startswith(prefix + "_") or silo == prefix:
                            archivo = os.path.join(COLEGIOS_BASE_DIR, silo, "fotos", f"{qr}.jpg")
                            if os.path.exists(archivo):
                                foto_path = archivo
                            break # Encontrado o no, el prefijo nos dice que este era el silo
                
                # Fallback: Búsqueda exhaustiva si el QR no tiene el formato nuevo
                if not foto_path:
                    for silo in os.listdir(COLEGIOS_BASE_DIR):
                        if not os.path.isdir(os.path.join(COLEGIOS_BASE_DIR, silo)): continue
                        archivo = os.path.join(COLEGIOS_BASE_DIR, silo, "fotos", f"{qr}.jpg")
                        if os.path.exists(archivo):
                            foto_path = archivo
                            break
            
            if foto_path:
                self.send_response(200)
                self.send_header('Content-Type', 'image/jpeg')
                self.end_headers()
                with open(foto_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
            return
        
        # --- ENDPOINT VER FOTO ... ---
        # ... (dejo el código anterior igual)

        # --- ENDPOINT VER LOGO (NUEVO v4.7) ---
        if self.path.startswith('/api/obtener_logo'):
            from urllib.parse import urlparse, parse_qs
            query = parse_qs(urlparse(self.path).query)
            codigo = query.get('codigo', [None])[0]
            if not codigo:
                self.send_response(404)
                self.end_headers()
                return

            logo_path = None
            if os.path.exists(COLEGIOS_BASE_DIR):
                for silo in os.listdir(COLEGIOS_BASE_DIR):
                    if silo.startswith(codigo + "_") or silo == codigo:
                        archivo = os.path.join(COLEGIOS_BASE_DIR, silo, "infografias", "logo_frente.svg")
                        if os.path.exists(archivo):
                            logo_path = archivo
                        break
            
            if logo_path:
                self.send_response(200)
                self.send_header('Content-Type', 'image/svg+xml')
                self.end_headers()
                with open(logo_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                # Fallback al logo de Netmarlyn si no tiene uno propio
                self.send_response(302)
                self.send_header('Location', '/netmarlyn_website_00/assets/G_icono_netmarlyn.jpg')
                self.end_headers()
            return
        
        return super().do_GET()

    def simular_procesamiento_ia(self, carpeta, ts, texto):
        """Genera un archivo HTML con un SVG que simula ser una infografía IA avanzada"""
        nombre_html = f"infografia_{ts}.html"
        ruta_html = os.path.join(carpeta, nombre_html)
        
        # Lógica de expansión de contenido (Simulación de IA con base de conocimientos)
        t_low = texto.lower()
        extra_info = ""
        svg_graphic = ""
        
        if "rodilla" in t_low:
            extra_info = "La rodilla es la articulación más grande del cuerpo humano. Une el fémur con la tibia y está protegida por la rótula. Permite realizar movimientos de flexión y extensión indispensables para el desplazamiento."
            svg_graphic = """
            <g transform="translate(50,50)">
                <path d="M-10,-40 L10,-40 L10,0 L-10,0 Z" fill="#00e5ff" opacity="0.6" />
                <path d="M-10,10 L10,10 L10,50 L-10,50 Z" fill="#00e5ff" opacity="0.6" />
                <circle cx="0" cy="5" r="8" fill="#00e5ff">
                    <animate attributeName="r" values="8;10;8" dur="2s" repeatCount="indefinite" />
                </circle>
            </g>
            """
        elif "corazón" in t_low or "corazon" in t_low:
            extra_info = "El corazón es un órgano del tamaño de un puño compuesto de tejido muscular. Su función es bombear sangre a todo el cuerpo, transportando oxígeno y nutrientes vitales para la vida."
            svg_graphic = """
            <path d="M50 30 C 50 20 20 20 20 50 C 20 80 50 100 50 100 C 50 100 80 80 80 50 C 80 20 50 20 50 30" fill="#00e5ff">
                <animateTransform attributeName="transform" type="scale" values="1;1.1;1" dur="0.8s" repeatCount="indefinite" additive="sum" pivot="50 50" />
            </path>
            """
        elif "volcan" in t_low or "volcán" in t_low:
            extra_info = "Un volcán es una apertura en la corteza terrestre por donde emerge el magma, gases y cenizas. Su actividad es fundamental para la evolución geológica de nuestro planeta."
            svg_graphic = """
            <path d="M20 90 L50 20 L80 90 Z" fill="#444" stroke="#00e5ff" stroke-width="2" />
            <path d="M45 35 L55 35 L60 20 L40 20 Z" fill="#ff4400">
                <animate attributeName="opacity" values="0.5;1;0.5" dur="1s" repeatCount="indefinite" />
            </path>
            """
        elif "cerebro" in t_low or "cerebelo" in t_low:
            extra_info = "El cerebro y el cerebelo son partes fundamentales del sistema nervioso central. El cerebro procesa el pensamiento y los sentidos, mientras que el cerebelo coordina el equilibrio y el movimiento fino."
            svg_graphic = """
            <g transform="translate(50,50)">
                <path d="M-30,-10 C-40,-40 40,-40 30,-10 C45,0 45,30 30,40 C10,50 -10,50 -30,40 C-45,30 -45,0 -30,-10" fill="none" stroke="#00e5ff" stroke-width="2" />
                <path d="M0,-30 L0,45" stroke="#00e5ff" stroke-width="1" stroke-dasharray="2,2" />
                <circle cx="-15" cy="0" r="3" fill="#00e5ff"><animate attributeName="opacity" values="0;1;0" dur="1.5s" repeatCount="indefinite"/></circle>
                <circle cx="15" cy="15" r="3" fill="#00e5ff"><animate attributeName="opacity" values="0;1;0" dur="1.5s" begin="0.5s" repeatCount="indefinite"/></circle>
            </g>
            """
        elif "oído" in t_low or "oido" in t_low or "tímpano" in t_low:
            extra_info = "El oído humano capta ondas sonoras que hacen vibrar el tímpano. Estos impulsos mecánicos se transforman en señales eléctricas que el cerebro interpreta como sonido."
            svg_graphic = """
            <path d="M20,50 Q40,10 80,50 T140,50" fill="none" stroke="#00e5ff" stroke-width="3" opacity="0.5" transform="translate(0,0)">
                <animate attributeName="d" values="M20,50 Q40,10 80,50 T140,50;M20,50 Q40,90 80,50 T140,50;M20,50 Q40,10 80,50 T140,50" dur="2s" repeatCount="indefinite" />
            </path>
            <circle cx="80" cy="50" r="10" fill="none" stroke="#00e5ff" stroke-width="2" />
            """
        else:
            extra_info = "Netmarlyn IA ha analizado tu audio y ha generado esta síntesis educativa personalizada para fortalecer la comprensión de este tema en el aula."
            svg_graphic = """
            <circle cx="50" cy="50" r="45" fill="none" stroke="#00e5ff" stroke-width="1" stroke-dasharray="2,2" />
            <circle cx="50" cy="50" r="35" fill="none" stroke="#00e5ff" stroke-width="2" />
            <path d="M40 50 L45 55 L60 40" fill="none" stroke="#00e5ff" stroke-width="4" stroke-linecap="round" />
            <circle cx="50" cy="50" r="5" fill="#00e5ff"><animate attributeName="r" values="5;7;5" dur="0.8s" repeatCount="indefinite" /></circle>
            """

        html_template = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Infografía IA Netmarlyn</title>
    <style>
        body {{ background: #001342; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; }}
        .infographic {{ max-width: 600px; margin: 20px auto; background: #001342; border: 2px solid #00e5ff; border-radius: 40px; padding: 40px; box-shadow: 0 0 60px rgba(0,229,255,0.2); position: relative; overflow: hidden; }}
        .bg-grid {{ position: absolute; top:0; left:0; width:100%; height:100%; background-image: radial-gradient(#00e5ff 1px, transparent 1px); background-size: 30px 30px; opacity: 0.1; z-index: 0; }}
        .content {{ position: relative; z-index: 1; text-align: center; }}
        h1 {{ color: #00e5ff; letter-spacing: 10px; font-size: 24px; margin-bottom: 40px; text-shadow: 0 0 10px rgba(0,229,255,0.5); }}
        .viz-box {{ width: 200px; height: 200px; margin: 0 auto; background: rgba(0,229,255,0.05); border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(0,229,255,0.2); }}
        .data-panel {{ text-align: left; margin-top: 40px; padding: 30px; background: rgba(255,255,255,0.03); border-radius: 20px; border-left: 6px solid #00e5ff; }}
        .topic-title {{ font-size: 20px; color: #00e5ff; font-weight: bold; margin-bottom: 15px; text-transform: uppercase; }}
        .description {{ line-height: 1.8; color: #8b9bb4; font-size: 16px; }}
        .charts {{ display: flex; gap: 10px; margin-top: 20px; }}
        .bar {{ flex: 1; background: rgba(0,229,255,0.2); border-radius: 5px; height: 10px; overflow: hidden; position: relative; }}
        .bar-fill {{ position: absolute; top:0; left:0; height:100%; background: #00e5ff; }}
        .footer {{ margin-top: 40px; font-size: 12px; color: #5a6b8a; font-style: italic; }}
        .btn {{ display: inline-block; margin-top: 40px; padding: 18px 40px; background: #00e5ff; color: #001342; text-decoration: none; border-radius: 20px; font-weight: bold; transition: 0.3s; letter-spacing: 2px; }}
        .btn:hover {{ transform: scale(1.05); box-shadow: 0 0 30px #00e5ff; }}
    </style>
</head>
<body>
    <div class="infographic">
        <div class="bg-grid"></div>
        <div class="content">
            <h1>NETMARLYN IA</h1>
            
            <div class="viz-box">
                <svg width="150" height="150" viewBox="0 0 100 100">
                    {svg_graphic}
                </svg>
            </div>

            <div class="data-panel">
                <div class="topic-title">Análisis Generativo</div>
                <p style="font-size: 18px; font-weight: bold; margin-bottom: 15px; color: #fff;">{texto[:150]}...</p>
                <div class="description">{extra_info}</div>
                
                <div class="charts">
                    <div class="bar"><div class="bar-fill" style="width: 85%;"><animate attributeName="width" from="0%" to="85%" dur="1.5s" repeatCount="1"/></div></div>
                    <div class="bar"><div class="bar-fill" style="width: 92%;"><animate attributeName="width" from="0%" to="92%" dur="1.8s" repeatCount="1"/></div></div>
                    <div class="bar"><div class="bar-fill" style="width: 78%;"><animate attributeName="width" from="0%" to="78%" dur="1.2s" repeatCount="1"/></div></div>
                </div>
            </div>

            <p class="footer">Infografía generada por motor Netmarlyn v6.15 el {ts}</p>
            
            <a href="../ver_infografias.html?v=8813" class="btn">VOLVER A GALERÍA</a>
        </div>
    </div>
</body>
</html>
"""
        with open(ruta_html, "w", encoding="utf-8") as f:
            f.write(html_template)

# Levantar el servidor Motor con Blindaje de Hilos y Red
import socket

class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # Esto permite que el puerto se libere instantáneamente al cerrar
    allow_reuse_address = True
    # Soporte para IPv4 y IPv6 simultáneos si el OS lo permite
    address_family = socket.AF_INET6 if socket.has_ipv6 else socket.AF_INET

if __name__ == "__main__":
    try:
        # Forzamos a que escuche en todas las interfaces de forma asíncrona
        with ThreadedHTTPServer(("", PORT), NetmarlynTrackerHandler) as httpd:
            print(f"==================================================")
            print(f" NETMARLYN LOCAL SERVER INICIADO - MOTOR DE DATOS ")
            print(f"==================================================")
            print(f"Escuchando en: PORT {PORT} (IPv4/IPv6 Dual Stack)")
            print(f"Base de Datos Activa: {DATA_FILE}")
            print(f"==================================================")
            httpd.serve_forever()
    except Exception as e:
        print(f"[FATAL] El motor no pudo arrancar: {e}")
        sys.exit(1)
