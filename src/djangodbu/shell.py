# -*- coding: utf-8 -*-



import sys
import inspect
import pprint
import contextlib

import re
import types
from collections import defaultdict, OrderedDict, Counter
from itertools import chain, zip_longest
from math import ceil
from io import StringIO
from datetime import datetime

class MultiValueDict(object):
    pass

# @contextlib.contextmanager
# def pprint_OrderedDict():
#     pp_orig = pprint._sorted
#     od_orig = OrderedDict.__repr__
#     try:
#         pprint._sorted = lambda x:x
#         OrderedDict.__repr__ = dict.__repr__
#         yield
#     finally:
#         pprint._sorted = pp_orig
#         OrderedDict.__repr__ = od_orig

@contextlib.contextmanager
def pprint_ordered():
    pprint.sorted = lambda arg, *args, **kwargs: arg
    yield
    pprint.sorted = sorted




def _sanitize_defaultdicts_list(l):
    for i, item in enumerate(l):
        l[i] = sanitize_defaultdicts(item)
    return l

def _sanitize_defaultdicts_dict(d):
    if isinstance(d, (defaultdict, Counter, OrderedDict)):
        d = dict(d)
    for k, v in d.items():
        d[k] = sanitize_defaultdicts(v)
    return d

def sanitize_defaultdicts(obj):
    if isinstance(obj, list):
        return _sanitize_defaultdicts_list(obj)
    if isinstance(obj, (dict, OrderedDict, defaultdict)):
        return _sanitize_defaultdicts_dict(obj)
    return obj




try:
    from django.db.models import Model
    from django.db.models.query import QuerySet
    from django.db.models.sql.query import Query, RawQuery
    from django.core.exceptions import FieldError
    from django.db.models.manager import BaseManager
    from django.db.models import Model
    from django.utils.datastructures import MultiValueDict
    from django.core.paginator import Paginator
except:
    print("Could not import Django")
    class Model(object):
        pass
    class QuerySet(object):
        pass
    class Query(object):
        pass
    class RawQuery(object):
        pass


from .terminalsize import get_terminal_size

from .sql import print_query


# TODO: add support for windows cli

# COLORS FOR TERMINAL

RED     = '\033[0;31m'
GREEN   = '\033[0;32m'
BLUE    = '\033[0;34m'
CYAN    = '\033[0;36m'
MAGENTA = '\033[0;35m'
YELLOW  = '\033[0;33m'
WHITE   = '\033[0;37m'
BLACK   = '\033[0;30m'

RED_B     = '\033[1;31m'
GREEN_B   = '\033[1;32m'
BLUE_B    = '\033[1;34m'
CYAN_B    = '\033[1;36m'
MAGENTA_B = '\033[1;35m'
YELLOW_B  = '\033[1;33m'
WHITE_B   = '\033[1;37m'
BLACK_B   = '\033[1;30m'

RESET = '\033[0m'


B_RED     = '\033[0;41m'
B_GREEN   = '\033[0;42m'
B_BLUE    = '\033[0;44m'
B_CYAN    = '\033[0;46m'
B_MAGENTA = '\033[0;45m'
B_YELLOW  = '\033[0;43m'
B_WHITE   = '\033[0;47m'
B_BLACK   = '\033[0;40m'

B_RED_B     = '\033[30;41m'
B_GREEN_B   = '\033[30;42m'
B_BLUE_B    = '\033[30;44m'
B_CYAN_B    = '\033[30;46m'
B_MAGENTA_B = '\033[30;45m'
B_YELLOW_B  = '\033[30;43m'
B_WHITE_B   = '\033[30;47m'
B_BLACK_B   = '\033[30;40m'

BOLD = '\033[1m'
UNDERLINE = '\033[4m'
REVERSE = '\033[7m'

class default_colors(object):
    def __init__(self):
        self.RED     = '\033[0;31m'
        self.GREEN   = '\033[0;32m'
        self.BLUE    = '\033[0;34m'
        self.CYAN    = '\033[0;36m'
        self.MAGENTA = '\033[0;35m'
        self.YELLOW  = '\033[0;33m'
        self.WHITE   = '\033[0;37m'
        self.BLACK   = '\033[0;30m'

        self.RED_B     = '\033[1;31m'
        self.GREEN_B   = '\033[1;32m'
        self.BLUE_B    = '\033[1;34m'
        self.CYAN_B    = '\033[1;36m'
        self.MAGENTA_B = '\033[1;35m'
        self.YELLOW_B  = '\033[1;33m'
        self.WHITE_B   = '\033[1;37m'
        self.BLACK_B   = '\033[1;30m'
        self.B_BLACK   = '\033[0;90m'

        self.RESET = '\033[0m'


        self.B_RED     = '\033[0;41m'
        self.B_GREEN   = '\033[0;42m'
        self.B_BLUE    = '\033[0;44m'
        self.B_CYAN    = '\033[0;46m'
        self.B_MAGENTA = '\033[0;45m'
        self.B_YELLOW  = '\033[0;43m'
        self.B_WHITE   = '\033[0;47m'
        # self.B_BLACK   = '\033[0;40m'

        self.B_RED_B     = '\033[30;41m'
        self.B_GREEN_B   = '\033[30;42m'
        self.B_BLUE_B    = '\033[30;44m'
        self.B_CYAN_B    = '\033[30;46m'
        self.B_MAGENTA_B = '\033[30;45m'
        self.B_YELLOW_B  = '\033[30;43m'
        self.B_WHITE_B   = '\033[30;47m'
        self.B_BLACK_B   = '\033[2;30;90m'

        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'
        self.REVERSE = '\033[7m'
        self.FAINT = '\033[2m'

class red_colors(object):
    def __init__(self):
        self.RED     = '\033[0;31m'
        self.GREEN   = '\033[0;31m'
        self.BLUE    = '\033[0;31m'
        self.CYAN    = '\033[0;31m'
        self.MAGENTA = '\033[0;31m'
        self.YELLOW  = '\033[0;31m'
        self.WHITE   = '\033[0;31m'
        self.BLACK   = '\033[0;31m'

        self.RED_B     = '\033[1;31m'
        self.GREEN_B   = '\033[1;31m'
        self.BLUE_B    = '\033[1;31m'
        self.CYAN_B    = '\033[1;31m'
        self.MAGENTA_B = '\033[1;31m'
        self.YELLOW_B  = '\033[1;31m'
        self.WHITE_B   = '\033[1;31m'
        self.BLACK_B   = '\033[1;31m'

        self.RESET = '\033[0m'


        self.B_RED     = '\033[0;41m'
        self.B_GREEN   = '\033[0;41m'
        self.B_BLUE    = '\033[0;41m'
        self.B_CYAN    = '\033[0;41m'
        self.B_MAGENTA = '\033[0;41m'
        self.B_YELLOW  = '\033[0;41m'
        self.B_WHITE   = '\033[0;41m'
        self.B_BLACK   = '\033[0;41m'

        self.B_RED_B     = '\033[30;41m'
        self.B_GREEN_B   = '\033[30;41m'
        self.B_BLUE_B    = '\033[30;41m'
        self.B_CYAN_B    = '\033[30;41m'
        self.B_MAGENTA_B = '\033[30;41m'
        self.B_YELLOW_B  = '\033[30;41m'
        self.B_WHITE_B   = '\033[30;41m'
        self.B_BLACK_B   = '\033[30;41m'

        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'
        self.REVERSE = '\033[7m'
        self.FAINT = '\033[2m'

_CLR = default_colors()

def theme_set_colors(colors):
    global _CLR
    _CLR = colors

def theme_change_colors(colors_dict, new=False):
    colors = default_colors() if new else _CLR

    for key, value in list(colors_dict.items()):
        if not hasattr(colors, key):
            print('no such color: {}'.format(key))
            return
        setattr(colors, key, value)
    theme_set_colors(colors)


def theme_print_colors():
    for attr_name in dir(_CLR):
        if not attr_name.startswith('_') :
            sequence = getattr(_CLR, attr_name)
            print('{:15} {:18} {}{}{}'.format(attr_name, repr(sequence), sequence, attr_name, RESET))



class COLORS(object):
    def __init__(self):
        self.RED       = '\033[0;31m'
        self.GREEN     = '\033[0;32m'
        self.BLUE      = '\033[0;34m'
        self.CYAN      = '\033[0;36m'
        self.MAGENTA   = '\033[0;35m'
        self.YELLOW    = '\033[0;33m'
        self.WHITE     = '\033[0;37m'
        self.BLACK     = '\033[0;30m'
        self.RED_B     = '\033[1;31m'
        self.GREEN_B   = '\033[1;32m'
        self.BLUE_B    = '\033[1;34m'
        self.CYAN_B    = '\033[1;36m'
        self.MAGENTA_B = '\033[1;35m'
        self.YELLOW_B  = '\033[1;33m'
        self.WHITE_B   = '\033[1;37m'
        self.BLACK_B   = '\033[1;30m'
        self.RESET     = '\033[0m'

COLOR_DEFS = COLORS()

class NOCOLORS(object):
    def __init__(self):
        self.RED = ''
        self.GREEN = ''
        self.BLUE = ''
        self.CYAN = ''
        self.MAGENTA = ''
        self.YELLOW = ''
        self.WHITE = ''
        self.BLACK = ''
        self.RED_B = ''
        self.GREEN_B = ''
        self.BLUE_B = ''
        self.CYAN_B = ''
        self.MAGENTA_B = ''
        self.YELLOW_B = ''
        self.WHITE_B = ''
        self.BLACK_B = ''
        self.RESET = ''

RE_STRIP_TYPE = r"^.*'(.*)'"


COLORS_CATEGORY = {
    'BOOL'    : _CLR.BLUE,
    'NUMBER'  : _CLR.WHITE,
    'STRING'  : _CLR.GREEN,
    'LIST'    : _CLR.BLUE_B,
    'FUNCTION': _CLR.YELLOW,
    'RELATED' : _CLR.MAGENTA,
    'CLASS'   : _CLR.YELLOW_B,
    'DATE'    : _CLR.CYAN,
    'OTHER'   : _CLR.RESET,
    'NONE'    : _CLR.B_BLACK,
    'ERROR'   : _CLR.RED,
}

NOCOLOR = ''

NOCOLORS_CATEGORY = {
    'BOOL'    : NOCOLOR,
    'NUMBER'  : NOCOLOR,
    'STRING'  : NOCOLOR,
    'LIST'    : NOCOLOR,
    'FUNCTION': NOCOLOR,
    'RELATED' : NOCOLOR,
    'CLASS'   : NOCOLOR,
    'DATE'    : NOCOLOR,
    'OTHER'   : NOCOLOR,
    'NONE'    : NOCOLOR,
    'ERROR'   : NOCOLOR,
}

def get_COLORS_CATEGORY():
    return {
        'BOOL'    : _CLR.BLUE,
        'NUMBER'  : _CLR.WHITE,
        'STRING'  : _CLR.GREEN,
        'LIST'    : _CLR.BLUE_B,
        'FUNCTION': _CLR.YELLOW,
        'RELATED' : _CLR.MAGENTA,
        'CLASS'   : _CLR.YELLOW_B,
        'DATE'    : _CLR.CYAN,
        'OTHER'   : _CLR.RESET,
        'NONE'    : _CLR.B_BLACK,
        'ERROR'   : _CLR.RED,
    }

COLUMN_GROUPS = [
    ['FUNCTION', 'BUILTIN'],
    ['RELATED'],
    ['BOOL', 'STRING', 'NUMBER', 'DATE', 'LIST'],
    ['CLASS'],
]

TYPE_SUBSTITUTIONS = [
    ('django.db.models.fields.related.RelatedManager', 'RelatedManager'),
    ('django.db.models.fields.related.ManyRelatedManager', 'ManyRelatedManager'),
    ('django.db.models.fields.related.RelatedObjectDoesNotExist', 'DoesNotExist'),
    ('django.core.exceptions.FieldDoesNotExist', 'FieldDoesNotExist'),
]

def _extract_model(obj):
    obj_repr = repr(obj)
    m = re.match(r"<class '([A-Za-z.]*)\.(.*)'>", obj_repr)
    return m.groups() if m else (None, None)

def type_to_category_value(thing, hluni=False):
    if inspect.ismodule(thing):
        #print "module", uni(thing.__name__)
        return ('CLASS', uni(thing.__name__))
    if isinstance(thing, type):
        #print "type", thing
        return ('OTHER', None)
    if inspect.isclass(thing):
        #print "class", uni(thing.__name__)
        return ('CLASS', uni(thing.__name__))
    if isinstance(thing, bool):
        #print "bool", thing
        return ('BOOL', (_CLR.GREEN if thing else _CLR.RED) + uni(thing) + _CLR.RESET)
    if isinstance(thing, int):
        #print "int", thing
        return ('NUMBER', thing)
    if isinstance(thing, float):
        #print "float", thing
        return ('NUMBER', thing)
    if isinstance(thing, int):
        #print "long", thing
        return ('NUMBER', thing)
    if isinstance(thing, bytes):
        #print "str", uni(thing)
        return ('STRING', uni(thing).replace('\n', '␤').replace('\r', '␍'))
    if isinstance(thing, str):
        #print "unicode", thing
        return ('STRING', thing.replace('\n', '␤').replace('\r', '␍') if not hluni else symbolize(thing))
    if isinstance(thing, list):
        #print "list"
        return ('LIST', len(thing))
    if isinstance(thing, dict):
        #print "dict"
        return ('LIST', len(thing))
    if isinstance(thing, tuple):
        #print "tuple"
        return ('LIST', len(thing))
    if isinstance(thing, type(None)):
        #print "none"
        return ('NONE', None)

    if uni(type(thing)).find('RelatedManager') != -1:
        #print "related manager", uni(thing.count())
        module_path, model = _extract_model(thing.__dict__.get('model', None))
        if model:
            return ('RELATED', '{} {}({})'.format(uni(thing.count()), _CLR.B_BLACK, model))
        return ('RELATED', uni(thing.count()))
    if isinstance(thing, types.BuiltinFunctionType) or isinstance(thing, types.BuiltinMethodType):
        #print "builtin function, builtin method"
        return ('BUILTIN', None)
    if inspect.ismethod(thing):
        #print "method"
        return ('FUNCTION', None)
    if inspect.isfunction(thing):
        #print "function"
        return ('FUNCTION', None)
    if callable(thing):
        #print "callable"
        return ('FUNCTION', None)
    if uni(type(thing)).startswith('<class'):
        if uni(type(thing)).find('Decimal') != -1:
            #print "decimal", uni(thing)
            #return ('NUMBER', thing.__str__())
            return ('NUMBER', uni(thing))
    if isinstance(thing, Model):
        #print "model", uni(thing)
        return ('RELATED', "{} > '{}'".format(thing.pk, uni(thing)))
    if isinstance(thing, QuerySet):
        #print "queryset", uni(thing.count())
        return ('RELATED', uni(thing.count()))
    if uni(type(thing)).find('datetime') != -1:
        #print "datetime", uni(thing)
        return ('DATE', uni(thing))
    if hasattr(thing, '__class__'):
        #print "__class__", uni(thing.name) if hasattr(thing, 'name') and isinstance(thing, (str, unicode)) else None
        # return ('CLASS', uni(thing.name) if hasattr(thing, 'name') and isinstance(thing.name, (str, unicode)) else uni(thing))
        if hasattr(thing, 'name') and isinstance(thing.name, str):
            # print thing
            return ('CLASS', uni(thing.name))
        _repr = uni(thing)
        if not _repr:
            _repr = uni(repr(thing))
        if re.findall(r'object.*at', uni(thing)):
            return ('CLASS', None)
        return ('CLASS', _repr)

    #print "other", uni(repr(thing))
    return ('OTHER', uni(repr(thing)))


def dormm(obj, ignore_builtin=True, values_only=True, minimal=False, padding=0, callable=None, values=None, v=None, color=True, autoquery=True, truncate=None, search=None, s=None, stream=None):
    dorm(obj, ignore_builtin, values_only, minimal, padding, callable, values, v, color, autoquery, truncate, search, s, stream)


# TODO: paginate=True/False
# TODO: search -> search dicts / lists ?
# TODO: dormv -> values only -> dont show types, ids, functions, put values first
def dorm(
    obj,
    ignore_builtin=True,
    values_only=False,
    minimal=False,
    padding=0,
    callable=None,
    callables=None,
    values=None,
    v=None,
    c=None,
    color=True,
    autoquery=True,
    truncate=None,
    search=None,
    s=None,
    stream=None,
    paginate=True,
    references_only=False,
    qs_values=False,
    asc=False,
    annotate=None,
    hluni=False,
):
    """
Debug django ORM. pretty prints:
  - Model instances
    + attribute coloring + grouping
    + attribute values
    + print in parallel columns (if space)
  - QuerySets
    + print all rows in queryset
    + prints selected values (in values=[] fashion) or value from 'callable'
    + paginate, with skipt to page
  - Querys
    + syntax highlight
  - List / Dict / Tuple through pprint

Args:
    obj (object): Object to print.
    ignore_builtin (bool): Skip attributes starting with '_'.  (default True)
    values(list): List of values to print. ['name','price']
    v (string): Shorthand for values in one string. 'name,price'
    callable (string | labmda): attribute name of a function to call (to get a value) for each row in queryset
    color (bool): whether to print ansi color sequences. (default True)
    truncate (int): truncate value lines of model instance to this length. (default None)
    autoquery (bool): Automatically print related as querysets and if queryset contains only 1 record print the object. (default True)
    search (string): Include only attributes matching the search
    s (string): Shorthand for search.

Returns:
    None
    """

    if annotate is not None:
        print(annotate)


    # print lists and such with pprint
    if ignore_builtin and type(obj) in (list, dict, tuple, defaultdict, OrderedDict) or isinstance(obj, set):
        if values_only and stream is not None:
            terminal_width = get_terminal_size()[0]
            pprint.pprint(obj, indent=2, width=terminal_width - padding, stream=stream)
            return
        with pprint_ordered():
            if isinstance(obj, set):
                pprint.pprint(list(obj), indent=2, width=2)
            else:
                obj2 = sanitize_defaultdicts(obj)
                pprint.pprint(obj2, indent=2, width=2)
        return

    # if ignore_builtin and isinstance(obj, defaultdict):
    #     pprint.pprint(dict(obj), indent=2, width=2)
    #     return

    if ignore_builtin and isinstance(obj, MultiValueDict):
        pprint.pprint([(k, v) for (k, v) in obj.items()], indent=2, width=2)
        return

    # print sql
    if ignore_builtin and isinstance(obj, Query) or isinstance(obj, RawQuery):
        print_query(obj)
        return

    # ordered dict -> show as json would?
    if ignore_builtin and isinstance(obj, OrderedDict):
        # with pprint_OrderedDict():
        pprint.pprint(obj, indent=2, width=2, sort_dicts=False)
        return

    # TODO: print members of a module
    #if isinstance(thing, types.ModuleType):
    #    pass

    autoquery_queryset = False
    if autoquery and not isinstance(obj, QuerySet) and hasattr(obj, 'model') and hasattr(obj, 'all'):
        # print "AUTOQUERYING"
        obj = obj.all()
        autoquery_queryset = True

    # iterate querysets
    if isinstance(obj, QuerySet) and ignore_builtin:
        lines_printed = 0
        if v is not None and values is None:
            if '(' in v:
                values = parse_parens_notation(v)
                print(f'values: {values}')
            else:
                values = [val.strip() for val in v.split(',')]

        if c is not None and callables is None:
            callables = [call.strip() for call in c.split(',')]

        if values is None and qs_values:
            values = get_value_attribute_names(obj)

        if values is not None:
            print(obj.model)
            results_per_page = get_terminal_size()[1]-3
            #terminal_width = get_terminal_size()[0]
            pagenum = 0

            for total, done, page in paginateQuerySet(obj, results_per_page, disable=not paginate):
                if pagenum != 0:
                    if pagenum == -1:
                        break
                    if done/results_per_page < pagenum and done < total:
                        continue
                    else:
                        pagenum = 0

                lines = []
                len_callables = len(callables) if callables is not None else 1 if callable is not None else 0
                col_max = [0] * (len(values) + len_callables)

                try:
                    page.values('pk', *values)
                except FieldError as e:
                    errorre = r"Cannot resolve keyword u?'([^']*)' into field. Choices are:(.*)"
                    m = re.match(errorre, e.args[0])
                    if m is None: # not matching -> some other error -> print
                        print(e)
                        return
                    wrong = m.groups()[0]
                    wrong_inserted = False
                    choices = [choice.strip() for choice in m.groups()[1].strip().split(',')]
                    choices_processed = []
                    choice_names = [c for c in choices if not c.endswith('_id')]
                    choice_ids = [c for c in choices if c.endswith('_id')]

                    for choice in choice_names:
                        if not wrong_inserted and choice > wrong:
                            choices_processed.append(_CLR.RED + wrong + _CLR.WHITE + ' <-- ' + _CLR.RED + 'error' + _CLR.RESET)
                            wrong_inserted = True

                        id_handle = choice + '_id'

                        if choice in values:
                            choice = _CLR.GREEN + choice + _CLR.RESET

                        if id_handle in choice_ids:
                            color = _CLR.GREEN if id_handle in values else _CLR.B_BLACK

                            choices_processed.append(choice + color +' (id)'+ _CLR.RESET)
                            choice_ids.remove(id_handle)
                        else:
                            choices_processed.append(choice)

                    if not wrong_inserted:
                        choices_processed.append(_CLR.RED + wrong + _CLR.RESET + ' <-- error')

                    choices_processed.extend(choice_ids)

                    print('FieldError:')
                    for choice in choices_processed:
                        print(_CLR.B_BLACK + '- ' + _CLR.RESET + choice)

                    return

                except Exception as e:
                    print(e)

                if callable:
                    prev_id = None
                    for row, row_object in zip(page.values('pk', *values), page):
                        callable_value = get_callable_value(row_object, callable)
                        item_id, datas = _print_minimal_values(row, values, additional=callable_value, truncate=truncate, hluni=hluni)
                        if item_id == prev_id: item_id = f'{_CLR.BLACK_B}{item_id:<6}'
                        else: prev_id = item_id
                        widths = [lenesc(x) for x in datas]
                        col_max = [max(x) for x in zip(col_max, widths)]
                        lines.append((f'{str(item_id):<6}', datas))  # str because uuid will error for format
                elif callables:
                    prev_id = None
                    for row, row_object in zip(page.values('pk', *values), page):
                        values_callable = [(call, get_callable_value(row_object, call)) for call in callables]
                        item_id, datas = _print_minimal_values(row, values, additional=values_callable, truncate=truncate, hluni=hluni)
                        if item_id == prev_id: item_id = f'{_CLR.BLACK_B}{item_id:<6}'
                        else: prev_id = item_id
                        widths = [lenesc(x) for x in datas]
                        col_max = [max(x) for x in zip(col_max, widths)]
                        lines.append((f'{str(item_id):<6}', datas))
                else:
                    prev_id = None
                    for row in page.values('pk', *values):
                        item_id, datas = _print_minimal_values(row, values, truncate=truncate, hluni=hluni)
                        if item_id == prev_id: item_id = f'{_CLR.BLACK_B}{item_id:<6}'
                        else: prev_id = item_id
                        widths = [lenesc(x) for x in datas]
                        col_max = [max(x) for x in zip(col_max, widths)]
                        lines.append((f'{str(item_id):<6}', datas))

                #print ''.join( v, w in zip(values, col_max) )

                if callable:
                    values.append(callable if isinstance(callable, str) else 'callable')
                    print('    id: ' + '  '.join(["{:<{width}.{width}}".format(squish_to_size(l, w) if l is not None else '', width=w) for l, w in zip(values, col_max)]))
                    values.pop()
                elif callables:
                    print('    id: ' + '  '.join(["{:<{width}.{width}}".format(squish_to_size(l, w) if l is not None else '', width=w) for l, w in zip(values+callables, col_max)]))
                else:
                    print('    id: ' + '  '.join(["{:<{width}.{width}}".format(squish_to_size(l, w) if l is not None else '', width=w) for l, w in zip(values, col_max)]))

                print(''.join(['-' for _ in range(get_terminal_size()[0])]))

                for item_id, datas in lines:
                    print("{col1}{id}{col2}: {reset}{values}".format(col1=_CLR.WHITE, id=item_id, col2=_CLR.B_BLACK, reset=_CLR.RESET, values='  '.join(
                            ["{value}{pad}".format(
                                value=l if l is not None else '',
                                pad=''.join([' ' for _ in range(w - lenesc(l))])
                            ) for l, w in zip(datas, col_max)]
                        )
                    ))
                    lines_printed += 1

                if done < total:
                    try:
                        while True:
                            userinput = input("-- {} ({}) / {} ({}) -- ".format(done, int(done//results_per_page), total, int(ceil(total/float(results_per_page)))))
                            if userinput.startswith('q'):
                                pagenum = -1
                                break
                            try:
                                pagenum = int(userinput)
                                if done/results_per_page >= pagenum:
                                    print("paging error: can't go back")
                                    pagenum = 0

                                elif pagenum > int(ceil(total/float(results_per_page))):
                                    print("paging error: no such page")
                                    pagenum = 0
                                else:
                                    # print "\r\033[F" + ''.join([' ' for _ in xrange(terminal_width-4)]) + '\r',
                                    break
                            except Exception as e:
                                if userinput == '':
                                    pagenum = 0
                                    # print "\r\033[F" + ''.join([' ' for _ in xrange(terminal_width-4)]) + '\r',
                                    break
                                print('paging error: could not parse page number {}'.format(len(userinput)))
                                pass

                    except KeyboardInterrupt as e:
                        break
        else:
            results_per_page = get_terminal_size()[1]-1
            terminal_width = get_terminal_size()[0]
            pagenum = 0
            for total, done, page in paginateQuerySet(obj, results_per_page):
                if pagenum != 0:
                    if pagenum == -1:
                        break
                    if done/results_per_page < pagenum and done < total:
                        continue
                    else:
                        pagenum = 0


                for item in page:
                    if callable is not None:
                        _print_minimal_callable(item, callable_prop=callable)
                    else:
                        # TODO: separate
                        _print_minimal(item)
                    lines_printed += 1

                if done < total:
                    try:
                        while True:
                            userinput = input("-- {} ({}) / {} ({}) -- ".format(done, int(done/results_per_page), total, int(ceil(total/float(results_per_page)))))
                            if userinput.startswith('q'):
                                pagenum = -1
                                break
                            try:
                                pagenum = int(userinput)
                                if done/results_per_page >= pagenum:
                                    print("paging error: can't go back")
                                    pagenum = 0

                                elif pagenum > int(ceil(total/float(results_per_page))):
                                    print("paging error: no such page")
                                    pagenum = 0
                                else:
                                    # print "\r\033[F" + ''.join([' ' for _ in xrange(terminal_width-4)]) + '\r',
                                    break
                            except Exception as e:
                                if userinput == '':
                                    pagenum = 0
                                    # print "\r\033[F" + ''.join([' ' for _ in xrange(terminal_width-4)]) + '\r',
                                    break
                                print('paging error: could not parse page number {}'.format(len(userinput)))
                                pass

                    except KeyboardInterrupt as e:
                        break

        objcount = total if total is not None else obj.count()
        print("= {}{}{}{}".format(_CLR.RED, objcount, _CLR.RESET, ' / {}'.format(lines_printed) if lines_printed and lines_printed != objcount else ''))
        if (
            autoquery
            and v is None
            and values is None
            and callable is None
            and autoquery_queryset
            and objcount == 1
        ):
            _print_orm(obj.first(), ignore_builtin=ignore_builtin, values_only=values_only, padding=padding, color=color, truncate=truncate, asc=asc)

        return

    # else print orm debug
    if search is None and s is not None:
        search = s
    _print_orm(obj, ignore_builtin=ignore_builtin, values_only=values_only, padding=padding, color=color, truncate=50 if truncate is None and not (values_only or references_only) else truncate, search=search, stream=stream, references_only=references_only, asc=asc, hluni=hluni)


def dormmm(obj, ignore_builtin=True, values_only=False, minimal=False, padding=0, callable=None, values=None, v=None, color=True, autoquery=True, truncate=None, search=None, s=None, stream=None):
    if search is None and s is not None:
        search = s
    _print_orm(obj, ignore_builtin=ignore_builtin, values_only=values_only, padding=padding, color=color, truncate=truncate, search=search, stream=stream)


def paginateQuerySet(queryset, pagerowcount, autosense=True, disable=False):
    # total = queryset.count()
    if disable:
        yield None, None, queryset
        return
    # print "paginating {}/{}".format(total, pagerowcount)

    # set explicit order_by id if not specified (to silence warning)
    if not queryset.ordered:
        if hasattr(queryset.model, 'id'): queryset = queryset.order_by('id')
        elif hasattr(queryset.model, 'pk'): queryset = queryset.order_by('pk')

    paginator = Paginator(queryset, pagerowcount)
    total = paginator.count # excecute query
    # autosense paginates only when output is more than 2.5 x screen size
    if autosense and total / float(pagerowcount) <= 2.5:
        yield total, total, queryset

    else:
        done = 0
        on_page = 1
        while done < total:
            yield total, min(done + pagerowcount, total), paginator.page(on_page).object_list#queryset[done:done + pagerowcount]
            done += pagerowcount
            on_page += 1


def _print_minimal_values(values_row, selected_values, additional=None, truncate=40, hluni=False):
    '''values_row has contents of qs.values(...)'''
    item_id = values_row.pop('pk')
    values2 = []

    for key in selected_values:
        data = values_row.get(key)
        if isinstance(data, str):
            values2.append(nice_string(data, maxlen=truncate, show_whitespace=hluni))
        #     values2.append(unicode(data.decode('utf-8', 'replace'), 'utf-8', 'replace') + 'X')
        # elif isinstance(data, unicode):
        #     #values2.append(data.encode('utf-8', 'replace') + 'Z')
        #     #values2.append(data.encode('utf-8', 'replace').decode('utf-8','replace'))
        #     #print data
        #     values2.append(data)
        elif isinstance(data, bool):
            if data:
                values2.append(_CLR.GREEN+'True'+_CLR.RESET)
            else:
                values2.append(_CLR.RED+'False'+_CLR.RESET)
        elif isinstance(data, datetime):
            values2.append(data.strftime('%y%m%d-%H%M'))

        elif data is None:
            values2.append(_CLR.B_BLACK+'None'+_CLR.RESET)
        else:
            # print '>>', data
            values2.append(str(data))

    if additional is not None:
        if isinstance(additional, list):
            if isinstance(additional[0], tuple):
                values2 += [a[1] for a in additional]
            else:
                values2 += additional
        else:
            values2.append(additional)

    return (item_id, values2)

# def _print_minimal_values_pprint(row, selected_values):
#     item_id = row.pop('pk')
#     print "{}{}{}: {}{}".format(WHITE, item_id, BLACK_B, RESET, pprint.pformat(row))

# TODO: deduplicate in print_minimal_callable
def get_callable_value(obj, callable_prop):
    _id = ''
    if hasattr(obj, 'id'):
        _id = obj.id
    elif hasattr(obj, 'pk'):
        _id = obj.pk
    value = _id

    if isinstance(callable_prop, types.LambdaType):
        value = callable_prop(obj)

    elif callable_prop and hasattr(obj, callable_prop):
        attr = getattr(obj, callable_prop)
        if not callable(attr):
            value = attr
        else:
            try:
                value = attr()
            except Exception as e:
                value = 'ERR: {}'.format(e)

    elif callable_prop is not None and not hasattr(obj, callable_prop):
        raise Exception("No callable prop found '{}', choices are: \n{}".format(
            callable_prop,
            ',\n'.join(_get_callables(obj))
        ))

    elif callable_prop is None and hasattr(obj, 'name'):
        attr = getattr(obj, 'name')
        if not callable(attr):
            value = attr
        else:
            try:
                value = attr()
            except Exception as e:
                value = 'ERR: {}'.format(e)

    elif callable_prop is None and hasattr(obj, '__str__'):
        value = uni(obj)

    # print value

    return uni(value)

def _get_callables(obj):
    callables = []
    for attr_name in dir(obj):
        if attr_name.startswith('_') or attr_name in ('objects', 'active_objects'):
            continue
        try:
            attr = getattr(obj, attr_name)
        except Exception as e:
            print('Exception getting callable attribute', attr_name, e)
        if callable(attr):
            callables.append(attr_name)
    return callables

def _print_minimal_callable(obj, callable_prop):
    _id = ''
    if hasattr(obj, 'id'):
        _id = obj.id
    elif hasattr(obj, 'pk'):
        _id = obj.pk
    value = _id

    if isinstance(callable_prop, types.LambdaType):
        value = callable_prop(obj)

    elif callable_prop and hasattr(obj, callable_prop):
        attr = getattr(obj, callable_prop)
        if not callable(attr):
            value = attr
        else:
            value = attr()

    elif callable_prop is None and hasattr(obj, 'name'):
        attr = getattr(obj, 'name')
        if not callable(attr):
            value = attr
        else:
            value = attr()

    elif callable_prop is None and hasattr(obj, '__str__'):
        value = str(obj.__str__())

    print("{}{}{}: {}{}".format(_CLR.WHITE, _id, _CLR.B_BLACK, _CLR.RESET, uni(value)))


def _print_minimal(obj, annotation=None):
    if isinstance(obj, str):
        print(obj)
        return

    _id = ''
    if hasattr(obj, 'id'):
        _id = obj.id
    elif hasattr(obj, 'pk'):
        _id = obj.pk
    value = _id

    if hasattr(obj, '__unicode__'):
        value = obj.__unicode__()

    elif hasattr(obj, '__str__'):
        value = str(obj.__str__())

    elif hasattr(obj, 'name'):
        attr = getattr(obj, 'name')
        if not callable(attr):
            value = attr

    print("{}{}{}: {}{}  {}{}{}".format(_CLR.WHITE, _id, _CLR.B_BLACK, _CLR.RESET, uni(value), _CLR.B_BLACK, annotation if annotation is not None else '', _CLR.RESET))


def dorme(*args, **kwargs):
    import ipdb
    try:
        dorm(*args, **kwargs)
    except Exception as e:
        print(e)
        ipdb.post_mortem()


ansisequence = re.compile(r'\x1B\[[^A-Za-z]*[A-Za-z]')

def strip_ansi(line):
    return ansisequence.sub('', line)

def strip_ansi_list(lines):
    return [ansisequence.sub('', line) for line in lines]

def lenesc(line):
    ''' length of line without ansi sequences'''
    if line is None:
        return 0
    return len(ansisequence.sub('', line))

def lenescU(line):
    if line is None:
        return 0
    if isinstance(line, str) or isinstance(line, str):
        return lenesc(line)
    return len("{}".format(line))

def ansilen(line):
    ''' length of ansi sequence'''
    return len(line) - lenesc(line)

def get_value_attribute_names(qs):
    obj = qs.first()
    if not obj:
        print('no rows?')
        return None

    attr_names = []
    for attr_name in dir(obj):
        if (
            attr_name.startswith('_')
            or attr_name == 'objects'
            #or attr_name == 'Meta'
        ):
            print('{} : is ignored'.format(attr_name))
            continue

        attr = None
        try:
            attr = getattr(obj, attr_name)
            cat, val = type_to_category_value(attr)
        except Exception as e:
            print("E", attr_name, e)
            continue

        if not cat in ['BOOL', 'STRING', 'NUMBER', 'DATE', 'LIST']:
            print(attr_name, ':', 'is not value')
            continue

        is_prop = isinstance(getattr(type(obj), attr_name, None), property)
        is_const = attr_name.isupper()
        is_id = re.match(r'(.*_)?id$', attr_name)
        if (is_prop or is_const or is_id):
            print(attr_name, ':', 'is prop / const / id')
            continue

        attr_names.append(attr_name)
    return attr_names

def nice_string(text, maxlen=0, show_whitespace=False):
    if show_whitespace:
        # raise Exception('not implemented')
        text = symbolize(text)
    else:
        text = text.replace('\n', ' ').replace('\t', ' ')

    if maxlen and len(text) > maxlen:
        text = text[:maxlen - 1] + '…'

    return text


def detect_encoding():
    iso_soft_hyphen = '­'
    uni_zero_width_space = '\u200b'

    try:
        sys.stdout.write(uni_zero_width_space)
        return 'utf'
    except:
        pass

    try:
        sys.stdout.write(iso_soft_hyphen)
        return 'iso'
    except:
        pass

    return 'ascii'


# TODO: retain first letter even if vocal
# TODO: split into chunks around space / _ and squish each part individually
# TODO: pass in list of other words to detect similarities and drop them
def squish_to_size(string, size):
    re_voc = re.compile(r'[aeiouyåäö]')
    re_con = re.compile(r'[bcdfghjklmnpqrstvwxz]')
    re_pun = re.compile(r'[\.:-_ !\(\)]')

    string = string.strip()

    while len(string) > size:
        rstring = string[::-1]
        count_pun = len(re_pun.findall(string))
        if count_pun > 0:
            position = len(string) - 1 - re_pun.search(rstring).start()
            string = string[:position] + string[position + 1:]
            continue

        count_voc = len(re_voc.findall(string))
        if count_voc > 0:
            position = len(string) - 1 - re_voc.search(rstring).start()
            string = string[:position] + string[position + 1:]
            continue

        count_con = len(re_con.findall(string))
        if count_con > 0:
            position = len(string) - 1 - re_con.search(rstring).start()
            string = string[:position] + string[position + 1:]
            continue

        string = string[:-1]
    return string

def squish_to_size2(string, size):
    re_voc = re.compile(r'[aeiouyåäö]')
    re_con = re.compile(r'[bcdfghjklmnpqrstvwxz]')
    re_pun = re.compile(r'[\.:-_ !\(\)]')

    string = string.strip()
    string = string.replace('__', '_')
    parts = string.split('_')

    length = len(string)

    while sum([len(part) for part in parts]) > size:
        for part_i, part in enumerate(parts):
            # TODO: here

            rstring = string[::-1]
            count_pun = len(re_pun.findall(string))
            if count_pun > 0:
                position = len(string) - 1 - re_pun.search(rstring).start()
                string = string[:position] + string[position + 1:]
                continue

            count_voc = len(re_voc.findall(string))
            if count_voc > 0:
                position = len(string) - 1 - re_voc.search(rstring).start()
                string = string[:position] + string[position + 1:]
                continue

            count_con = len(re_con.findall(string))
            if count_con > 0:
                position = len(string) - 1 - re_con.search(rstring).start()
                string = string[:position] + string[position + 1:]
                continue


            string = string[:-1]
    return string



import itertools, sys
anim_busy = itertools.cycle(['|', '/', '-', '\\'])
def squish_to_size3(text, size, other_labels):
    re_voc = re.compile(r'[aeiouyåäö]')
    re_con = re.compile(r'[bcdfghjklmnpqrstvwxz]')
    re_pun = re.compile(r'[\.: !\(\)]')

    text = text.strip()
    major_chunks = text.split('__')

    # parts = text.split('_')

    length = len(text)

    if len(major_chunks) > 1:
        pass

    while len(string) > size:

        sys.stderr.write(next(anim_busy))
        for part_i, part in enumerate(parts):
            # TODO: here

            rtext = text[::-1]
            count_pun = len(re_pun.findall(text))
            if count_pun > 0:
                position = len(text) - 1 - re_pun.search(rtext).start()
                text = text[:position] + text[position + 1:]
                continue

            count_voc = len(re_voc.findall(text))
            if count_voc > 0:
                position = len(text) - 1 - re_voc.search(rtext).start()
                text = text[:position] + text[position + 1:]
                continue

            count_con = len(re_con.findall(text))
            if count_con > 0:
                position = len(text) - 1 - re_con.search(rtext).start()
                text = text[:position] + text[position + 1:]
                continue


            text = text[:-1]
        sys.stderr.write('\b')
    return text


def dormnc(*args, **kwargs):
    dorm(*args, color=False, **kwargs)


class Category(object):
    def __init__(self, category='', attr_list=None, type_max_width=0, value_max_width=0, lines=None):
        self.category = category
        self.attr_list = attr_list if attr_list else []
        self.type_max_width = type_max_width
        self.value_max_width = value_max_width
        self.lines = lines if lines else []

    def update_max_width(self, width):
        if width > self.type_max_width:
            self.type_max_width = width

    def __str__(self):
        return "{}({}+{})".format(self.category, self.type_max_width, self.value_max_width)

    # def __str__(self):
    #     return "hello"


class Group(object):
    def __init__(self, categories=None, width=(0,0), height=0):
        self.categories = categories if categories else []
        self.width = width

    def update_width(self, width):
        if self.width[0] < width[0]:
            self.width = (width[0], self.width[1])
        if self.width[1] < width[1]:
            self.width = (self.width[0], width[1])

    def get_height(self):
        return sum([len(cat.lines) for cat in self.categories])

    def __unicode__(self):
        return "cats:{} width:{}".format(len(self.categories), self.width)

    def __str__(self):
        return "{}/{}".format(','.join([x.__str__() for x in self.categories]), self.width)

    def __repr__(self):
        return self.__str__()


def calculate_width(groups):
    temp = [c.type_max_width for g in groups for c in g.categories]
    type_max_width = max(temp) if temp else 0

    width = 0
    for group in groups:
        # max type + max value
        if not group.categories:
            continue
        # gmtw = max([cat.type_max_width for cat in group.categories])

        gmvw = max([lenesc(attr_name) + (lenesc("{}".format(uni(val))) if val is not None else -2) + 2 for cat in group.categories for attr_name, _, val in cat.attr_list])
        # print 'GMVW', gmvw

        # width = gmtw + 1 + gmvw
        # gmtw = type_max_width
        result = type_max_width + 1 + gmvw
        width = result if result > width else width

    return width + 1


# TODO: fix unicode / str : convert all str to unicode
def _print_orm(obj, ignore_builtin=True, values_only=False, padding=0, color=True, truncate=None, search=None, stream=None, references_only=False, asc=False, hluni=False):
    colors_category = NOCOLORS_CATEGORY if not color else get_COLORS_CATEGORY()

    supported_encoding = detect_encoding()
    if supported_encoding == 'ascii':
        print("output ascii")
        asc = True

    print_asc = (lambda x: print(x)) if not asc else (lambda x: print(x.encode('ascii', 'replace').decode()))

    # print object identifier
    if stream is not None:
        stream.write( ("{} : {}\n".format(uni(obj), type(obj))) )
    else:
        print_asc("{} : {}".format(uni(obj), type(obj)))

    categories = defaultdict(Category)

    # sort object data into categories with names and values
    for attr_name in dir(obj):
        if (ignore_builtin and attr_name.startswith('_')) or attr_name == 'objects':
            continue

        attr = None
        try:
            attr = getattr(obj, attr_name)
            cat, val = type_to_category_value(attr, hluni=hluni)
        except Exception as e:
            print_asc("exception: {}".format(e))
            cat = 'ERROR'
            val = ''
            error = uni(type(e))
            error = re.sub(r"<type '([^']*)'>", r'\g<1>', error)
            error = re.sub(r"<class '([^']*)'>", r'\g<1>', error)

        if values_only:
            if not cat in ['BOOL', 'STRING', 'NUMBER', 'DATE', 'LIST', 'CLASS']:
                # print 'skip %s' % cat
                continue

            if cat == 'LIST':
                # val = pprint.pformat(attr)
                val_buffer = StringIO()
                dorm(attr, values_only=values_only, padding=padding + 2, stream=val_buffer)
                val_buffer.flush()
                val_buffer.seek(0)
                lines = [uni(line) for line in val_buffer.readlines()]
                if len(lines) > 1:
                    PAD = ''.join([' ' for _ in range(padding+8)])
                    val = '\n' + ''.join(PAD+line for line in lines).rstrip()
                else:
                    val = ''.join(line for line in lines).rstrip()


            #categories[cat].update_max_width(0)
            #categories[cat].attr_list.append((attr_name, '', val))
            #continue
        elif references_only:
            if not cat in ['RELATED']:
                continue
            if isinstance(attr, BaseManager):
                if attr.count() == 0:
                    continue
                val = '[{}]'.format(', '.join([str(x) for x in attr.values_list('pk', flat=True)]))
            elif isinstance(attr, Model):
                val = '{}'.format(attr.pk)


        if val is not None and truncate and len(attr_name) + lenescU(val) > truncate:
            val = ('{}'.format(val))[:truncate - (len(attr_name) + 2)] + _CLR.B_BLACK + '..'

        # shorten some common types
        match = re.search(RE_STRIP_TYPE, uni(type(attr)))
        attr_type = match.group(1) if match else uni(type(obj))

        if references_only:
            attr_type = ''

        if cat == 'ERROR':
            attr_type = error

        for type_string, substitution in TYPE_SUBSTITUTIONS:
            if attr_type.find(type_string) != -1:
                attr_type = substitution
                break
        else:
            if attr_type.count('.') > 1:
                attr_type = '.'.join(chain([x[:2] for x in attr_type.split('.')[:-1]], (attr_type.split('.')[-1],)))

        if search is not None:
            if not (
                attr_name.lower().find(search.lower()) != -1 or
                (isinstance(val, str) and val.lower().find(search.lower()) != -1)
            ):
                continue

        if cat not in categories:
            categories[cat].category = cat

        is_prop = isinstance(getattr(type(obj), attr_name, None), property)
        is_const = attr_name.isupper()
        is_id = re.match(r'(.*_)?id$', attr_name)

        categories[cat].update_max_width(lenesc(attr_type))
        if is_prop:
            attr_name += _CLR.RED_B + '@'
        if is_const:
            attr_name = _CLR.BOLD + _CLR.B_BLACK_B + attr_name
        if is_id:
            attr_name = _CLR.FAINT + attr_name
        if values_only == 2 and (is_prop or is_const or is_id):
            continue

        categories[cat].attr_list.append((attr_name , attr_type, val))

    # remove builtin if preset
    if ignore_builtin and 'BUILTIN' in categories:
        categories.pop('BUILTIN')

    # then when we have the type_max_width we can build the lines
    for cat, category in categories.items():
        COLOR = colors_category[cat] if cat in colors_category else _CLR.RESET
        lines = []
        value_max_width = 0

        # print "cat", cat, "width:", category.type_max_width

        for attr_name, attr_type, value in category.attr_list:
            # if truncate and value:
            #     value = ('{}'.format(value))[:truncate]
            if isinstance(value, str):
                value = uni(value)

            value = (': {}'.format(value) if value else '')
            # lines.append("{col1}{type:=>{width}}{col2} {name}{rst}{value}".format(col1=BLACK_B, type=attr_type, col2=COLOR, name=attr_name, rst=RESET, value=value, width=category.type_max_width))
            lines.append("{col1}{type:>{width}}{col2} {name}{rst}{value}".format(col1=_CLR.B_BLACK, type=attr_type, col2=COLOR, name=attr_name, rst=_CLR.RESET, value=value, width=category.type_max_width))
            value_length = lenesc("{name}{value}".format(name=attr_name,  value=value)) + 1
            if value_max_width < value_length:
                value_max_width = value_length

        categories[cat].lines = lines
        categories[cat].value_max_width = value_max_width


    groups = []

    for grouping in COLUMN_GROUPS:
        group = Group()
        for category in grouping:
            if category in categories:
                group.categories.append(categories.pop(category))
        groups.append(group)

    # put all the rest into last group
    group = Group()
    for category in list(categories.keys()):
        group.categories.append(categories.pop(category))
    groups.append(group)

    # calculate group widths
    for group in groups:
        for cat in group.categories:
            group.update_width((cat.type_max_width, cat.value_max_width))

    # try to break out groups as columns if there is enough width
    # top group goes right

    # Determine if columns can be printed in parallel
    # calculate width of current + rest

    terminal_width, terminal_height = get_terminal_size()
    width_used = 0
    output_column_widths = []

    columns = []
    current_column = []
    current_column_height = 0
    current_column_width = 0
    tallest_column_height = 0

    DEBUG = False

    if DEBUG:
        print('terminal: {} x {}'.format(terminal_width, terminal_height))

    # brute force layout to min height
    layouts_fit_width = [layout for layout in get_subqueus_req(groups) if _calc_layout_width(layout) <= terminal_width]
    if layouts_fit_width:
        best_layout = min(layouts_fit_width, key=lambda x: _calc_layout_height(x))
    else:
        best_layout = [groups]
    # print 'best: {}x{}'.format(_calc_layout_width(best_layout), _calc_layout_height(best_layout))

    columns = best_layout
    output_column_widths = [(max([g.width[0] for g in layoutgroup]) + max([g.width[1] for g in layoutgroup])) for layoutgroup in best_layout]

    # render lines for each column
    # add padding according to group width & category type width

    output_columns = []

    for column in columns:
        output_lines = []

        column_type_max_width = sum([max([g.width[0] for g in column])])

        for group in column:
            for cat in group.categories:
                # print '?', cat.__unicode__(), cat.type_max_width, column_type_max_width - cat.type_max_width, column_type_max_width
                # pad = ''.join(['_' for _ in range(column_type_max_width - cat.type_max_width)])
                pad = ''.join([' ' for _ in range(column_type_max_width - cat.type_max_width)])
                for line in cat.lines:
                    output_lines.append('{pad}{line}'.format(pad=pad, line=line))
        output_columns.append(output_lines)

    # PAD = ''.join('+' for _ in xrange(padding))
    PAD = ''.join(' ' for _ in range(padding))

    if DEBUG: #DEBUG
        print("output columns {}: {} (from right to left)".format(len(output_columns), output_column_widths))
        from .utils import ruler
        _padd = 0
        for cw in reversed(output_column_widths):
            print(ruler(cw, _padd, start_from_zero=False))
            _padd += cw

    STREAM = stream if stream is not None else sys.stdout

    STREAM_write = (lambda x: STREAM.write(x)) if not asc else (lambda x: STREAM.write(x.encode('ascii', 'replace').decode()))

    # print output columns
    for line in zip_longest(*reversed(output_columns), fillvalue=''):
        if padding:
            STREAM.write(PAD)
        for column, width in zip(line, reversed(output_column_widths)):
            # count number of escapecharacters and add it to width
            if not color:
                ansi = ansilen(column)
                # STREAM.write(strip_ansi('{column:<{column_width}}'.format(column=column, column_width=min(width, terminal_width) + ansi)))
                STREAM_write(strip_ansi('{column:<{column_width}}'.format(column=column, column_width=min(width, terminal_width) + ansi)))
            else:
                ansi = ansilen(column)
                # STREAM.write('{column:·<{column_width}.{column_width}}'.format(column=column, column_width=min(width, terminal_width) + ansi))
                # STREAM.write('{column:<{column_width}.{column_width}}'.format(column=column, column_width=min(width, terminal_width) + ansi))
                # don't truncate for values_only
                # STREAM.write('{column:·<{column_width}}'.format(column=column, column_width=min(width, terminal_width) + ansi))
                STREAM_write('{column:<{column_width}}'.format(column=column, column_width=min(width, terminal_width) + ansi))
        STREAM.write('\n')


def _calc_layout_width(layout):
    '''
        layout = [  [1, 2], [3], [4, 5]  ]
        width = sum( max(group.width[0]) + max(group.width[1]) )
    '''
    # print
    # print layout
    # print 'widths:', [g.width for lg in layout for g in lg]
    # print 'col dimensions:', [(
    #     max([g.width[0] for g in layoutgroup]),
    #     max([g.width[1] for g in layoutgroup]),
    #     max([g.width[0] for g in layoutgroup]) + max([g.width[1] for g in layoutgroup]),
    #     # max([max([g.width[0] for g in layoutgroup]) + max([g.width[1] for g in layoutgroup]) for layoutgroup in layout]),
    # ) for layoutgroup in layout]
    # print ' =>', sum([(max([g.width[0] for g in layoutgroup]) + max([g.width[1] for g in layoutgroup])) for layoutgroup in layout])

    # return max([max([g.width[0] for g in layoutgroup]) + max([g.width[1] for g in layoutgroup]) for layoutgroup in layout])
    return sum([(max([g.width[0] for g in layoutgroup]) + max([g.width[1] for g in layoutgroup]) + 1) for layoutgroup in layout])

def _calc_layout_height(layout):
    '''
        layout = [  [1, 2], [3], [4, 5]  ]
        height = max(group.height) <- sum(g.get_height())
    '''
    # print
    # print layout
    # print 'heights:', [[g.get_height() for g in layoutgroup] for layoutgroup in layout]
    # print ' sums:', [sum([g.get_height() for g in layoutgroup]) for layoutgroup in layout]
    # print ' tallest:', max([sum([g.get_height() for g in layoutgroup]) for layoutgroup in layout])
    return max([sum([g.get_height() for g in layoutgroup]) for layoutgroup in layout])

# from .utils import ruler


from .utils import uni, get_subqueus_req, parse_parens_notation
from .unihl import symbolize
