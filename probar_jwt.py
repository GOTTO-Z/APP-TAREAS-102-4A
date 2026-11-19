import requests

URL = "http://127.0.0.1:8000"

datos = {"username": "eric", "password": "1234"}

# 1. Obtener los tokens
respuesta = requests.post(f"{URL}/api/token/", json=datos)

if respuesta.status_code == 200:

    tokens = respuesta.json()
    access = tokens["access"]
    refresh = tokens["refresh"]

    print("Autenticación exitosa")

    # 2. Utilizar Access Token para consultar tareas
    headers = {"Authorization": f"Bearer {access}"}

    respuesta_tareas = requests.get(f"{URL}/api/tareas/", headers=headers)

    print("\nCódigo HTTP:", respuesta_tareas.status_code)

    if respuesta_tareas.status_code == 200:
        print("Tareas registradas:")
        print(respuesta_tareas.json())
    else:
        print("Error:", respuesta_tareas.text)

else:
    print("Error al iniciar sesión:", respuesta.text)


# 3. Crear una nueva tarea mediante POST

nueva_tarea = {
    "titulo": "Tarea creada desde Python",
    "descripcion": "Probando autenticacion JWT",
    "completada": False,
}

respuesta_creacion = requests.post(
    f"{URL}/api/tareas/", json=nueva_tarea, headers=headers
)

print("\nCreacion de tarea:")
print("Codigo HTTP:", respuesta_creacion.status_code)
print(respuesta_creacion.json())


# 4. Actualizar una tarea mediante PUT

id_tarea = 2

datos_actualizados = {
    "titulo": "Tarea actualizada desde Python",
    "descripcion": "Probando el metodo PUT con JWT",
    "completada": True,
}

respuesta_put = requests.put(
    f"{URL}/api/tareas/{id_tarea}/", json=datos_actualizados, headers=headers
)

print("\nActualizacion de tarea:")
print("Codigo HTTP:", respuesta_put.status_code)
print(respuesta_put.json())


# 5. Eliminar una tarea mediante DELETE

id_tarea = 3

respuesta_delete = requests.delete(f"{URL}/api/tareas/{id_tarea}/", headers=headers)

print("\nEliminacion de tarea:")
print("Codigo HTTP:", respuesta_delete.status_code)

if respuesta_delete.status_code == 204:
    print("Tarea eliminada correctamente")
else:
    print(respuesta_delete.text)


# 6. Renovar Access Token utilizando Refresh Token

respuesta_refresh = requests.post(
    f"{URL}/api/token/refresh/", json={"refresh": refresh}
)

print("\nRenovacion de Access Token:")
print("Codigo HTTP:", respuesta_refresh.status_code)

if respuesta_refresh.status_code == 200:

    nuevos_tokens = respuesta_refresh.json()

    access = nuevos_tokens["access"]
    refresh = nuevos_tokens.get("refresh", refresh)

    print("Access Token renovado correctamente")
    print("Nuevo Refresh Token recibido:", "refresh" in nuevos_tokens)

else:
    print("Error al renovar:", respuesta_refresh.text)
