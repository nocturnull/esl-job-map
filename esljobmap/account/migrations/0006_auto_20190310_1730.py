# Generated by Django 2.0.6 on 2019-03-10 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_remove_siteuser_contact_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='siteuser',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='siteuser',
            name='opted_out_of_expired_job_emails',
            field=models.BooleanField(default=False, verbose_name='Don’t receive job expire notification emails'),
        ),
    ]
