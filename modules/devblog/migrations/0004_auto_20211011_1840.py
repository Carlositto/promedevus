# Generated by Django 3.2.6 on 2021-10-11 18:40

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('devblog', '0003_auto_20210928_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reply',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='reply',
            name='user',
        ),
        migrations.RemoveField(
            model_name='like',
            name='post',
        ),
        migrations.AlterField(
            model_name='like',
            name='target_type',
            field=models.ForeignKey(limit_choices_to={'model__in': ['post', 'comment', 'threadecomment']}, on_delete=django.db.models.deletion.PROTECT, to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='post',
            name='date_created',
            field=models.DateField(default=datetime.date(2021, 10, 11), verbose_name='Publication date'),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Reply',
        ),
    ]
