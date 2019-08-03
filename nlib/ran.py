
import random
import string


def random_string(length=8) -> str:
    """
    Randomly generate an alphanumeric string of fixed length.

    https://pynative.com/python-generate-random-string/
    :param length:
    :return:
    """
    pool = string.ascii_letters + string.digits
    return ''.join(random.choice(pool) for i in range(length))
