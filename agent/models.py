from django.db import models


class Email(models.Model):
    sender = models.CharField(max_length=255)
    recipient = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    date_sent = models.DateTimeField()

    def __str__(self):
        return self.subject
