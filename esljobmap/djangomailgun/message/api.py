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
        """Constructor"""
        self._endpoint = 'https://api.mailgun.net/v3/{}/messages'.format(settings.MAILGUN_DOMAIN)
        self._api_key = settings.MAILGUN_PRIVATE_API_KEY

    def send(self, recipient, subject, body, cc=None, reply_to=None, html=None):
        """
        Send an email through the Mailgun API.

        :param recipient:
        :param subject:
        :param body:
        :param cc:
        :param reply_to:
        :param html:
        :return:
        """
        payload = {
            'from': settings.NO_REPLY_EMAIL,
            'to': recipient,
            'subject': subject,
            'text': body
        }
        if cc is not None:
            payload['cc'] = cc

        if reply_to is not None:
            payload['h:Reply-To'] = reply_to

        if html is not None:
            payload['html'] = html

        requests.post(self._endpoint, data=payload, auth=('api', self._api_key))
