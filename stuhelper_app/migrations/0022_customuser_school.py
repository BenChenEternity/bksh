# Generated by Django 3.2.4 on 2023-11-08 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuhelper_app', '0021_auto_20231108_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='school',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
