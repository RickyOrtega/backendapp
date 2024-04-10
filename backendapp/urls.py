from django.urls import path
from sistemasusuarios.views import (
    listar_empleados,
    detalle_empleado,
    crear_empleado,
    eliminar_empleado,
    actualizar_empleado,
    testear_conexion_bd,
    MyTokenObtainPairView,
    MyTokenRefreshView,
    login_user
)

urlpatterns = [
    # Registro y login
    path('api/login/', login_user, name='login'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),


    # Empleados
    path('api/empleados/crear-empleado/', crear_empleado, name='crear-empleados'),
    path('api/empleados/', listar_empleados, name='empleados'),
    path('api/empleados/<int:pk>/', detalle_empleado, name='detalle-empleado'),
    path('api/empleados/editar-empleado/<int:pk>', actualizar_empleado, name='crear-empleados'),
    path('api/empleados/eliminar-empleado/<int:pk>', eliminar_empleado, name='eliminar-empleados'),

    # Testear BD
    path('testear-conexion-bd/', testear_conexion_bd, name='testear-conexion-bd'),
]
