# Generated by Django 3.2.4 on 2023-11-06 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuhelper_app', '0007_alter_empty_classroom_floor_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empty_classroom',
            name='floor_id',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='empty_classroom',
            name='seat_num',
            field=models.IntegerField(default=1),
        ),
    ]
