# esljobmap/validators.py

import os

from django.forms import ValidationError


def validate_pdf_extension(value):
    """
    Validator for PDF files.

    :param value:
    :return:
    """
    if not value.name.endswith('.pdf'):
        raise ValidationError(u'Only PDF files allowed')


def validate_jpeg_extension(value):
    """
    Validator for JPEG files.

    :param value:
    :return:
    """
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg']
    if ext not in valid_extensions:
        raise ValidationError(u'Only JPEG files allowed')
