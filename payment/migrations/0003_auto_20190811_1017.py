# Generated by Django 2.2 on 2019-08-11 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_auto_20190804_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='order', to='payment.Plan'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='site_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='customer_subscriptions', to=settings.AUTH_USER_MODEL),
        ),
    ]
