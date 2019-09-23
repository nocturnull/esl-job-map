
from datetime import datetime

from django import template
from django.utils.safestring import mark_safe

from account.models import SiteUser

register = template.Library()


@register.simple_tag
def next_bill_date_en(bill_date: datetime, user: SiteUser) -> str:
    """
    Build the description for the billing cycle in English.

    :param bill_date:
    :param user:
    :return:
    """
    if user.has_subscription and bill_date is not None:
        bill_date_fm = bill_date.strftime('%b %d %Y')
        bill_amount = user.active_subscription.order.plan.formatted_billing_amount
        return mark_safe('<span>Your next billing date is</span>: {} for {}.'.format(bill_date_fm, bill_amount))
    return ''


@register.simple_tag
def next_bill_date_ko(bill_date: datetime, user: SiteUser) -> str:
    """
    Build the description for the billing cycle in Korean.

    :param bill_date:
    :param user:
    :return:
    """
    if user.has_subscription and bill_date is not None:
        bill_date_fm = bill_date.strftime('%Y년 %m월 %d일')
        bill_amount = user.active_subscription.order.plan.formatted_billing_amount
        return mark_safe('<span>회원님의 다음 결제일은</span>: {}, 결제 금액은 {} 입니다.'.format(bill_date_fm, bill_amount))
    return ''
