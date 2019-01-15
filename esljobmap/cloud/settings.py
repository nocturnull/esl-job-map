"""
Cloud app settings
"""
import os

AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET')
AWS_S3_PARENT_DIR = os.environ.get('AWS_S3_PARENT_DIR', 'staging')
AWS_CDN_BASE_LINK = 'https://cdn.esljobmap.com/'
