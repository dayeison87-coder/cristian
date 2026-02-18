#  Sistema Web de Gestión para Barbería

##  Descripción

Sistema web desarrollado para la gestión integral de una barbería.  
Permite administrar clientes, citas, servicios y usuarios mediante una arquitectura basada en Backend as a Service (BaaS) utilizando Firebase.

El sistema está compuesto por:

- Frontend: HTML, CSS y JavaScript
- Backend: Firebase Authentication 
- Hosting en la nube con Firebase Hosting

---

#  Objetivos

## Objetivo General

Desarrollar una plataforma web segura y escalable que permita la gestión digital de una barbería.

## Objetivos Específicos

- Implementar autenticación segura.
- Gestionar clientes y citas en tiempo real.
- Diseñar una interfaz responsive.
- Aplicar reglas de seguridad en la base de datos.

---

#  Arquitectura del Sistema

El sistema utiliza una arquitectura Cliente-Servidor basada en servicios en la nube.

Usuario  
⬇  
Frontend (HTML + CSS + JS)  
⬇  
Firebase Authentication  
⬇  
Firebase Hosting  

---

#  Tecnologías Utilizadas

## Frontend
- HTML
- CSS
- JavaScript 

## Backend
- Firebase Authenticat
- Firebase Hosting
<img width="744" height="855" alt="image" src="https://github.com/user-attachments/assets/a9dbb415-e5c1-45bb-b299-883a15a3d4c1" />

---

#  Estructura del Proyecto

```
/clase-1
│
├── clase1/
│   ├── agende/
│   ├── agentes/
│   ├── workflows/
│   ├── firebase/
│   ├── usuarios/
│   │   ├── migrations/
│   │   │   ├── __pycache__/
│   │   │   └── __init__.py
│   │   │
│   │   ├── templates/
│   │   │   └── citas/
│   │   │       ├── crear.html
│   │   │       ├── listar.html
│   │   │       ├── dashboard.html
│   │   │       ├── login.html
│   │   │       └── registro.html
│   │   │
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── venv/
│
├── .env
├── .gitignore
├── db.sqlite3
├── manage.py
└── README.md
```
---

#  Descripción de la Estructura

##  clase1/
Contiene la configuración principal del proyecto Django.

- `settings.py` → Configuración general del proyecto (base de datos, apps instaladas, seguridad).
- `urls.py` → Enrutamiento principal del sistema.
- `asgi.py` → Configuración para despliegue asíncrono.
- `wsgi.py` → Configuración para despliegue en servidores.
- `__init__.py` → Indica que es un paquete de Python.

---

##  usuarios/
Aplicación encargada de la gestión de usuarios y funcionalidades relacionadas con autenticación y citas.

- `models.py` → Define la estructura de la base de datos.
- `views.py` → Contiene la lógica de negocio.
- `urls.py` → Define las rutas internas del módulo.
- `admin.py` → Configuración para el panel de administración.
- `apps.py` → Configuración de la aplicación.
- `tests.py` → Pruebas del sistema.
- `migrations/` → Archivos de migración de base de datos.
- `templates/` → Archivos HTML del sistema.

---

##  templates/citas/
Contiene las vistas del sistema en formato HTML.

- `crear.html` → Formulario para crear citas.
- `listar.html` → Visualización de citas registradas.
- `dashboard.html` → Panel principal del sistema.
- `login.html` → Inicio de sesión.
- `registro.html` → Registro de nuevos usuarios.

---

##  firebase/
Configuración e integración con Firebase para autenticación o servicios en la nube.

---

##  agende/
Módulo relacionado con la gestión de agendas o programación.

---

##  agentes/
Módulo relacionado con gestión de personal o usuarios internos.

---

##  workflows/
Contiene la lógica de procesos o flujos internos del sistema.

---

##  venv/
Entorno virtual de Python que contiene las dependencias del proyecto.

---

##  Archivos principales

- `.env` → Variables de entorno (claves privadas).
- `.gitignore` → Archivos ignorados por Git.
- `db.sqlite3` → Base de datos local de desarrollo.
- `manage.py` → Archivo principal para ejecutar comandos de Django.
- `README.md` → Documentación del proyecto.
---

# Autores
Juan David Cuadros Yeison David Moreno , Kevin Santiago Larrota, harold olivera.
---

#  Seguridad

- Autenticación mediante email y contraseña.
- Reglas de seguridad en Firestore.
- Validación de formularios en frontend.
- Control de acceso por roles.

---

#  Funcionalidades Principales

- Registro de usuarios
- Inicio de sesión
- Gestión de clientes
- Agendamiento de citas
- Panel administrativo
- Actualización en tiempo real

---

#  Requisitos

## Funcionales
- Registro y login funcional.
- CRUD de clientes.
- CRUD de citas.
- Gestión de servicios.

## No Funcionales
- Interfaz responsive.
- Seguridad en autenticación.
- Disponibilidad 24/7.
- Escalabilidad en la nube.

---



