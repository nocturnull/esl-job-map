# api/lib/security.py

from jwt.exceptions import DecodeError, ExpiredSignatureError
from typing import Optional
import time

import jwt

from ..settings import *


class JwtAuthentication:
    """JWT token management interface"""

    @classmethod
    def encode(cls, email='', expires=False) -> bytes:
        """
        Create a signed token JWT to be distributed for API usage.

        :param email:
        :param expires:
        :return:
        """
        return jwt.encode(cls._get_claims(email, expires),
                          SECRET_KEY,
                          algorithm=SIGNING_ALGORITHM)

    @classmethod
    def decode(cls, encoded) -> Optional[dict]:
        """
        Create a signed token JWT to be distributed for API usage.

        :param encoded:
        :return:
        """
        try:
            return jwt.decode(encoded, SECRET_KEY, algorithms=SIGNING_ALGORITHM)
        except (DecodeError, ExpiredSignatureError):
            pass
        return None

    @classmethod
    def _get_claims(cls, email: str, expires: bool) -> dict:
        """
        Create registered and private claims for token signage.

        :param email:
        :param expires:
        :return:
        """

        claims = {
            'iss': 'esljobmap',
            'usr': 'kocotask'
        }
        if len(email) > 0:
            claims['email'] = email
        if expires:
            claims['exp'] = time.time() + 3600  # 1 hour expiration period.

        return claims
