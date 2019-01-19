"""
Cloud app settings
"""
import os

AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET')
AWS_S3_PARENT_DIR = os.environ.get('AWS_S3_PARENT_DIR', 'staging')
AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION')
AWS_SECURE_CDN_BASE_LINK = 'https://cdn.esljobmap.com/'
AWS_STANDARD_CDN_BASE_LINK = 'https://cdn.esljobmap.com/'
AWS_S3_BASE_LINK = 'https://s3.{0}.amazonaws.com/{1}/{2}'
