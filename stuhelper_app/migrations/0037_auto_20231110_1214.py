# Generated by Django 3.2.4 on 2023-11-10 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuhelper_app', '0036_rename_brief_content_post_brief'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='post',
        #     name='brief',
        # ),
        migrations.AddField(
            model_name='post',
            name='star',
            field=models.IntegerField(default=0),
        ),
    ]