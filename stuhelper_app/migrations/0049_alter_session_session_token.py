# Generated by Django 3.2.4 on 2023-11-12 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuhelper_app', '0048_alter_session_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='session_token',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
