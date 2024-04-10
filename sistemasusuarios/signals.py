from django.contrib.auth.models import User

def create_default_user():

    print('Dentro de la función create_default_user()')

    if not User.objects.filter(username='admin').exists():
        print('Dentro del if')

        User.objects.create_superuser('admin', 'test@gmail.com', 'admin')

