from email import message_from_bytes

from django.shortcuts import render
from django.core.mail import send_mail
from .models import Email
from .forms import EmailForm
import imaplib
import io
import email.message
import codecs
import chardet


# def add_email(request):
#     if request.method == 'POST':
#         form = EmailForm(request.POST)
#         if form.is_valid():
#             form.save()
#     else:
#         form = EmailForm()
#     return render(request, 'email_add.html', {'form': form})


def email_list(request):
    # Подключаемся к почтовому серверу
    conn = imaplib.IMAP4_SSL("imap.mail.ru")
    # Логинимся на почтовом сервере
    conn.login("gt-abv@mail.ru", "wmLEKPhXK72f5jW2ZghG")
    # Выбираем нужный почтовый ящик
    conn.select("inbox")
    # Получаем 50 последних email писем в ящике
    _, data = conn.search(None, 'ALL')
    email_ids = data[0].split()[-50:]
    emails = []
    for email_id in email_ids:
        _, data = conn.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]
        email_message = message_from_bytes(raw_email)
        email = Email(
            sender=email_message['From'],
            recipient=email_message['To'],
            subject=email_message['Subject'],
            message=email_message.get_payload(),
            date_sent=email_message['Date']
        )
        emails.append(email)
    conn.close()

    def convert_to_utf8(text, encoding):
        decoded_text = text.decode(encoding)
        encoded_text = codecs.encode(decoded_text, 'utf-8')
        return encoded_text

    for email in emails:
        if hasattr(email, 'encoding'):
            if email.encoding.lower() != 'utf-8':
                email.message = convert_to_utf8(email.message, email.encoding)
        else:
            if isinstance(email.message, str):
                message_bytes = email.message.encode()
            else:
                message_bytes = b''.join(part.as_bytes() for part in email.message)
            detected_encoding = chardet.detect(message_bytes)['encoding']
            if detected_encoding:
                email.encoding = detected_encoding
                if email.encoding.lower() != 'utf-8':
                    email.message = convert_to_utf8(message_bytes, email.encoding)

    return render(request, 'email_list.html', {'emails': emails})


def get_emails(request):
    # Подключаемся к почтовому серверу
    conn = imaplib.IMAP4_SSL("imap.mail.ru")
    # Логинимся на почтовом сервере
    conn.login("gt-abv@mail.ru", "wmLEKPhXK72f5jW2ZghG")
    # Выбираем нужный почтовый ящик
    conn.select("inbox")
    # Получаем все email письма в ящике
    result, data = conn.uid('search', None, "ALL")
    # Преобразуем полученные данные в список email писем
    emails = []
    for uid in data[0].split():
        result, email_data = conn.uid('fetch', uid, '(RFC822)')
        raw_email = email_data[0][1]
        email_message = message_from_bytes(raw_email)
        email = {
            "sender": email_message["From"],
            "recipient": email_message["To"],
            "subject": email_message["Subject"],
            "message": email_message.get_payload(),
            "date_sent": email_message["Date"],
        }
        emails.append(email)
    # Закрываем соединение с почтовым сервером
    conn.close()
    conn.logout()
    context = {"emails": emails}
    return render(request, "templates\email_list.html", context)
