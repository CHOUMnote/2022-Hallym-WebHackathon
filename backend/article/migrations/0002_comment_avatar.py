# Generated by Django 2.2.28 on 2022-09-19 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='avatar',
            field=models.TextField(default='/public/avatar/default.png'),
        ),
    ]