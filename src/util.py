import re


def replace_all(repls, str):
    """
    Applies replacements as described in the repls dictionary on input str.
    :param repls: Dictionary of replacements
    :param str: The string to be changed
    :return: The changed string
    """
    return re.sub('|'.join(re.escape(key) for key in repls.keys()),
                  lambda k: repls[k.group(0)], str)