# Generated by Django 4.1.7 on 2023-03-13 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
    ]
