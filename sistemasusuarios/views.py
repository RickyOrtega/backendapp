from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from sistemasusuarios.models import Empleado
from sistemasusuarios.serializers import EmpleadoSerializer, TelefonoSerializer, EmailSerializer
from django.db import connection

# Registro y loggeo de usuarios:


@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({'error': 'Missing username, email, or password'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

    user = User.objects.create_user(username, email, password)
    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED, content_type='application/json')


@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK, content_type='application/json')
    else:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED, content_type='application/json')

# Funciones CRUD:


# Endpoint para crear un nuevo empleado, al crearse un empleado, obtiene un id automáticamente, el cual se devuelve en la respuesta
@api_view(['POST'])
def crear_empleado(request):
    serializer = EmpleadoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"mensaje": f"Empleado {serializer.data.get("id")} creado con éxito"}, status=status.HTTP_201_CREATED, content_type='application/json')

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')


# Endpoint para obtener todos los empleados
@api_view(['GET'])
def listar_empleados(request):
    empleados = Empleado.objects.all()

    # Si no hay empleados, devolver un mensaje de error
    if not empleados.exists():
        return Response({'error': 'No hay empleados registrados'}, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

    serializer = EmpleadoSerializer(empleados, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json')


# Endpoint para obtener detalles de un empleado
@api_view(['GET'])
def detalle_empleado(request, pk):
    try:
        empleado = Empleado.objects.get(pk=pk)
    except Empleado.DoesNotExist:
        return Response({'error': 'Empleado no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = EmpleadoSerializer(empleado)
    return Response(serializer.data)


# Endpoint para actualizar un empleado
@api_view(['PUT'])
def actualizar_empleado(request, pk):
    try:
        empleado = Empleado.objects.get(pk=pk)
    except Empleado.DoesNotExist:
        return Response({'error': 'Empleado no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    serializer = EmpleadoSerializer(empleado, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response({"mensaje": f"Empleado {serializer.data.get("id")} editado con éxito"}, status=status.HTTP_201_CREATED, content_type='application/json')


# Endpoint para eliminar un empleado
@api_view(['DELETE'])
def eliminar_empleado(request, pk):
    try:
        empleado = Empleado.objects.get(pk=pk)
    except Empleado.DoesNotExist:
        return Response({'error': 'Empleado no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    empleado.delete()
    return Response({"mensaje": "Empleado eliminado satisfactoriamente"},status=status.HTTP_204_NO_CONTENT)


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