# Generated by Django 4.0.1 on 2022-03-11 10:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_user_address_alter_discount_finish_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='finish_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 16, 15, 47, 58, 573777)),
        ),
    ]
