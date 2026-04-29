import http.server
import socketserver
import json
import os
import sys
import urllib.parse
from datetime import datetime

# --- GUARDIA DE DIRECTORIO (CWD) ---
# Asegura que el servidor siempre sepa dónde está parado,
# incluso si macOS lo arranca desde el Watchdog o Automator.
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

PORT = 9300
DATA_FILE = "visitas_detalladas.json"

# Asegurar que el archivo de base de datos exista
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

class NetmarlynTrackerHandler(http.server.SimpleHTTPRequestHandler):
    def send_response(self, code, message=None):
        """Sobrescribimos send_response para inyectar cabeceras anti-caché de forma segura 
        después del código de estado y antes de que se cierren las cabeceras."""
        super().send_response(code, message)
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '-1')
        self.send_header('Access-Control-Allow-Origin', '*')

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

                # Crear carpeta del colegio si no existe aún
                carpeta_listas = os.path.join("colegios_data", codigo_colegio, "listas")
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

                archivo_lista = os.path.join("colegios_data", codigo_colegio, "listas", f"{aula}.json")
                
                if not os.path.exists(archivo_lista):
                    raise ValueError(f"No existe lista para el aula {aula}")

                # Leer JSON actual
                with open(archivo_lista, 'r', encoding='utf-8') as f:
                    payload = json.load(f)

                alumnos = payload.get("alumnos", [])
                modificado = False
                import random, string

                # Asignar QR si no lo tiene
                for alumno in alumnos:
                    if not alumno.get("qr"):
                        # Generar ID de formato: 7 dígitos - 4 letras/números
                        num_part = ''.join(random.choices(string.digits, k=7))
                        hash_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
                        alumno["qr"] = f"{num_part}-{hash_part}"
                        modificado = True

                if modificado:
                    # Guardar JSON actualizado
                    payload["alumnos"] = alumnos
                    with open(archivo_lista, 'w', encoding='utf-8') as f:
                        json.dump(payload, f, indent=4, ensure_ascii=False)
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] QRs ASIGNADOS: {codigo_colegio}/{aula}")

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                resp = json.dumps({"status": "ok", "alumnos": alumnos}, ensure_ascii=False)
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

                directorio = os.path.join("colegios_data", codigo, "listas")
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

        elif self.path == '/api/identificar_alumno':
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

                resultado = None
                # Búsqueda exhaustiva en todos los colegios y listas
                base_dir = "colegios_data"
                if os.path.exists(base_dir):
                    for colegio_folder in os.listdir(base_dir):
                        path_listas = os.path.join(base_dir, colegio_folder, "listas")
                        if os.path.exists(path_listas):
                            for archivo in os.listdir(path_listas):
                                if archivo.endswith(".json"):
                                    try:
                                        with open(os.path.join(path_listas, archivo), "r", encoding="utf-8") as f:
                                            data_lista = json.load(f)
                                            for alumno in data_lista.get("alumnos", []):
                                                if alumno.get("qr") == qr_buscado:
                                                    resultado = {
                                                        "nombre": alumno["nombre"],
                                                        "grado": archivo.replace(".json", "").replace("_", " "),
                                                        "colegio": data_lista.get("colegio", "COLEGIO " + colegio_folder),
                                                        "foto": alumno.get("foto") # Base64
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

                # Directorio de fotos
                carpeta_fotos = os.path.join("colegios_data", codigo, "fotos")
                os.makedirs(carpeta_fotos, exist_ok=True)
                
                nombre_archivo = f"{qr_id}.jpg"
                ruta_foto = os.path.join(carpeta_fotos, nombre_archivo)

                # Guardar JPG
                with open(ruta_foto, "wb") as fh:
                    fh.write(img_data)

                # Actualizar JSON del aula
                archivo_lista = os.path.join("colegios_data", codigo, "listas", f"{aula}.json")
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
                self.send_header('Access-Control-Allow-Origin', '*')
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
                self.end_headers()
                resp = json.dumps({"status": "ok", "texto": texto_extraido, "lineas": num_lineas}, ensure_ascii=False)
                self.wfile.write(resp.encode('utf-8'))

            except Exception as e:
                print(f"[ERROR] /api/leer_archivo: {e}")
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "msg": str(e)}).encode('utf-8'))

        else:
            # Si alguien intenta hacer POST a otro lugar que no sea la API, rechazar
            self.send_response(403)
            self.end_headers()

    def do_OPTIONS(self):
        # Necesario para CORS (especialmente desde mobile/PWA)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    # Manejar las solicitudes GET normales (para servir la página y telemetría)
    def do_GET(self):
        if self.path.startswith('/api/ver_foto'):
            # ===================================================
            # ENDPOINT: Servir imagen física del alumno por QR
            # ===================================================
            from urllib.parse import urlparse, parse_qs
            query = parse_qs(urlparse(self.path).query)
            qr = query.get('qr', [None])[0]
            if not qr:
                self.send_response(404)
                self.end_headers()
                return

            foto_encontrada = None
            base_dir = "colegios_data"
            if os.path.exists(base_dir):
                for colegio in os.listdir(base_dir):
                    path_fotos = os.path.join(base_dir, colegio, "fotos")
                    if os.path.exists(path_fotos):
                        archivo_esperado = os.path.join(path_fotos, f"foto_{qr}.jpg")
                        if os.path.exists(archivo_esperado):
                            foto_encontrada = archivo_esperado
                            break
            
            if foto_encontrada:
                self.send_response(200)
                self.send_header('Content-Type', 'image/jpeg')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                with open(foto_encontrada, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
            return

        # El nuevo Endpoint Oficial Interno para la página web
        if self.path == '/api/live_stats':
            try:
                # Contar cuántas personas han entrado en la historia (soportando NDJSON antiguo)
                with open(DATA_FILE, "r") as f:
                    contenido = f.read().strip()
                
                if not contenido:
                    total_visitas = 0
                elif contenido.startswith('['):
                    total_visitas = len(json.loads(contenido))
                else:
                    total_visitas = len([line for line in contenido.split('\n') if line.strip()])
                
                # Responderle a la página web en secreto
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                respuesta = json.dumps({"total_visitas": total_visitas})
                self.wfile.write(respuesta.encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.end_headers()
            return
            
        # Cuando exista la página netmarlyn original, el túnel la servirá por aquí
        if self.path == '/':
            self.path = '/netmarlyn_website_00/index.html'
        elif not self.path.startswith('/api/'):
            # Redirigir todas las peticiones estáticas a la subcarpeta del website
            self.path = '/netmarlyn_website_00' + self.path
        
        return super().do_GET()

# Levantar el servidor Motor
with socketserver.TCPServer(("", PORT), NetmarlynTrackerHandler) as httpd:
    print(f"==================================================")
    print(f" NETMARLYN LOCAL SERVER INICIADO - MOTOR DE DATOS ")
    print(f"==================================================")
    print(f"Escuchando en puerto: {PORT}")
    print(f"Base de Datos Activa: {DATA_FILE}")
    print(f"Esperando trafico desde Cloudflare Tunnel...")
    print(f"==================================================")
    httpd.serve_forever()
