# djangomailgun/message/api.py
import requests

from .. import settings


class MessageApi(object):
    """
    Interface for the Mailgun Message API.

    When contributing, please follow the API documentation.
    https://documentation.mailgun.com/en/latest/user_manual.html#sending-via-api
    """

    def __init__(self):
        self._endpoint = 'https://api.mailgun.net/v3/{}/messages'.format(settings.MAILGUN_DOMAIN)
        self._api_key = settings.MAILGUN_PRIVATE_API_KEY

    def send(self, sender, recipient, subject, body):
        payload = {
            'from': sender,
            'to': recipient,
            'cc': sender,
            'subject': subject,
            'text': body
        }
        requests.post(self._endpoint, data=payload, auth=('api', self._api_key))
