import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
import os
from dotenv import load_dotenv

# Obtener la ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Ahora sí se puede leer
print("API KEY:", os.getenv("FIREBASE_API_KEY"))


def initialize_firebase():
    try:
        cert_path = os.getenv('FIREBASE_KEYS_PATH')

        if not cert_path:
            cert_path = 'firebase/serviceAccountKey.json'

        if not os.path.isabs(cert_path):
            cert_path = os.path.join(BASE_DIR, cert_path)

        if not os.path.exists(cert_path):
            raise ValueError(
                f"No se ha encontrado el archivo de credenciales en: {cert_path}")

        # Verificar si ya está inicializado
        if not firebase_admin._apps:
            cred = credentials.Certificate(cert_path)
            firebase_admin.initialize_app(cred)

        firestore.client()
        print('✅ Éxito... Django y Firebase están conectados ✅')

    except Exception as e:
        print(f"✖️ Error de conexión ✖️: {e}")
        return None
