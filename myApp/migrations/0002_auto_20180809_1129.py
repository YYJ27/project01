# Generated by Django 2.0.7 on 2018-08-09 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.IntegerField(max_length=100),
        ),
    ]