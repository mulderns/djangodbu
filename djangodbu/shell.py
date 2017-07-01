import inspect
import pprint
import re
import types
from collections import defaultdict
from itertools import chain, izip_longest

from django.db.models import Model
from django.db.models.query import QuerySet

from terminalsize import get_terminal_size

# TODO: add support for windows cli

# COLORS FOR TERMINAL

RED = '\033[0;31m'
GREEN = '\033[0;32m'
BLUE = '\033[0;34m'
CYAN = '\033[0;36m'
MAGENTA = '\033[0;35m'
YELLOW = '\033[0;33m'
WHITE = '\033[0;37m'
BLACK = '\033[0;30m'

RED_B = '\033[1;31m'
GREEN_B = '\033[1;32m'
BLUE_B = '\033[1;34m'
CYAN_B = '\033[1;36m'
MAGENTA_B = '\033[1;35m'
YELLOW_B = '\033[1;33m'
WHITE_B = '\033[1;37m'
BLACK_B = '\033[1;30m'

RESET = '\033[0m'


RE_STRIP_TYPE = r"^.*'(.*)'"

COLORS_CATEGORY = {
    'BOOL': BLUE,
    'NUMBER': WHITE,
    'STRING': GREEN,
    'LIST': BLUE_B,
    'FUNCTION': YELLOW,
    'RELATED': MAGENTA,
    'CLASS': YELLOW_B,
    'DATE': CYAN,
    'OTHER': BLACK_B,
}

def type_to_category_value(thing):
    if inspect.ismodule(thing): return ('CLASS', thing.__name__)
    if inspect.isclass(thing): return ('CLASS', thing.__name__)
    if isinstance(thing, bool): return ('BOOL', (GREEN if thing else RED) + str(thing) + RESET)
    if isinstance(thing, int): return ('NUMBER', thing)
    if isinstance(thing, float): return ('NUMBER', thing)
    if isinstance(thing, long): return ('NUMBER', thing)
    if isinstance(thing, str): return ('STRING', thing)
    if isinstance(thing, unicode): return ('STRING', thing)
    if isinstance(thing, list): return ('LIST', len(thing))
    if isinstance(thing, dict): return ('LIST', len(thing))
    if isinstance(thing, tuple): return ('LIST', len(thing))
    if isinstance(thing, types.NoneType): return ('OTHER', None)
    if isinstance(thing, types.TypeType): return ('OTHER', None)
    if str(type(thing)).find('RelatedManager') != -1:
        return ('RELATED', str(thing.count()))
    if isinstance(thing, types.BuiltinFunctionType) or isinstance(thing, types.BuiltinMethodType):
        return ('BUILTIN', None)
    if inspect.ismethod(thing): return ('FUNCTION', None)
    if inspect.isfunction(thing): return ('FUNCTION', None)
    if callable(thing): return ('FUNCTION', None)
    if str(type(thing)).startswith('<class'):
        if str(type(thing)).find('Decimal') != -1:
            return ('NUMBER', thing.__str__())
    if isinstance(thing, Model): return ('RELATED', u"{} > '{}'".format(thing.id, thing.__unicode__() if hasattr(thing,'__unicode__') else thing.__str__()))
    if str(type(thing)).find('datetime') != -1:
        return ('DATE', thing.__str__())
    return ('OTHER', None)


def dorm(obj, ignore_builtin=True, values_only=False, minimal=False, padding=0):
    if type(obj) in (types.ListType, types.DictType, types.TupleType):
        pprint.pprint(obj, indent=2)
        return

    if isinstance(obj, QuerySet):
        for item in obj:
            #dorm(item, values_only=True, padding=4)
            dorm(item, minimal=True)
        print u"= {}{}{}".format(RED, obj.count(), RESET)
        return

    if minimal:
        print u"{}{}{}: {}{}".format(WHITE, obj.id, BLACK_B, RESET, obj)
        return

    if values_only:
        print u"{} : {}".format(obj, type(obj))
    else:
        print u"{} : {}".format(obj, type(obj))
    categories = defaultdict(list)
    terminal_size, _ = get_terminal_size()
    type_max_width = 0

    for attr_name in dir(obj):
        if attr_name.startswith('_') or attr_name == 'objects':
            continue

        attr = None
        try:
            attr = getattr(obj, attr_name)
        except Exception as e:
            print "exception:", e
            pass

        cat, val = type_to_category_value(attr)

        # shorten types
        match = re.search(RE_STRIP_TYPE, str(type(attr)))
        attr_type = match.group(1) if match else str(type(obj))
        if attr_type.find('django.db.models.fields.related.RelatedManager') != -1:
            attr_type = 'RelatedManager'
        elif attr_type.find('django.db.models.fields.related.ManyRelatedManager') != -1:
            attr_type = 'ManyRelatedManager'
        elif attr_type.count('.') > 1:
            attr_type = '.'.join(chain(map(lambda x: x[:2], attr_type.split('.')[:-1]), (attr_type.split('.')[-1],)))

        type_max_width = len(attr_type) if len(attr_type) > type_max_width else type_max_width

        categories[cat].append((attr_name, attr_type, val))

    if values_only:
        for key in categories.keys():
            if not key in [
                    'BOOL',
                    'NUMBER',
                    'STRING',
                    'LIST',
                    'RELATED',
                    #'CLASS',
                    'DATE']:
                categories.pop(key)

    functions = categories.pop('FUNCTION', [])
    builtin = categories.pop('BUILTIN', [])

    if not ignore_builtin:
        functions.extend(builtin)

    lines_left = []
    lines_right = []

    for cat, attr_list in categories.iteritems():
        COLOR = COLORS_CATEGORY[cat] if COLORS_CATEGORY.has_key(cat) else RESET
        for attr_name, attr_type, value in attr_list:
            if value is not None:
                lines_left.append(u"{col1}{type:>{width}}{col2} {name}{rst}: {value}".format(col1=BLACK_B, type=attr_type, col2=COLOR, name=attr_name, rst=RESET, value=value, width=type_max_width))
            else:
                lines_left.append(u"{col1}{type:>{width}}{col2} {name}{rst}".format(col1=BLACK_B, type=attr_type, col2=COLOR, name=attr_name, rst=RESET, width=type_max_width))

    type_max_width_right = max([len(x[1]) for x in functions]) if len(functions) > 0 else 10

    COLOR = COLORS_CATEGORY['FUNCTION'] if COLORS_CATEGORY.has_key(cat) else RESET
    #print cat
    for attr_name, attr_type, value in functions:
        if value is not None:
            lines_right.append(u"{col1}{type:>{width}}{col2} {name}{rst}: {value}".format(col1=BLACK_B, type=attr_type, col2=COLOR, name=attr_name, rst=RESET, value=value, width=type_max_width_rigth))
        else:
            lines_right.append(u"{col1}{type:>{width}}{col2} {name}{rst}".format(col1=BLACK_B, type=attr_type, col2=COLOR, name=attr_name, rst=RESET, width=type_max_width_right))

    width_left = max([len(x) for x in lines_left]) if len(lines_left) > 0 else 10
    width_right = max([len(x) for x in lines_right]) if len(lines_right) > 0 else 10

    # Print in two columns if there is enough space
    # take into account terminal control characters
    padding = ''.join([' ' for _ in range(padding)])

    if width_left - len(BLACK+RED+RESET) + width_right - len(BLACK+RED+RESET) > terminal_size:
        padr, padl = (type_max_width - type_max_width_right, 0) if type_max_width > type_max_width_right else (0, type_max_width_right - type_max_width)
        padr = ''.join([' ' for _ in range(padr)])
        padl = ''.join([' ' for _ in range(padl)])

        for right in lines_right:
            print u"{padding}{:{width}}".format(right, width=width_right, padding=padr)
        for left in lines_left:
            print u"{padding}{:{width}}".format(left, width=width_left, padding=padl)
    else:
        for left, right in izip_longest(lines_left, lines_right, fillvalue=BLACK+RED+RESET):
            print u"{padding}{left:{width_left}} {right:{width_right}}".format(left=left, right=right, width_left=width_left, width_right=width_right, padding=padding)

