from django.urls import path
from . import views

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

]
    