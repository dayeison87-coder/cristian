from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('citas/', views.listar_citas, name='listar_citas'),
    path('citas/crear/', views.crear_cita, name='crear_cita'),
    path('citas/cancelar/<str:cita_id>/', views.cancelar_cita, name='cancelar_cita'),
]
    