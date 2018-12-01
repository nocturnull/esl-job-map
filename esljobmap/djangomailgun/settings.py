"""
Mailgun app settings
"""
import os

MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN')
MAILGUN_PRIVATE_API_KEY = os.environ.get('MAILGUN_PRIVATE_API_KEY')

NO_REPLY_EMAIL = 'no-reply@esljobmap.com'
