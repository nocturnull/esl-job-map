# Generated by Django 2.0.6 on 2018-08-12 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employment', '0002_jobapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpost',
            name='salary',
            field=models.CharField(blank=True, default='', max_length=512),
        ),
        migrations.AlterField(
            model_name='jobpost',
            name='pay_rate',
            field=models.CharField(blank=True, default='', max_length=512),
        ),
    ]
