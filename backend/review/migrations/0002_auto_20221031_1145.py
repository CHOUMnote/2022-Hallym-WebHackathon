# Generated by Django 2.2.28 on 2022-10-31 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('articleid', models.IntegerField()),
                ('starCount', models.IntegerField(default=0)),
                ('sumStar', models.IntegerField(default=0)),
                ('avgStar', models.TextField()),
                ('visitorCount', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='star',
            field=models.IntegerField(default=0),
        ),
    ]
