import imaplib
from email import message_from_bytes
from django.shortcuts import render
from .models import Email
from .forms import SpamFilterForm
# from keras.models import load_model
# from keras.preprocessing.text import Tokenizer
# from keras.preprocessing.sequence import pad_sequences
# import pandas as pd
# import numpy as np

# def classify_email(email_content):
# model = load_model('spamkiller.h5')
#     tokenizer = Tokenizer(num_words=1000)
#     tokenizer.fit_on_texts([email_content])
#     email_sequences = tokenizer.texts_to_sequences([email_content])
#     email_data = pad_sequences(email_sequences, maxlen=100)
#
#     prediction = model.predict(email_data)
#     spam_probability = prediction[0][0]
#
#     if spam_probability > 0.5:
#         return 'spam'
#     else:
#         return 'not spam'
# def spam_filter(request):
#     if request.method == 'POST':
#         form = SpamFilterForm(request.POST)
#         if form.is_valid():
#             # прогнать через spmkiller
#     else:
#         form = SpamFilterForm()
#     return render(request, 'email_lsit.html', {'form': form})

def email_list(request):
    conn = imaplib.IMAP4_SSL("imap.mail.ru")
    conn.login("gt-abv@mail.ru", "qNB7VLJkvmeMdxJZ6Fy7")
    conn.select("inbox")
    _, data = conn.search(None, 'ALL')
    data = data[0].split()
    emails = []
    for data in data:
        _, data = conn.fetch(data, '(RFC822)')
        raw_email = data[0][1]
        email_message = message_from_bytes(raw_email)
        email = Email(
            sender=email_message['From'],
            recipient=email_message['To'],
            subject=email_message['Subject'],
            message=email_message.get_payload(),
            date_sent=email_message['Date'],

        )
        emails.append(email)
    conn.expunge()
    conn.close()
    conn.logout()

    return render(request, 'email_list.html', {'emails': emails})
