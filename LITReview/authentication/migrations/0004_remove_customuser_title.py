# Generated by Django 4.1.7 on 2023-03-20 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_customuser_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='title',
        ),
    ]