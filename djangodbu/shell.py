# -*- coding: utf-8 -*-
import sys
import inspect
import pprint
import re
import types
from collections import defaultdict
from itertools import chain, izip_longest

from django.db.models import Model
from django.db.models.query import QuerySet
from django.db.models.sql.query import Query, RawQuery


from terminalsize import get_terminal_size

from sql import print_query

# from utils import ruler

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



class COLORS(object):
    def __init__(self):
        self.RED = '\033[0;31m'
        self.GREEN = '\033[0;32m'
        self.BLUE = '\033[0;34m'
        self.CYAN = '\033[0;36m'
        self.MAGENTA = '\033[0;35m'
        self.YELLOW = '\033[0;33m'
        self.WHITE = '\033[0;37m'
        self.BLACK = '\033[0;30m'
        self.RED_B = '\033[1;31m'
        self.GREEN_B = '\033[1;32m'
        self.BLUE_B = '\033[1;34m'
        self.CYAN_B = '\033[1;36m'
        self.MAGENTA_B = '\033[1;35m'
        self.YELLOW_B = '\033[1;33m'
        self.WHITE_B = '\033[1;37m'
        self.BLACK_B = '\033[1;30m'
        self.RESET = '\033[0m'

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

COLORSx = {
    'RED':  '\033[0;31m',
    'GREEN':  '\033[0;32m',
    'BLUE':  '\033[0;34m',
    'CYAN':  '\033[0;36m',
    'MAGENTA':  '\033[0;35m',
    'YELLOW':  '\033[0;33m',
    'WHITE':  '\033[0;37m',
    'BLACK':  '\033[0;30m',
    'RED_B':  '\033[1;31m',
    'GREEN_B':  '\033[1;32m',
    'BLUE_B':  '\033[1;34m',
    'CYAN_B':  '\033[1;36m',
    'MAGENTA_B':  '\033[1;35m',
    'YELLOW_B':  '\033[1;33m',
    'WHITE_B':  '\033[1;37m',
    'BLACK_B':  '\033[1;30m',
    'RESET': '\033[0m',
}


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
    'OTHER': RESET,
    'NONE': BLACK_B,
}

NOCOLOR = ''

NOCOLORS_CATEGORY = {
    'BOOL': NOCOLOR,
    'NUMBER': NOCOLOR,
    'STRING': NOCOLOR,
    'LIST': NOCOLOR,
    'FUNCTION': NOCOLOR,
    'RELATED': NOCOLOR,
    'CLASS': NOCOLOR,
    'DATE': NOCOLOR,
    'OTHER': NOCOLOR,
    'NONE': NOCOLOR,
}


COLUMN_GROUPS = [
    ['FUNCTION', 'BUILTIN'],
    ['RELATED'],
    ['BOOL', 'STRING', 'NUMBER', 'DATE', 'LIST'],
]

TYPE_SUBSTITUTIONS = [
    ('django.db.models.fields.related.RelatedManager', 'RelatedManager'),
    ('django.db.models.fields.related.ManyRelatedManager', 'ManyRelatedManager'),
]

def type_to_category_value(thing):
    if inspect.ismodule(thing): return ('CLASS', thing.__name__)
    if isinstance(thing, types.TypeType): return ('OTHER', None)
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
    if isinstance(thing, types.NoneType): return ('NONE', None)

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
    if isinstance(thing, QuerySet): return ('RELATED', str(thing.count()))
    if str(type(thing)).find('datetime') != -1:
        return ('DATE', thing.__str__())
    if hasattr(thing, '__class__'): return ('CLASS', thing.name if hasattr(thing,'name') else None)
    return ('OTHER', repr(thing))


def dorm(obj, ignore_builtin=True, values_only=False, minimal=False, padding=0, data=None, enable_callable=False, values=None, v=None, no_color=False):
    # print lists and such with pprint
    if type(obj) in (types.ListType, types.DictType, types.TupleType):
        pprint.pprint(obj, indent=2)
        return

    if isinstance(obj, defaultdict):
        pprint.pprint(dict(obj), indent=2)
        return

    # print sql
    if isinstance(obj, Query) or isinstance(obj, RawQuery):
        print_query(obj)
        return

    # TODO: print members of a module
    #if isinstance(thing, types.ModuleType):
    #    pass

    # iterate querysets
    if isinstance(obj, QuerySet):
        if v is not None and values is None:
            values = [val.strip() for val in v.split(',')]

        if values is not None:
            print obj.model
            lines = []
            col_max = ['0'] * len(values)
            for row in obj.values('pk', *values):
                item_id, datas = _print_minimal_values2(row, values)
                col_max = [max(x, key=len) for x in zip(col_max, datas)]
                lines.append(('{:6}'.format(item_id), datas))

            #print ''.join( v, w in zip(values, col_max) )
            print '    id: ' + u'  '.join([u"{:{width}.{width}}".format(squish_to_size(l, len(w)) if l is not None else '', width=len(w)) for l, w in zip(values, col_max)])

            print ''.join(['-' for _ in xrange(get_terminal_size()[0])])


            for item_id, datas in lines:
                print u"{col1}{id}{col2}: {reset}{values}".format(col1=WHITE, id=item_id, col2=BLACK_B, reset=RESET, values=u'  '.join(
                    [u"{:{width}}".format(l if l is not None else '', width=len(w)) for l, w in zip(datas, col_max)]
                ))
        else:
            for item in obj:
                _print_minimal(item, data=data, enable_callable=enable_callable)
        print u"= {}{}{}".format(RED, obj.count(), RESET)
        return

    # else print orm debug
    _print_orm(obj, ignore_builtin=ignore_builtin, values_only=values_only, padding=padding, no_color=no_color)


def _print_minimal_values(row, selected_values):
    item_id = row.pop('pk')
    values2 = []

    for key in selected_values:
        data = row.get(key)
        if isinstance(data, str):
            values2.append(unicode(data, 'utf-8', 'replace'))
        else:
            values2.append(unicode(data))

    #try:
    print u"{}{}{}: {}{}".format(WHITE, item_id, BLACK_B, RESET, ', '.join(values2))
    #except Exception as e:
    #    values2 = [unicode(value.decode('utf-8', 'replace')) for value in values2]
    #    print u"{}{}{}: {}{}".format(WHITE, item_id, BLACK_B, RESET, ', '.join(values2))

def _print_minimal_values2(row, selected_values):
    item_id = row.pop('pk')
    values2 = []

    for key in selected_values:
        data = row.get(key)
        if isinstance(data, str):
            values2.append(unicode(data.decode('utf-8', 'replace'), 'utf-8', 'replace') + u'X')
        elif isinstance(data, unicode):
            #values2.append(data.encode('utf-8', 'replace') + u'Z')
            #values2.append(data.encode('utf-8', 'replace').decode('utf-8','replace'))
            #print data
            values2.append(data)
        else:
            values2.append(unicode(data))

    return (item_id, values2)


def _print_minimal_values_pprint(row, selected_values):
    item_id = row.pop('pk')
    print u"{}{}{}: {}{}".format(WHITE, item_id, BLACK_B, RESET, pprint.pformat(row))

def _print_minimal(obj, data=None, enable_callable=False):
    id = obj.id if hasattr(obj, 'id') else ''
    value = id

    # TODO: if values -> .values()
    # TODO: lambda as data
    if data and hasattr(obj, data):
        attr = getattr(obj, data)
        if not callable(attr):
            value = attr
        else:
            if enable_callable:
                value = attr()
            else:
                value = u'callable: {} '.format(type(attr))

    elif data is None and hasattr(obj, 'name'):
        attr = getattr(obj, 'name')
        if not callable(attr):
            value = attr
        else:
            if enable_callable:
                value = attr()
            else:
                value = u'callable: {} '.format(type(attr))
    elif data is None and hasattr(obj, '__str__'):
        value = unicode(obj.__str__().decode('utf-8', 'replace'))

    try:
        print u"{}{}{}: {}{}".format(WHITE, id, BLACK_B, RESET, value)
    except Exception as e:
        value = unicode(value.decode('utf-8', 'replace'))
        print u"{}{}{}: {}{}".format(WHITE, id, BLACK_B, RESET, value)


def dorme(*args, **kwargs):
    import ipdb
    try:
        dorm(*args, **kwargs)
    except Exception as e:
        print e
        ipdb.post_mortem()


ansisequence = re.compile(r'\x1B\[[^A-Za-z]*[A-Za-z]')

def strip_ansi(line):
    return ansisequence.sub('', line)

def lenesc(line):
    return len(ansisequence.sub('', line))

def ansilen(line):
    return len(line) - lenesc(line)

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


def dormnc(*args, **kwargs):
    dorm(*args, no_color=True, **kwargs)


class Category(object):
    def __init__(self, category='', attr_list=None, type_max_width=0, lines=None):
        self.category = category
        self.attr_list = attr_list if attr_list else []
        self.type_max_width = type_max_width
        self.lines = lines if lines else []

    def update_max_width(self, width):
        if width > self.type_max_width:
            self.type_max_width = width


class Group(object):
    def __init__(self, categories=None, width=0):
        self.categories = categories if categories else []
        self.width = width

    def update_width(self, width):
        if width > self.width:
            self.width = width

    def get_height(self):
        height = sum([len(c.lines) for c in self.categories])
        return height


def calculate_width(groups):
    #type_max_width = max([c.type_max_width for c in [g.categories for g in groups]])
    type_max_width = 0
    for g in groups:
        for c in g.categories:
            if c.type_max_width > type_max_width:
                type_max_width = c.type_max_width

    # g_w + t_mw - g_c_mw
    width = 0
    for group in groups:
        _max = max([c.type_max_width for c in group.categories]) if group.categories else 0
        result = group.width + (type_max_width - _max)

        #result = group.width + (type_max_width - max([c.type_max_width for c in group.categories]))
        width = result if result > width else width
    return width

def _print_orm(obj, ignore_builtin=True, values_only=False, padding=0, no_color=False):
    colors = NOCOLORS() if no_color else COLORS()
    colors_category = NOCOLORS_CATEGORY if no_color else COLORS_CATEGORY

    # print object identifier
    print u"{} : {}".format(obj, type(obj))

    categories = defaultdict(Category)

    # sort object data into categories with names and values
    for attr_name in dir(obj):
        if (ignore_builtin and attr_name.startswith('_')) or attr_name == 'objects':
            continue

        attr = None
        try:
            attr = getattr(obj, attr_name)
        except Exception as e:
            print "exception:", e
            pass

        cat, val = type_to_category_value(attr)

        # shorten some common types
        match = re.search(RE_STRIP_TYPE, str(type(attr)))
        attr_type = match.group(1) if match else str(type(obj))

        for type_string, substitution in TYPE_SUBSTITUTIONS:
            if attr_type.find(type_string) != -1:
                attr_type = substitution
                break
        else:
            if attr_type.count('.') > 1:
                attr_type = '.'.join(chain(map(lambda x: x[:2], attr_type.split('.')[:-1]), (attr_type.split('.')[-1],)))

        if not categories.has_key(cat):
            categories[cat].category = cat

        categories[cat].update_max_width(len(attr_type))
        categories[cat].attr_list.append((attr_name, attr_type, val))

    # then when we have the type_max_width we can build the lines

    for cat, category in categories.iteritems():
        COLOR = colors_category[cat] if colors_category.has_key(cat) else colors.RESET
        lines = []

        for attr_name, attr_type, value in category.attr_list:
            lines.append(u"{col1}{type:>{width}}{col2} {name}{rst}{value}".format(col1=BLACK_B, type=attr_type, col2=COLOR, name=attr_name, rst=RESET, value=(u': {}'.format(value) if value else ''), width=category.type_max_width))

        categories[cat].lines = lines


    groups = []

    for grouping in COLUMN_GROUPS:
        group = Group()
        for category in grouping:
            if categories.has_key(category):
                group.categories.append(categories.pop(category))
        groups.append(group)

    # put all the rest into last group
    group = Group()
    for category in categories.keys():
        group.categories.append(categories.pop(category))
    groups.append(group)

    # calculate group widths
    for group in groups:
        for cat in group.categories:
            for line in cat.lines:
                line_length = lenesc(line)
                group.update_width(line_length)

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

    for i, group in enumerate(groups):
        #if (terminal_width - width_used) > (1 + current_column_width + group.width + calculate_width(groups[i+1:])):
        if (terminal_width - width_used) > (1 + current_column_width + calculate_width(groups[i:])):
            # we have space for new column

            if current_column_height + group.get_height() <= min(tallest_column_height, terminal_height):
                # ump this column to current column
                current_column_height += group.get_height()
                current_column.append(group)
                current_column_width = calculate_width(current_column)

            else:
                # move current_column to output
                columns.append(current_column)
                width_used += current_column_width
                output_column_widths.append(current_column_width)

                # create new_column from this group
                current_column = [group]
                current_column_width = calculate_width(current_column)
                current_column_height = group.get_height()
                if tallest_column_height < current_column_height:
                    tallest_column_height = current_column_height

        else:
            # we don't have space for new column
            # ump this column to current column
            current_column_height += group.get_height()
            current_column.append(group)
            current_column_width = calculate_width(current_column)

    # place the last open column to columns
    columns.append(current_column)
    output_column_widths.append(current_column_width)

    # render lines for each column
    # add padding according to group width & category type width

    output_columns = []

    for column in columns:
        output_lines = []
        #column_type_max_width = max([c.type_max_width for c in [g.categories for g in column]])

        column_type_max_width = 0
        for g in column:
            for c in g.categories:
                if c.type_max_width > column_type_max_width:
                    column_type_max_width = c.type_max_width

        for group in column:
            for cat in group.categories:
                pad = u''.join([u' ' for _ in range(column_type_max_width - cat.type_max_width)])
                for line in cat.lines:
                    output_lines.append(u'{pad}{line}'.format(pad=pad, line=line))
        output_columns.append(output_lines)


    # print output columns
    for line in izip_longest(*reversed(output_columns), fillvalue=''):
        for column, width in zip(line, reversed(output_column_widths)):
            # count number of escapecharacters and add it to width
            if no_color:
                ansi = ansilen(column)
                sys.stdout.write(strip_ansi(u'{column:{column_width}}'.format(column=column, column_width=width + ansi+1)))
            else:
                ansi = ansilen(column)
                sys.stdout.write(u'{column:{column_width}}'.format(column=column, column_width=width + ansi+1))
        sys.stdout.write('\n')

