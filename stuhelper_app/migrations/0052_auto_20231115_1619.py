# Generated by Django 3.2.4 on 2023-11-15 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuhelper_app', '0051_follow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='temp_like',
        ),
        migrations.RemoveField(
            model_name='post',
            name='temp_star',
        ),
        migrations.AddField(
            model_name='message',
            name='owner',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='read',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='file_share',
        ),
    ]
