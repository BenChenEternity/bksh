# Generated by Django 3.2.4 on 2023-11-07 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stuhelper_app', '0012_rename_id_trade_post_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='file_share',
            fields=[
                ('id', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=20, null=True)),
                ('content', models.CharField(max_length=1024, null=True)),
                ('file_link', models.CharField(max_length=256)),
                ('time', models.TimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stuhelper_app.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='post',
            fields=[
                ('id', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=20, null=True)),
                ('content', models.CharField(max_length=1024, null=True)),
                ('category', models.CharField(max_length=16, null=True)),
                ('time', models.TimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stuhelper_app.customuser')),
            ],
        ),
        migrations.DeleteModel(
            name='trade_post',
        ),
    ]