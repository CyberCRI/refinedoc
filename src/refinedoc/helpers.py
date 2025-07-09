import re
from typing import Generator


def unify_list_len(to_len_unified: list[list[str]], at_top: bool = False):
    """
    Unify the length of lists in a list of lists by adding empty strings to the shorter lists.
    :param to_len_unified: list of lists to be unified
    :param at_top: if True, add empty strings at the beginning of the lists; if False, add at the end
    :return: None
    """
    maxlen = len(max(to_len_unified, key=len))

    for sublist in to_len_unified:
        place_holders = [""] * (maxlen - len(sublist))
        if at_top:
            for place_holder in place_holders:
                sublist.insert(0, place_holder)
        else:
            sublist.extend([""] * (maxlen - len(sublist)))


def generate_weights(weight_len: int = 5) -> Generator:
    """
    Generate weights for the header/footer detection algorithm.
    :param weight_len: length of the weights list
    :return: generator of weights
    """
    if weight_len <= 0:
        yield None
    if weight_len >= 1:
        yield 1.0
    if weight_len >= 2:
        yield 0.75
    for _ in range(max(0, weight_len - 2)):
        yield 0.5


def neutralize_arabic_numerals(input_str: str, neutral_representation: str = "@"):
    """
    Replace Arabic numerals in a string with neutral representation.
    :param input_str: the input string containing Arabic numerals
    :param neutral_representation: the character to replace Arabic numerals with (e.g., '@')
    :return: a string with Arabic numerals replaced by a neutral representation
    """
    digits = "0123456789"
    map_trans = str.maketrans(digits, neutral_representation * len(digits))
    ret = input_str.translate(map_trans)
    return ret


def neutralize_roman_numerals(input_str: str, neutral_representation: str = "@"):
    """
    Replace Roman numerals in a string with neutral representation.
    :param input_str: the input string containing Roman numerals
    :param neutral_representation: the character to replace Roman numerals with (e.g., '@')
    :return: a string with Roman numerals replaced by a neutral representation
    """
    regex = r"\b[IVXLCDM]{1,4}\b(?![A-Z])"
    ret = re.sub(regex, neutral_representation, input_str, flags=re.IGNORECASE)
    return ret
