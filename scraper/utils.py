import os
import django

# Укажите путь к вашему модулю с настройками Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scraper.settings')

# Настройка Django
django.setup()
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import get_connection, send_mail

connection = get_connection()
connection.open()  # Явно открываем соединение

def send_email(subject, message, recipient_list):
    """
    Отправка email через настройки Django.

    :param subject: Тема письма
    :param message: Тело письма
    :param recipient_list: Список получателей (list)
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )


# try:
#     send_email(
#         subject="Test Letter",
#         message="Это тестовое письмо, отправленное через Django.",
#         recipient_list=["v.kotelnikovdidi@gmail.com"],
#     )
#     connection.close()
# except Exception as e:
#     print(e)
