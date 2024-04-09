from django.urls import path
from sistemasusuarios.views import (
    register_user,
    login_user,
    listar_empleados,
    detalle_empleado,
    crear_empleado,
    eliminar_empleado,
    actualizar_empleado,
    testear_conexion_bd
)

urlpatterns = [
    # Registro y login
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),

    # Empleados
    path('crear-empleado/', crear_empleado, name='crear-empleados'),
    path('empleados/', listar_empleados, name='empleados'),
    path('empleados/<int:pk>/', detalle_empleado, name='detalle-empleado'),
    path('editar-empleado/<int:pk>', actualizar_empleado, name='crear-empleados'),
    path('eliminar-empleado/<int:pk>', eliminar_empleado, name='eliminar-empleados'),

    # Testear BD
    path('testear-conexion-bd/', testear_conexion_bd, name='testear-conexion-bd'),
]