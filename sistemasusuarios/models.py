from django.db import models

# Los modelos, tratando de ser los más fiel posibles a la BD


class Empleado(models.Model):
	TIPO_IDENTIFICACION_CHOICES = [
		('nit', 'NIT'),
		('cc', 'Cédula de ciudadanía'),
	]

	id = models.AutoField(primary_key=True)
	nombres = models.CharField(max_length=100)
	apellidos = models.CharField(max_length=100)
	tipo_identificacion = models.CharField(max_length=3, choices=TIPO_IDENTIFICACION_CHOICES)
	identificacion = models.CharField(max_length=20)
	fecha_ingreso = models.DateField()
	salario_mensual = models.DecimalField(max_digits=10, decimal_places=2)
	cargo = models.CharField(max_length=100)
	departamento = models.CharField(max_length=100)

	def __str__(self):
		return f"{self.nombres} {self.apellidos}"


class Telefono(models.Model):
	TIPO_CHOICES = [
		('cell', 'Celular'),
		('tel', 'Teléfono'),
	]

	id = models.AutoField(primary_key=True)
	tipo = models.CharField(max_length=4, choices=TIPO_CHOICES)
	numero = models.CharField(max_length=20)
	indicativo = models.CharField(max_length=10)
	empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='telefonos')

	def __str__(self):
		return f"{self.tipo}: {self.numero}"


class Email(models.Model):
	id = models.AutoField(primary_key=True)
	email = models.EmailField(max_length=100)
	empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='emails')

	def __str__(self):
		return self.email
