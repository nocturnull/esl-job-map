import os

"""
Tasks API Settings
"""
AUTH_USERNAME = 'kocotutor'
SIGNING_ALGORITHM = 'HS256'
SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
