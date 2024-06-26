import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated


from sistemasusuarios.email_service import send_info_email
from sistemasusuarios.models import Empleado
from sistemasusuarios.serializers import EmpleadoSerializer, TelefonoSerializer, EmailSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.db import connection
from rest_framework.response import Response
from django.middleware.csrf import get_token

# Registro y loggeo de usuarios:


# Vista para obtener el token JWT
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Vista para refrescar el token JWT
class MyTokenRefreshView(TokenRefreshView):
    pass


@csrf_exempt
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    token = get_token(request)

    if user is not None:
        login(request, user)
        return Response({"mensaje": "Inicio de sesión exitoso"}, status=status.HTTP_200_OK)
    else:
        try:
            # Verifica si el usuario ya existe antes de intentar crear uno nuevo
            user = User.objects.get(username=username)
            return Response({"error": "El usuario ya existe, pero la contraseña es incorrecta"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            # Si el usuario no existe, entonces intenta crear uno nuevo
            user = User.objects.create_user(username=username, password=password)
            user.save()

            # Inicia sesión con el nuevo usuario creado
            login(request, user)
            return Response({"mensaje": "Usuario creado y sesión iniciada", "csrfToken": token}, status=status.HTTP_200_OK)


# Funciones CRUD:


# Endpoint para crear un nuevo empleado, al crearse un empleado, obtiene un id automáticamente, el cual se devuelve en la respuesta
@api_view(['POST'])
def crear_empleado(request):

    print(json.dumps(request.data, indent=4))

    datos_empleado = request.data.get('empleado')
    datos_telefono = request.data.get('telefono')
    datos_email = request.data.get('email')

    id_empleado = None

    serializer_empleado = EmpleadoSerializer(data=datos_empleado)
    if serializer_empleado.is_valid():
        serializer_empleado.save()
        id_empleado = serializer_empleado.data.get('id')

    if id_empleado:

        datos_telefono['empleado'] = id_empleado

        serializer_telefono = TelefonoSerializer(data=datos_telefono)
        if serializer_telefono.is_valid():
            serializer_telefono.save(empleado_id=id_empleado)

        datos_email['empleado'] = id_empleado

        serializer_email = EmailSerializer(data=datos_email)
        if serializer_email.is_valid():
            serializer_email.save(empleado_id=id_empleado)

        empleado = Empleado.objects.get(id=id_empleado)
        send_info_email(datos_email.get('email'), empleado)

        return Response({"mensaje": f"Empleado {id_empleado} creado con éxito"}, status=status.HTTP_201_CREATED, content_type='application/json')

    return Response({"error": "No se pudo crear el empleado"}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')


# Endpoint para obtener todos los empleados
@api_view(['GET'])
def listar_empleados(request):

    # Necesitamos obtener todos los empleados, así que usamos el método all() del modelo Empleado
    # También necesitaremos el telefono y el email de cada empleado, por lo que devolveremos los datos de estos también
    empleados = Empleado.objects.all()
    serializer = EmpleadoSerializer(empleados, many=True)

    for empleado in serializer.data:
        empleado_id = empleado.get('id')
        telefono = TelefonoSerializer(Empleado.objects.get(id=empleado_id).telefonos.all(), many=True).data
        email = EmailSerializer(Empleado.objects.get(id=empleado_id).emails.all(), many=True).data
        empleado['telefono'] = telefono
        empleado['email'] = email


    return Response(serializer.data, content_type='application/json', status=status.HTTP_200_OK)


# Endpoint para obtener detalles de un empleado
@api_view(['GET'])
def detalle_empleado(request, pk):
    try:
        empleado = Empleado.objects.get(pk=pk)
    except Empleado.DoesNotExist:
        return Response({'error': 'Empleado no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = EmpleadoSerializer(empleado)
    data = serializer.data.copy()  # Crear una copia de serializer.data
    empleado_id = data.get('id')
    telefono = TelefonoSerializer(Empleado.objects.get(id=empleado_id).telefonos.all(), many=True).data
    email = EmailSerializer(Empleado.objects.get(id=empleado_id).emails.all(), many=True).data
    data['telefono'] = telefono
    data['email'] = email

    return Response(data, content_type='application/json', status=status.HTTP_200_OK)


# Endpoint para actualizar un empleado
@api_view(['PUT'])
def actualizar_empleado(request, pk):

    try:
        empleado = Empleado.objects.get(pk=pk)
    except Empleado.DoesNotExist:
        return Response({'error': 'Empleado no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    datos_empleado = request.data.get('empleado')
    datos_telefono = request.data.get('telefono')
    datos_email = request.data.get('email')

    nuevo_telefono = datos_telefono.copy()
    nuevo_telefono['empleado'] = empleado.id

    nuevo_email = datos_email.copy()
    nuevo_email['empleado'] = empleado.id

    print(json.dumps(datos_telefono, indent=4))

    serializer_empleado = EmpleadoSerializer(empleado, data=datos_empleado)
    if serializer_empleado.is_valid():
        serializer_empleado.save()

    telefono = empleado.telefonos.first()
    email = empleado.emails.first()

    serializer_telefono = TelefonoSerializer(telefono, data=nuevo_telefono)
    if serializer_telefono.is_valid():
        serializer_telefono.save()

    serializer_email = EmailSerializer(email, data=nuevo_email)
    if serializer_email.is_valid():
        serializer_email.save()

    return Response({"mensaje": "Empleado actualizado correctamente"}, status=status.HTTP_200_OK, content_type='application/json')


# Endpoint para eliminar un empleado
@api_view(['DELETE'])
def eliminar_empleado(request, pk):

    # Intentamos obtener el empleado con el id dado
    try:
        empleado = Empleado.objects.get(pk=pk)
    except Empleado.DoesNotExist:
        return Response({'error': 'Empleado no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Si el empleado existe, buscamos su telefono y email y los eliminamos
    telefono = empleado.telefonos.first()
    email = empleado.emails.first()

    telefono.delete()
    email.delete()

    # Finalmente eliminamos el empleado
    empleado.delete()

    return Response({'mensaje': 'Empleado eliminado correctamente'}, status=status.HTTP_200_OK)

# Estaba teniendo algunos problemas con la BD, así que creé un endpoint para probar si la conexión estaba funcionando
# correctamente:


@api_view(['GET'])
def testear_conexion_bd(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            resultado = cursor.fetchone()
        if resultado:
            return Response({'mensaje': 'Conexión a la base de datos exitosa'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No se pudo conectar a la base de datos'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'error': 'Error al conectar con la base de datos: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)