import urllib.request
import os

folder = '/Users/mauricio/ANTIGRAVITY_PROJECTS_folder/NETMARLYN_site_websitefoldermake/netmarlyn_site_folder_macstudio/netmarlyn_website_00/assets/qrs_prueba'
os.makedirs(folder, exist_ok=True)

# IDs a incrustar en los QRs de prueba
qrs = {
    'qr_maestro_roberto.png': 'MAESTRO_ROBERTO_3RO_B_SECURE_TOKEN_XYZ',
    'qr_alumno_001.png': 'NL-001_JUAN_PEREZ_SECURE',
    'qr_alumno_002.png': 'NL-002_MARIA_GOMEZ_SECURE',
    'qr_alumno_003.png': 'NL-003_CARLOS_LOPEZ_SECURE'
}

for filename, data in qrs.items():
    url = f"https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={data}&margin=2"
    file_path = os.path.join(folder, filename)
    print(f"Descargando {filename}...")
    urllib.request.urlretrieve(url, file_path)

print("¡4 Códigos QR de prueba generados exitosamente!")
