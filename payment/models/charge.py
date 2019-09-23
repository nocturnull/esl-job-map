# payment/models/charge.py

from django.db import models

from account.models.user import SiteUser


class Charge(models.Model):
    STATUS_COMPLETED = 'completed'
    STATUS_REFUNDED = 'refunded'
    STATUS_CHOICES = (
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_REFUNDED, 'Refunded')
    )

    site_user = models.ForeignKey(SiteUser, on_delete=models.DO_NOTHING, related_name='payment_charges')
    stripe_charge_id = models.CharField(blank=False, max_length=1024)
    status = models.CharField(max_length=128, choices=STATUS_CHOICES, default=STATUS_COMPLETED)

    def __str__(self):
        return '{0}-{1}'.format(self.site_user, self.stripe_charge_id)
