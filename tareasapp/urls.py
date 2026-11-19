from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # LOGIN Y SESION WEB
    path("", views.login_pagina, name="login_pagina"),
    path("web/login/", views.login_web, name="login_web"),
    path("web/logout/", views.cerrar_sesion, name="cerrar_sesion"),
    # PAGINAS DE TAREAS
    path("tareas/", views.inicio, name="inicio"),
    path("crear/", views.crear_tarea, name="crear_tarea"),
    path("detalle/<int:id>/", views.detalle_tarea, name="detalle_tarea"),
    path("editar/<int:id>/", views.editar_tarea, name="editar_tarea"),
    path("eliminar/<int:id>/", views.eliminar_tarea, name="eliminar_tarea"),
    # API REST - TAREAS
    path("api/tareas/", views.TareasApiView.as_view(), name="api_tareas"),
    path(
        "api/tareas/<int:id>/",
        views.TareaDetalleApiView.as_view(),
        name="api_tarea_detalle",
    ),
    # JWT - GENERAR Y RENOVAR TOKENS
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
