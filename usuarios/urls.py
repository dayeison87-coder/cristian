from django.urls import path
from . import views
from .views import ia_usuarios

urlpatterns = [

    # registro
    path('registro/', views.registro_usuario),

    # login API
    path('api/auth/login/', views.login_api),

    # citas
    path('citas/', views.citas),

    # editar cita
    path('citas/<str:cita_id>/', views.editar_cita),

    # eliminar cita
    path('citas/<str:cita_id>/delete/', views.eliminar_cita),
    path("ia/", ia_usuarios, name="ia_usuarios"),# IA
]
    