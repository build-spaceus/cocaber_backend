import re

import rstr
from phonenumbers import carrier, is_possible_number, parse
from phonenumbers.phonenumberutil import number_type

from core.constants import BASE_TOKEN_REGEX


def generate_random_string_with_regex(regex=BASE_TOKEN_REGEX):
    return rstr.xeger(regex)


def is_valid_phone_number(phone_number, check_mobile=True):
    """
    Returns True if the input phone number is a valid mobile
    number
    :param phone_number:
    :param check_mobile:
    :return Boolean:
    Ex:
    Input: '+918943535353'
    Output: True

    Input: '000918943003500'
    Output: False

    Input: '+91 8943 353 843'
    Output: False
    """
    if not bool(re.match(r"^\+\d*$", phone_number)):
        return False
    try:
        phone_number = parse(phone_number)
    except Exception:
        return False
    if not is_possible_number(phone_number):
        return False
    if check_mobile and not carrier._is_mobile(number_type(phone_number)):
        return False
    return True
