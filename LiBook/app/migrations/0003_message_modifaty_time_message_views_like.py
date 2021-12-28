# Generated by Django 4.0 on 2021-12-28 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_akkount_alter_book_id_alter_box_book_alter_box_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='modifaty_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('book_file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.akkount')),
            ],
        ),
    ]
