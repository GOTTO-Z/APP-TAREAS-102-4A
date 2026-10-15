from django.urls import path
from . import views


urlpatterns = [
    #rUTA PAGINA DE LOGIN
    path('', views.loguin_pagina, name= 'login_pagina'),

    #RUTA DE TAREAS POS LOGIN EXITOSO
    path('tareas/', views.inicio, name='inicio'),

    path('crear/', views.crear_tarea, name= "crear_tarea"),
    path('detalle/<int:id>/', views.detalle_tarea, name='detalle_tarea'),
    path('editar/<int:id>', views.editar_tarea, name='editar_tarea'),
    path('eliminar/<int:id>/', views.eliminar_tarea, name='eliminar_tarea')

    #API DE AUTENTICACION
    path('api/login', views.LoginApiView.as_view)
]