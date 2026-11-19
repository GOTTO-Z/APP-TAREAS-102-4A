import json
from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.http import require_POST

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BaseAuthentication, SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError

from .models import Tarea

# =====================================================
# AUTENTICACION WEB MEDIANTE SESION DJANGO
# =====================================================


def sesion_web_requerida(vista):
    """
    Comprueba que exista una sesión web válida.
    Renueva el Access Token cuando expira.
    """

    #Protege al HTML 
    #Y no permite que nadie ingrese si no tiene una sección echa
    @wraps(vista)
    def funcion(request, *args, **kwargs):

        access = request.session.get("access")
        refresh = request.session.get("refresh")

        if not access or not refresh:
            request.session.flush()
            return redirect("/")

        try:
            AccessToken(access)

        except TokenError:
            try:
                serializer = TokenRefreshSerializer(data={"refresh": refresh})
                serializer.is_valid(raise_exception=True)

                nuevos_tokens = serializer.validated_data

                request.session["access"] = nuevos_tokens["access"]

                if "refresh" in nuevos_tokens:
                    request.session["refresh"] = nuevos_tokens["refresh"]

            except Exception:
                request.session.flush()
                return redirect("/")

        return vista(request, *args, **kwargs)

    return funcion


# =====================================================
# AUTENTICACION JWT DESDE LA SESION WEB
# =====================================================


class SessionJWTAuthentication(BaseAuthentication):
    """
    Permite que las API REST utilicen el JWT almacenado
    en la sesión Django cuando no reciben un Bearer Token.

    También renueva automáticamente el Access Token.
    """

    def authenticate(self, request):

        access = request.session.get("access")
        refresh = request.session.get("refresh")

        # Si no hay sesión JWT, permite continuar con
        # el siguiente método de autenticación.
        if not access and not refresh:
            return None

        if not access or not refresh:
            request.session.flush()
            raise AuthenticationFailed("Sesión expirada. Inicia sesión nuevamente.")

        # Exigir CSRF cuando se utiliza autenticación por sesión.
        SessionAuthentication().enforce_csrf(request)

        jwt_auth = JWTAuthentication()

        try:
            validated_token = jwt_auth.get_validated_token(access)

        except TokenError:
            # Access vencido: intentar renovar con Refresh.
            try:
                serializer = TokenRefreshSerializer(data={"refresh": refresh})
                serializer.is_valid(raise_exception=True)

                nuevos_tokens = serializer.validated_data

                request.session["access"] = nuevos_tokens["access"]

                if "refresh" in nuevos_tokens:
                    request.session["refresh"] = nuevos_tokens["refresh"]

                validated_token = jwt_auth.get_validated_token(
                    request.session["access"]
                )

            except Exception:
                request.session.flush()
                raise AuthenticationFailed(
                    "Tu sesión ha expirado. Inicia sesión nuevamente."
                )

        try:
            usuario = jwt_auth.get_user(validated_token)

            if not usuario.is_active:
                request.session.flush()
                raise AuthenticationFailed("Usuario desactivado.")

        except AuthenticationFailed:
            request.session.flush()
            raise

        return (usuario, validated_token)


# =====================================================
# LOGIN WEB
# =====================================================


def login_pagina(request):

    if request.session.get("access") and request.session.get("refresh"):
        return redirect("/tareas/")

    return render(request, "tareasapp/login.html")


@require_POST
def login_web(request):

    try:
        datos = json.loads(request.body)

        username = datos.get("username")
        password = datos.get("password")

        if not username or not password:
            return JsonResponse(
                {"error": "Debes ingresar usuario y contraseña"}, status=400
            )

        usuario = authenticate(request, username=username, password=password)

        if usuario is None:
            return JsonResponse(
                {"error": "Usuario o contraseña incorrectos"}, status=401
            )

        if not usuario.is_active:
            return JsonResponse({"error": "La cuenta está desactivada"}, status=403)

        # Generar JWT.
        refresh = RefreshToken.for_user(usuario)

        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Crear una nueva sesión Django.
        request.session.flush()

        request.session["access"] = access_token
        request.session["refresh"] = refresh_token
        request.session["usuario"] = usuario.username

        # Expiración de sesión: 30 minutos.
        request.session.set_expiry(1800)

        return JsonResponse(
            {"mensaje": "Inicio de sesión correcto", "usuario": usuario.username}
        )

    except json.JSONDecodeError:
        return JsonResponse({"error": "Solicitud JSON inválida"}, status=400)


# =====================================================
# CERRAR SESION
# =====================================================


@require_POST
def cerrar_sesion(request):

    refresh = request.session.get("refresh")

    if refresh:
        try:
            token = RefreshToken(refresh)
            token.blacklist()

        except TokenError:
            pass

    # Destruir la sesión Django.
    request.session.flush()

    return JsonResponse({"mensaje": "Sesión cerrada correctamente"})


# =====================================================
# VISTAS HTML PROTEGIDAS
# =====================================================


@sesion_web_requerida
def inicio(request):
    return render(request, "tareasapp/inicio.html")


@sesion_web_requerida
def crear_tarea(request):
    return render(request, "tareasapp/crear.html")


@sesion_web_requerida
def detalle_tarea(request, id):
    return render(request, "tareasapp/detalle.html")


@sesion_web_requerida
def editar_tarea(request, id):
    return render(request, "tareasapp/editar.html")


@sesion_web_requerida
def eliminar_tarea(request, id):
    return render(request, "tareasapp/eliminar.html")


# =====================================================
# API REST - TAREAS
# ACEPTA JWT BEARER Y JWT DESDE SESION WEB
# =====================================================


class TareasApiView(APIView):

    authentication_classes = [JWTAuthentication, SessionJWTAuthentication]

    permission_classes = [IsAuthenticated]

    # GET: listar todas las tareas.
    def get(self, request):

        tareas = Tarea.objects.all()

        datos = []

        for tarea in tareas:
            datos.append(
                {
                    "id": tarea.id,
                    "titulo": tarea.titulo,
                    "descripcion": tarea.descripcion,
                    "completada": tarea.completada,
                }
            )

        return Response(datos, status=status.HTTP_200_OK)

    # POST: crear una nueva tarea.
    def post(self, request):

        titulo = request.data.get("titulo")
        descripcion = request.data.get("descripcion")
        completada = request.data.get("completada", False)

        if not titulo or not descripcion:
            return Response(
                {"error": "El titulo y la descripcion son obligatorios"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tarea = Tarea.objects.create(
            titulo=titulo, descripcion=descripcion, completada=completada
        )

        return Response(
            {
                "mensaje": "Tarea creada correctamente",
                "tarea": {
                    "id": tarea.id,
                    "titulo": tarea.titulo,
                    "descripcion": tarea.descripcion,
                    "completada": tarea.completada,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class TareaDetalleApiView(APIView):

    authentication_classes = [JWTAuthentication, SessionJWTAuthentication]

    permission_classes = [IsAuthenticated]

    # GET: consultar tarea por ID.
    def get(self, request, id):

        tarea = get_object_or_404(Tarea, id=id)

        return Response(
            {
                "id": tarea.id,
                "titulo": tarea.titulo,
                "descripcion": tarea.descripcion,
                "completada": tarea.completada,
            },
            status=status.HTTP_200_OK,
        )

    # DELETE: eliminar tarea.
    def delete(self, request, id):

        tarea = get_object_or_404(Tarea, id=id)
        tarea.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    # PUT: actualizar todos los campos.
    def put(self, request, id):

        tarea = get_object_or_404(Tarea, id=id)

        titulo = request.data.get("titulo")
        descripcion = request.data.get("descripcion")
        completada = request.data.get("completada")

        if titulo is None or descripcion is None or completada is None:
            return Response(
                {"error": "Debes enviar todos los campos"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not isinstance(titulo, str) or not titulo.strip():
            return Response(
                {"error": "El titulo es obligatorio"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tarea.titulo = titulo
        tarea.descripcion = descripcion
        tarea.completada = completada
        tarea.save()

        return Response(
            {
                "mensaje": "Tarea Actualizada correctamente",
                "id": tarea.id,
                "descripcion": tarea.descripcion,
                "completada": tarea.completada,
            },
            status=status.HTTP_200_OK,
        )
