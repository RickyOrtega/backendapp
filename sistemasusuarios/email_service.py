# Enviaremos desde sendgrid usando SMTP
import smtplib
from email.mime.text import MIMEText

USER = 'apikey'
PASSWORD = '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'
SERVER = 'smtp.sendgrid.net'
PORT = 587
FROM = "bienvenida.fake.servicio@gmail.com"


def send_info_email(to_email, empleado):
    try:
        server = smtplib.SMTP(SERVER, PORT)
        server.starttls()
        server.login(USER, PASSWORD)

        msg = MIMEText(f'Hola {empleado.nombres} {empleado.apellidos},\n\n'
                       f'Bienvenido a la empresa, esperamos que tu experiencia con nosotros sea la mejor.\n\n'
                       f'Estos son tus datos de ingreso:\n\n'
                          f'Nombres: {empleado.nombres}\n'
                            f'Apellidos: {empleado.apellidos}\n'
                            f'Tipo de identificación: {empleado.tipo_identificacion}\n'
                            f'Identificación: {empleado.identificacion}\n'
                            f'Fecha de ingreso: {empleado.fecha_ingreso}\n'
                            f'Salario mensual: {empleado.salario_mensual}\n'
                       f'Saludos,\n\nLa empresa')
        msg['Subject'] = 'Bienvenido a la empresa'
        msg['From'] = FROM
        msg['To'] = to_email

        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(e)
        return False
