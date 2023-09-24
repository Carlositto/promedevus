# Generated by Django 3.2.6 on 2021-10-21 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloguser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='E-mail'),
        ),
        migrations.AddField(
            model_name='bloguser',
            name='first_name',
            field=models.CharField(blank=True, max_length=32, verbose_name='First name'),
        ),
        migrations.AddField(
            model_name='bloguser',
            name='last_name',
            field=models.CharField(blank=True, max_length=64, verbose_name='Last name'),
        ),
    ]