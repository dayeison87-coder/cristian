from pydoc import doc
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from firebase_admin import auth, firestore  
from barveria import initialize_firebase
from functools import wraps
import requests
import os


# Inicializar Firebase
initialize_firebase()
db = firestore.client()

#registro de usuario
def registro_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('email'),
        password = request.POST.get('password'),

        if not email or not password:
            messages.error(request, 'por favor hay que llenar todos lo campos')
            return redirect('registro_usuario')
       
        try:
            #esta parte es para crear un un nuevo usuario en firebase
            user = auth.create_user(email=email, password=password )

            # en esta parte se va a guardar la info adicional del usuario en firestore
            db.collection('usuarios').document(user.uid).set({
                'email': email,
                'uid': user.uid,
                'rol': 'aprendiz',
                'fecha_registro': firestore.SERVER_TIMESTAMP
            })

            messages.success(request, "Usuario registrado exitosamente 😊🎮")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"Error al registrar usuario: {str(e)}")

    return render(request, 'registro.html')

