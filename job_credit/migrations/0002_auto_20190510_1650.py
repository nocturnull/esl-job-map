# Generated by Django 2.2 on 2019-05-10 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_credit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='action',
            field=models.CharField(choices=[('purchase', 'Purchased'), ('consume', 'Consumed'), ('refund', 'Refunded')], default='purchase', max_length=128),
        ),
        migrations.AlterField(
            model_name='record',
            name='amount',
            field=models.FloatField(default=0),
        ),
    ]
