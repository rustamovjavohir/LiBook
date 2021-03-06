# Generated by Django 4.0.1 on 2022-03-11 05:36

import datetime
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='count',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.IntegerField(default=5000),
        ),
        migrations.AddField(
            model_name='book',
            name='rate',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='sold_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='box',
            name='is_delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_price', models.IntegerField()),
                ('stat', models.DateTimeField(auto_now_add=True)),
                ('finish_date', models.DateTimeField(default=datetime.datetime(2022, 3, 16, 10, 36, 19, 61944))),
                ('is_deleted', models.BooleanField(default=False)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.book')),
            ],
        ),
    ]
