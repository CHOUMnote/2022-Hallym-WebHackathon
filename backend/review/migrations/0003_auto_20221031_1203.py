# Generated by Django 2.2.28 on 2022-10-31 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_auto_20221031_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageinfo',
            name='avgStar',
            field=models.TextField(default=0),
        ),
    ]
