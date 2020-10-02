# Generated by Django 3.0.4 on 2020-10-02 11:34

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('MessagingSystem', '0003_unreadmessages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unreadmessages',
            name='unread_messages',
            field=models.IntegerField(blank=True, default='', max_length=200, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
        ),
    ]
