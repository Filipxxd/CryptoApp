import random
import re
from unidecode import unidecode


class StringExtensions:

    @staticmethod
    def shuffle(text: str) -> str:
        chars = list(text)
        random.shuffle(chars)
        return ''.join(chars)

    @staticmethod
    def remove_duplicates(text: str) -> str:
        filtered_text = ''

        for char in text:
            if char not in filtered_text:
                filtered_text += char

        return filtered_text

    @staticmethod
    def sanitize_text(text: str, regex_keep=r'[A-Z]') -> str:
        filtered_text = unidecode(text.upper().strip())
        return ''.join(re.findall(regex_keep, filtered_text))

    @staticmethod
    def remove_first_occurrence(text: str, char_to_remove: chr) -> str:
        first_occurrence_index = text.find(char_to_remove)
        if first_occurrence_index != -1:
            return text[:first_occurrence_index] + text[first_occurrence_index + 1:]

        return text
