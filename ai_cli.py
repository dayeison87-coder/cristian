
import requests
import time
import getpass
from google import genai


# -----------------------------
# LOGIN
# -----------------------------
def login_usuario():

    print("--- Login de usuario ---")

    email = input("Ingrese su correo electrónico: ")
    password = getpass.getpass("Ingrese su contraseña: ")

    url_login = "http://127.0.0.1:8000/api/auth/login/"

    try:

        response = requests.post(
            url_login,
            json={
                "email": email,
                "password": password
            }
        )

        if response.status_code == 200:

            print("Login exitoso")

            return response.json().get("token")

        else:

            print("Error en login:", response.text)

    except Exception as e:

        print("Error de conexión:", str(e))

    return None


# -----------------------------
# CONSULTAR CITAS
# -----------------------------
def consultar_mis_citas(token):

    print("CONSULTANDO CITAS...")

    url = "http://127.0.0.1:8000/citas/"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:

        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            print("Error obteniendo citas:", res.text)
            return None

        return res.json()

    except Exception as e:

        print("Error:", e)
        return None


# -----------------------------
# ELIMINAR CITA
# -----------------------------
def eliminar_cita(token, cita_id):

    print(f"ELIMINANDO CITA {cita_id}...")

    url = f"http://127.0.0.1:8000/citas/{cita_id}/delete/"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:

        res = requests.delete(url, headers=headers)

        if res.status_code in [200, 204]:

            print("La cita fue eliminada correctamente.")

        else:

            print("No se pudo eliminar la cita:", res.text)

    except Exception as e:

        print("Error eliminando cita:", str(e))


# -----------------------------
# CONFIGURACIÓN IA
# -----------------------------
API_KEY = "AIzaSyBSxMbwN6rE0WKr8cPxIAoSZTwIfzFn9w4"

client = genai.Client(api_key=API_KEY)

modelo = "gemini-2.5-flash"


# -----------------------------
# PROGRAMA PRINCIPAL
# -----------------------------
token = login_usuario()

if token:

    print("Usuario autenticado, puedes hablar con la IA")

    while True:

        pregunta = input("\nTu: ")

        texto = pregunta.lower()

        if texto in ["salir", "exit", "chao", "adios"]:
            break


        # -----------------------------
        # CONSULTAR CITAS
        # -----------------------------
        if "cita" in texto and "eliminar" not in texto and "borrar" not in texto:

            citas = consultar_mis_citas(token)

            if not citas:

                print("No tienes citas registradas.")

            else:

                print("\nTus citas:\n")

                for c in citas:

                    print("ID:", c.get("id"))
                    print("Titulo:", c.get("titulo"))
                    print("Descripcion:", c.get("descripcion"))
                    print("----------------------")

            continue


        # -----------------------------
        # ELIMINAR CITA
        # -----------------------------
        if "eliminar" in texto or "borrar" in texto:

            partes = pregunta.split()

            if len(partes) >= 3:

                cita_id = partes[-1]

                eliminar_cita(token, cita_id)

            else:

                print("Debes escribir el ID completo.")
                print("Ejemplo: eliminar cita 2KFLQNiK9y5PvYSWtCxh")

            continue


        # -----------------------------
        # CONVERSACIÓN CON IA
        # -----------------------------
        try:

            response = client.models.generate_content(
                model=modelo,
                contents=pregunta
            )

            print("IA:", response.text)

        except Exception as e:

            error = str(e)

            if "429" in error:

                print("Límite alcanzado, esperando 20 segundos...")
                time.sleep(20)

            else:

                print("Error:", error)

