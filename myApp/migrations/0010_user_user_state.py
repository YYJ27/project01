# Generated by Django 2.0.7 on 2018-09-12 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0009_user_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_state',
            field=models.CharField(default='有效', max_length=100),
        ),
    ]