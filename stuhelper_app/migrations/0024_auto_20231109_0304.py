# Generated by Django 3.2.4 on 2023-11-08 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuhelper_app', '0023_customuser_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='password',
        ),
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
    ]
