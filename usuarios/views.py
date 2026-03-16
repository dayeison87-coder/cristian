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
