# Generated by Django 3.2.6 on 2021-10-21 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_users', '0003_bloguser_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='description',
            field=models.TextField(blank=True, max_length=264, verbose_name='Description'),
        ),
    ]
