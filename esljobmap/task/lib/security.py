# api/lib/security.py

from jwt.exceptions import DecodeError, ExpiredSignatureError
from typing import Optional

import jwt

from ..settings import *


class JwtAuthentication:
    """JWT token management interface"""

    @classmethod
    def encode(cls) -> str:
        """
        Create a signed token JWT to be distributed for API usage.

        :return:
        """
        return jwt.encode(cls._get_claims(),
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
    def _get_claims(cls) -> dict:
        """
        Create registered and private claims for token signage.

        :return: dict
        """
        return {
            'iss': 'esljobmap',
            'usr': 'kocotask'
        }
