# Generated by Django 3.2.4 on 2023-11-05 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuhelper_app', '0004_auto_20231105_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='empty_classroom',
            name='campus',
            field=models.CharField(choices=[('1', '大学城校区'), ('2', '五山校区'), ('3', '国际校区')], default='1', max_length=10),
        ),
    ]
