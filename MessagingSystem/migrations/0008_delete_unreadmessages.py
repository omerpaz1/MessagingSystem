# Generated by Django 3.0.4 on 2020-10-03 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MessagingSystem', '0007_auto_20201003_0805'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UnreadMessages',
        ),
    ]