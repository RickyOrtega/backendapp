from rest_framework import serializers
from .models import Empleado, Telefono, Email
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token


class EmpleadoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Empleado
		fields = '__all__'


class TelefonoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Telefono
		fields = '__all__'


class EmailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Email
		fields = '__all__'
