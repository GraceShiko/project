# Generated by Django 3.1.2 on 2021-07-22 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
