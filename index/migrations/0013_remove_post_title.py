# Generated by Django 3.1.3 on 2020-12-04 02:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0012_auto_20201204_0138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
    ]
