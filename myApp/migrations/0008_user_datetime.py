# Generated by Django 2.0.7 on 2018-09-11 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0007_facility'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='dateTime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
