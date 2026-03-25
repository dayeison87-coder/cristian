from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import auth, firestore
from firebase.firebase_config import initialize_firebase
from functools import wraps
import json
import requests
import os

# Inicializar Firebase
initialize_firebase()
db = firestore.client()


# ==========================================
# DECORADOR PARA VALIDAR TOKEN FIREBASE
# ==========================================
def firebase_token_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JsonResponse({"error": "Token requerido"}, status=401)

        try:
            token = auth_header.split("Bearer ")[1]
            decoded_token = auth.verify_id_token(token)

            request.uid = decoded_token["uid"]

        except Exception:
            return JsonResponse({"error": "Token inválido"}, status=401)

        return view_func(request, *args, **kwargs)

    return wrapper


# ==========================================
# REGISTRO
# ==========================================
@csrf_exempt
def registro_usuario(request):

    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    data = json.loads(request.body)

    email = data.get("email")
    password = data.get("password")

    try:
        user = auth.create_user(
            email=email,
            password=password
        )

        db.collection("usuarios").document(user.uid).set({
            "email": email,
            "uid": user.uid,
            "fecha_registro": firestore.SERVER_TIMESTAMP
        })

        return JsonResponse({
            "mensaje": "Usuario creado correctamente",
            "uid": user.uid
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ==========================================
# LOGIN
# ==========================================
@csrf_exempt
def login_api(request):

    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    data = json.loads(request.body)

    email = data.get("email")
    password = data.get("password")

    api_key = os.getenv("FIREBASE_API_KEY")

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=payload)
    data = response.json()

    if response.status_code == 200:

        return JsonResponse({
            "token": data["idToken"],
            "uid": data["localId"],
            "email": data["email"]
        })

    return JsonResponse({
        "error": "Correo o contraseña incorrectos"
    }, status=401)


# ==========================================
# CITAS (GET Y POST)
# ==========================================
@csrf_exempt
@firebase_token_required
def citas(request):

    # ----------- VER CITAS -----------
    if request.method == "GET":

        citas = []

        docs = db.collection("citas") \
            .where("uid_cliente", "==", request.uid) \
            .stream()

        for doc in docs:
            cita = doc.to_dict()
            cita["id"] = doc.id
            citas.append(cita)

        return JsonResponse(citas, safe=False)

    # ----------- CREAR CITA -----------
    elif request.method == "POST":

        data = json.loads(request.body)

        titulo = data.get("titulo")
        descripcion = data.get("descripcion")

        cita_ref = db.collection("citas").add({
            "uid_cliente": request.uid,
            "titulo": titulo,
            "descripcion": descripcion,
            "estado": "pendiente",
            "fecha_creacion": firestore.SERVER_TIMESTAMP
        })

        return JsonResponse({
            "mensaje": "Cita creada correctamente",
            "id": cita_ref[1].id
        })

    return JsonResponse({"error": "Método no permitido"}, status=405)


# ==========================================
# EDITAR CITA
# ==========================================
@csrf_exempt
@firebase_token_required
def editar_cita(request, cita_id):

    if request.method != "PUT":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    data = json.loads(request.body)

    db.collection("citas").document(cita_id).update({
        "titulo": data.get("titulo"),
        "descripcion": data.get("descripcion"),
        "estado": data.get("estado")
    })

    return JsonResponse({
        "mensaje": "Cita actualizada correctamente"
    })


# ==========================================
# ELIMINAR CITA
# ==========================================
@csrf_exempt
@firebase_token_required
def eliminar_cita(request, cita_id):

    if request.method != "DELETE":
        print(request.method)
        return JsonResponse({"error": "Método no permitido"}, status=405)

    db.collection("citas").document(cita_id).delete()

    return JsonResponse({
        "mensaje": "Cita eliminada correctamente"
    })