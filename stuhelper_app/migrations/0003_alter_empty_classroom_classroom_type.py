# Generated by Django 3.2.4 on 2023-11-05 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuhelper_app', '0002_alter_empty_classroom_classroom_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empty_classroom',
            name='classroom_type',
            field=models.CharField(choices=[('1', '普通教室'), ('2', '智慧教室')], default=1, max_length=10),
        ),
    ]
