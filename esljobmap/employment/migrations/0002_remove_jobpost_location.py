# Generated by Django 2.0.6 on 2018-12-02 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobpost',
            name='location',
        ),
    ]
