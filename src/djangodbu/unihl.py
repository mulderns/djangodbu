# -*- coding: utf-8 -*-

_unicode_trouble = {
    'spaces': [
        '\u2000',
        '\u2001',
        '\u2002',
        '\u2003',
        '\u2004',
        '\u2005',
        '\u2006',
        '\u2007',
        '\u2008',
        '\u2009',
        '\u200a',
        '\u202f',
        '\u205f',
    ],

    'format': [
        '\u200b',
        '\u200c',
        '\u200d',
        '\u200e',
        '\u200f',
        '\u2060',
        '\u2066',
        '\u2067',
        '\u2068',
        '\u2069',
    ],

    'separators': [
        '\u202a',
        '\u202b',
        '\u202c',
        '\u202d',
        '\u202e',
    ],

    'operators': [
        '\u2061',
        '\u2062',
        '\u2063',
        '\u2064',
        '\u2065',
    ],

    'deprecated': [
        '\u206A',
        '\u206B',
        '\u206C',
        '\u206D',
        '\u206E',
        '\u206F',
    ]
}

symbols = {
    'spaces'    : '␣',
    'format'    : 'ǂ',
    'separators': '÷',
    'operators' : '×',
    'deprecated': '°',
}


C = '\x1b[0;31m'  #if not no_color else ''
E = '\x1b[7;35m'  #if not no_color else ''
B = '\x1b[30;41m' #if not no_color else ''
R = '\033[0m'     #if not no_color else ''

white_space_symbols = [
    (' '    , '·'   , C),
    ('\t'   , '→'   , C),
    ('\n'   , '␤'   , B),
    ('\r'   , '␍'   , B),
    ('\xa0' , '…'   , B),
    ('\x7f' , '␡'   , B),
]


TRANSLATE_TABLE_COLOR = {
    ord(uchar): E + symbols[category] + R for (uchar, category) in [
        (uchar, category) for (category, charlist) in _unicode_trouble.items() for uchar in charlist
    ]
}

TRANSLATE_TABLE_COLOR.update({
    ord(char): color + symbol + R for (char, symbol, color) in white_space_symbols
})


# TRANSLATE_TABLE = {
#     ord(uchar): symbols[category] for (uchar, category) in [
#         (uchar, category) for (category, charlist) in _unicode_trouble.items() for uchar in charlist
#     ]
# }

# TRANSLATE_TABLE.update({
#     ord(char): symbol for (char, symbol, color) in white_space_symbols
# })


def symbolize(text, no_color=False):
    if not text: return text
    if not isinstance(text, str): return text
    return text.translate(TRANSLATE_TABLE_COLOR) #if not no_color else TRANSLATE_TABLE)

__all__ = ['symbolize']
