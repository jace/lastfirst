# -*- coding: utf-8 -*-

import re
from collections import namedtuple

__all__ = ['tokenize']


TypeValue = namedtuple('TypeValue', ['type', 'value'])
separators = {u'.', u',', u'-', u' '}
split_re = re.compile(ur'([., -])')
whitespace_re = re.compile(ur'\s', re.UNICODE)


def tokenize(text):
    """
    Tokenize text into a TypeValue sequence, where type
    is one of 't' (text) and 's' (separator). Separators are always
    a single character and repeating sequences are discarded.
    """
    # First, convert all forms of whitespace to spaces
    text = whitespace_re.sub(u' ', text)
    # Second, split by separators
    split = split_re.split(text)
    # Third, run through components and tag appropriately
    result = []
    for token in split:
        if token:  # We could get empty values at the end of the split list
            if token not in separators:
                result.append(TypeValue('t', token))
            else:
                if result and result[-1].value == token:
                    continue
                else:
                    result.append(TypeValue('s', token))
    return result
