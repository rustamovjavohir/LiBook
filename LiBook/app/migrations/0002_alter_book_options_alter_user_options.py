# Generated by Django 4.0 on 2022-01-25 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['id'], 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
