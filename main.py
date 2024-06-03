from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


import smtplib
from Foxtrot.foxtrot import start_foxtrot
from KTC.ktc import start_ktc
from Moyo.moyo import start_moyo

from config import EMAIL_USERNAME, EMAIL_PASSWORD

EMAIL_RECIPIENT = 'v.kotelnikovdidi@gmail.com'


def start_shops_checking():
    foxtrot_results = start_foxtrot() or []
    moyo_results = start_moyo() or []
    ktc_results = start_ktc() or []

    return {
        "Foxtrot": foxtrot_results,
        "Moyo": moyo_results,
        "KTC": ktc_results
    }


def send_email_with_result(subject: str, body: str, to_email: str):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = EMAIL_USERNAME
    smtp_password = EMAIL_PASSWORD

    # Создаем сообщение
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_email
    msg['Subject'] = subject

    # Добавляем тело сообщения
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


def send_shops_data():
    results = start_shops_checking()
    body = '\n\n'.join([str(result) for result in results])
    send_email_with_result(subject="Shops Data Results", body=body, to_email=EMAIL_RECIPIENT)


# if __name__ == '__main__':
#     send_shops_data()
