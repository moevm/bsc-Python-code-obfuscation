import random
import string


class UniqueObfuscatedIdGenerator:

    DEFAULT_ID_LENGTH = 5

    def __init__(self, names=[]):

        self._generated_names = set(names)

    @staticmethod
    def _generate_random_name(len):

        first_symbol = random.choice(string.ascii_letters)
        remaining_symbols = ''.join(
            random.choices(string.ascii_letters + string.digits, k=len - 1)
        )

        random_name = first_symbol + remaining_symbols

        return random_name

    def get_random_name(self, len=DEFAULT_ID_LENGTH):

        random_name = self._generate_random_name(len)

        while random_name in self._generated_names:
            random_name = self._generate_random_name(len)

        self._generated_names.add(random_name)

        return random_name

    def get_random_name_random_len(
        self, min_len=DEFAULT_ID_LENGTH, max_len=DEFAULT_ID_LENGTH
    ):

        random_len = random.randint(min_len, max_len)

        return self.get_random_name(random_len)

    def append_name(self, name):

        self._generated_names.add(name)
