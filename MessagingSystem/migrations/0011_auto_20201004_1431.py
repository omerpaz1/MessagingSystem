# Generated by Django 3.0.4 on 2020-10-04 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MessagingSystem', '0010_message_visible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='creation_date',
            field=models.DateField(),
        ),
    ]
