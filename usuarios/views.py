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
#cambio

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