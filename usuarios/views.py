from django.shortcuts import render, redirect
from django.contrib import messages
from firebase_admin import auth, firestore
from firebase.firebase_config import initialize_firebase
from functools import wraps
import requests
import os

# Inicializar Firebase
initialize_firebase()
db = firestore.client()

# ==================================================
# DECORADOR LOGIN REQUIRED
# ==================================================
def login_required_firebase(view_func):
    @wraps(view_func)
    def _wrapper(request, *args, **kwargs):
        if not request.session.get('uid'):
            messages.warning(request, "Debes iniciar sesión.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapper


# ==================================================
# REGISTRO
# ==================================================
def registro_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, 'registro.html')

        try:
            user = auth.create_user(email=email, password=password)

            db.collection('usuarios').document(user.uid).set({
                'email': email,
                'uid': user.uid,
                'fecha_registro': firestore.SERVER_TIMESTAMP
            })

            messages.success(request, "Usuario registrado correctamente 💈")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"Error al registrar: {str(e)}")

    return render(request, 'registro.html')


# ==================================================
# LOGIN
# ==================================================
def iniciar_sesion(request):

    if request.session.get('uid'):
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        api_key = os.getenv('FIREBASE_API_KEY')

        if not api_key:
            messages.error(request, "API KEY no configurada.")
            return render(request, 'login.html')

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        try:
            response = requests.post(url, json=payload)
            data = response.json()

            if response.status_code == 200:
                request.session['uid'] = data['localId']
                request.session['email'] = data['email']
                request.session['idToken'] = data['idToken']
                return redirect('dashboard')
            else:
                messages.error(request, "Correo o contraseña incorrectos.")

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return render(request, 'login.html')


# ==================================================
# LOGOUT
# ==================================================
def cerrar_sesion(request):
    request.session.flush()
    return redirect('login')


# ==================================================
# DASHBOARD
# ==================================================
@login_required_firebase
def dashboard(request):
    uid = request.session.get('uid')

    doc = db.collection('usuarios').document(uid).get()
    datos = doc.to_dict() if doc.exists else {}

    return render(request, 'dashboard.html', {'datos': datos})


# ==================================================
# LISTAR CITAS (solo pendientes)
# ==================================================
@login_required_firebase
def listar_citas(request):
    uid = request.session.get('uid')
    citas = []

    try:
        # Traer solo citas que estén pendientes
        docs = db.collection('citas') \
                 .where('uid_cliente', '==', uid) \
                 .where('estado', '==', 'pendiente') \
                 .stream()

        for doc in docs:
            cita = doc.to_dict()
            cita['id'] = doc.id
            citas.append(cita)

    except Exception as e:
        messages.error(request, f"Error al cargar citas: {str(e)}")

    return render(request, 'citas/listar.html', {'citas': citas})



# ==================================================
# CREAR CITA
# ==================================================
@login_required_firebase
def crear_cita(request):
    if request.method == 'POST':
        uid = request.session.get('uid')
        servicio = request.POST.get('servicio')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')

        try:
            db.collection('citas').add({
                'uid_cliente': uid,
                'servicio': servicio,
                'fecha': fecha,
                'hora': hora,
                'estado': 'pendiente',
                'fecha_creacion': firestore.SERVER_TIMESTAMP
            })

            messages.success(request, "Cita agendada correctamente 💈")
            return redirect('listar_citas')

        except Exception as e:
            messages.error(request, f"Error al crear cita: {str(e)}")

    return render(request, 'citas/crear.html')


# ==================================================
# CANCELAR CITA
# ==================================================
@login_required_firebase
def cancelar_cita(request, cita_id):
    try:
        #borramos la cita.
        db.collection('citas').document(cita_id).delete()
        messages.success(request, "Cita cancelada correctamente 💈")
    except Exception as e:
        messages.error(request, f"Error al cancelar cita: {str(e)}")
    return redirect('listar_citas')

