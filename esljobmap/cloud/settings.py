"""
Cloud app settings
"""
import os

AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET')
AWS_S3_BASE_LINK = 'https://s3.{0}.amazonaws.com/{1}/{2}'
