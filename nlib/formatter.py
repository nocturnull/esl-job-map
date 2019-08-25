

def currency_to_symbol(curr: str) -> str:
    """
    Lazily convert currency code to a symbol.
    Do proper converting when we expand to many currencies.

    :param curr:
    :return:
    """
    if curr == 'USD':
        return '$'
    if curr == 'KRW':
        return '₩'
    return curr
