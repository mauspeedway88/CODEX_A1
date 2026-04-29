import http.server
import socketserver
import json
import os

PORT = 8082
DIRECTORY = "."

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == '/api/archive-memory':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                carnet = data.get('carnet', 'UNKNOWN')
                offloaded_records = data.get('records', [])
                
                if offloaded_records:
                    file_name = f"LONG_TERM_MEMORY_{carnet}.json"
                    file_path = os.path.join(DIRECTORY, file_name)
                    
                    if os.path.exists(file_path):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            try:
                                archive_data = json.load(f)
                            except:
                                archive_data = {"carnet": carnet, "archived_interactions": []}
                    else:
                        archive_data = {"carnet": carnet, "archived_interactions": []}
                        
                    archive_data["archived_interactions"].extend(offloaded_records)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(archive_data, f, indent=4, ensure_ascii=False)
                        
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "archived_count": len(offloaded_records)}).encode('utf-8'))
            except Exception as e:
                print(f"Error archiving memory: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"✅ Servidor MAUNET extendido activo en: http://localhost:{PORT}")
        print(f"🛡️ Listo para recibir guardados incrementales a disco por POST.")
        httpd.serve_forever()
