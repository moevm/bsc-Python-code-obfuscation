import random

from enum import Enum


class ObfuscationOutputType(Enum):
    TEXT_FILE = 'text_file'
    IMAGE = 'image'


class IntNumReprObfuscateType(Enum):

    BIN = 'bin'
    HEX = 'hex'
    OCT = 'oct'
    DEC = 'dec'

    @classmethod
    def get_random_value(cls):
        return random.choice(list(cls))


class IntObfuscationType(Enum):

    CALL_REPR = 'int_call_repr'
    OBFUSCATIONS = 'int_obfuscations'

    @classmethod
    def get_random_value(cls):
        return random.choice(list(cls))


class StrObfuscationType(Enum):

    CALL_REPR = 'str_call_repr'
    OBFUSCATIONS = 'str_obfuscations'

    @classmethod
    def get_random_value(cls):
        return random.choice(list(cls))
