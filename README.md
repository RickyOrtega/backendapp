# Guía de Instalación y Uso de la Aplicación

Esta guía proporciona instrucciones detalladas sobre cómo instalar, configurar y utilizar la aplicación.

## Requisitos Previos

- Asegúrate de tener instalado Python y pip en tu sistema local.
- Configura un servidor PostgreSQL y asegúrate de tener las credenciales necesarias para conectarte a la base de datos.

## Instalación

1. Clona este repositorio en tu máquina local:
```bash
  git clone https://github.com/RickyOrtega/backendapp.git
```

2. Navega al direction del proyecto:   
```bash
  cd backendapp
```

3. Creamos un entorno virtual en Python:
```bash
  python -m venv venv
```
3.1. Activamos el entorno virtual
3.1.1. MacOS/Linux:
```bash
 source venv/bin/activate
```
3.1.2. Windows:
```bash
 venv\Scripts\activate
```

4. Instalas las dependencias:
```bash
 pip install -r requirements.txt
```

## Ejecución

5. Ejecuta la app usando:
```bash
 python manage.py runserver
```

# Uso

1. La app iniciará el servidor de desarrollo y lo ejecutará en http://localhost:8000 por defecto.
