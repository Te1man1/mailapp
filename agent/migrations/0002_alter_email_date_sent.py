# Generated by Django 4.2 on 2023-05-14 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='date_sent',
            field=models.DateTimeField(),
        ),
    ]
