import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio
async def send_notification(text, recipient_email):
    '''
        param 1: Text - что отправлять
        param 2: recipient email - куда отправлять 
        Запускать через asyncio.run()
    '''

# Настройки
    smtp_server = "smtp.gmail.com"  # для Gmail
    port = 587                      # порт TLS
    sender_email = "v4n1shnerush@gmail.com"
    password = "fltq wika ojhh ullj"  # см. ниже!

# Создание сообщения
    message = MIMEMultipart("alternative")
    message["Subject"] = "Библиотека №14"
    message["From"] = sender_email
    message["To"] = recipient_email

# Текст и HTML-версия письма

# Добавление частей в сообщение
    message.attach(MIMEText(text, "plain"))

    # Подключение и отправка
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # шифрование
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        print("Письмо отправлено!")
        return "OK"
    except Exception as e:
        print("Ошибка:", e)
        return e
    finally:
        server.quit()
asyncio.run(send_notification("текст, ещё текст", "v4n1shnerush@gmail.com"))