# -*- coding: utf-8 -*-
''' For debugging SQL queries, (SOME ASSEMBLY REQUIRED!)

    You need to:
    - add a line to django.db.backends.utils.py, see details in stack_position
    - configure excluded paths for stack traces to get cleaner output


'''

import logging
import re
import os
import traceback
from math import log as ln
from collections import defaultdict

import sqlparse
from sqlparse import keywords

# SQL keywords for colorization
KEYS = keywords.KEYWORDS.keys()
KEYS.extend(keywords.KEYWORDS_COMMON.keys())

log = logging.getLogger(__name__)


_MINIBARS = [
    '\033[1;32m|',
    '\033[0;32m|',
    '\033[0;33m|',
    '\033[1;33m|',
    '\033[1;31m|',
    '\033[0;31m|',
]

_RESET = '\033[0m'

def _minilogbars(time):
    bars = max(0, min(5, int(round(ln(time*100)))) if time != 0 else 0)
    pad = ' ' * max(0, 5 - bars)
    return '{bars}{reset}{pad}'.format(bars=''.join(_MINIBARS[:bars]), reset=_RESET, pad=pad)



#colorize_sql_regexp = re.compile(r"([^.])`([^`]*)`\.", re.IGNORECASE)  # `(table)`.`...`
#colorize_sql_regexp_2 = re.compile(r"\.`([^`]*)`", re.IGNORECASE) # `table.`(field)`
colorize_sql_regexp_1_2 = re.compile(r"`([^`]*)`\.`([^`]*)`", re.IGNORECASE)  # `(table)`.`(field)`
colorize_sql_regexp_3 = re.compile(r" `([^`]*)`[^.]", re.IGNORECASE) # `(table)`
colorize_sql_regexp_4 = re.compile(r'('+'[^A-Z]|'.join(KEYS)+r')')  # KEYWORDS
colorize_sql_regexp_5 = re.compile(r'( [=<>] )')  # comparators

def colorize_sql(sql):
    #sql = colorize_sql_regexp.sub(r'\1\033[1;30m\2\033[0m.', sql)
    #sql = colorize_sql_regexp_2.sub(r'.\033[0;34m\1\033[0m', sql)
    sql = colorize_sql_regexp_1_2.sub(r'\033[1;30m\1\033[0m.\033[0;34m\2\033[0m', sql)
    sql = colorize_sql_regexp_3.sub(r' \033[0;35m\1\033[0m ', sql)
    sql = colorize_sql_regexp_4.sub(r'\033[0;33m\1\033[0m', sql)
    sql = colorize_sql_regexp_5.sub(r'\033[0;31m\1\033[0m', sql)
    return sql

def format_sql(sql):
    return sqlparse.format(sql, reindent=True)

def print_query(query):
    sqlstring = unicode(query.__str__())
    print colorize_sql(format_sql(sqlstring))

def sqlprint(data, filtering=True):
    '''
    "Print SQL queries": {
		"prefix": "dbusql",
		"body": [
			"from django.db import connection; # TODO: remove this debug\nfrom dbu import sql; sql.sqlprint(connection.queries) # TODO: remove this debug"
		],
		"description": "list sql queries"
	}

    also

	"Reset SQL queries": {
		"prefix": "dbusqlr",
		"body": [
			"from django.db import reset_queries; reset_queries()  # TODO: remove this debug"
		],
		"description": "reset sql queries list"
	}

    '''
    for row in data:
        #row['sql'] = colorize_sql(row['sql'])
        if filtering and float(row['time']) < 0.0001:
            log.info("{} :".format(row['time']))
            continue

        location = None
        if row.has_key('trace'):
            location = _get_location(row['trace'])

        sql = format_sql(row['sql'])
        sql = colorize_sql(sql)
        log.info("{} :{}\n{}\n".format(row['time'], location, sql))


new_line_replace = re.compile(r'(\n)')
def _indent_newlines(data, indentation=4):
    sub_space = '\n' + (' ' * indentation)
    return new_line_replace.sub(sub_space, data)


trace_exclude_paths = re.compile(r'/System|site-packages|wsgi\.py')
def __format_traceback_debug(tb):
    for frame in tb:
        if trace_exclude_paths.search(frame[0]):
            continue
        simple_file = os.path.basename(frame[0])
        #print "<{f}:{l}:{m}> {t}".format(f=simple_file, l=frame[1], m=frame[2], t=frame[3])
        print "{f}:{m}:{l:<4} > {t} \t ".format(f=frame[0], fs=simple_file, l=frame[1], m=frame[2], t=frame[3])

    print ""

def _format_traceback(tb):
    #return '\n \033[0;35m>\033[0m '.join("\033[0;34m{file}\033[1;30m:\033[0;36m{module}\033[1;30m:\033[0;37m{linenum:<3}\033[0;35m :\033[0m {text}".format(file=os.path.basename(frame[0]), linenum=frame[1], module=frame[2], text=frame[3]) for frame in tb if not trace_exclude_paths.search(frame[0]))
    #return '\n \033[0;35m>\033[0m '.join("\033[0;34m{file}\033[1;30m:\033[0;37m{linenum:<3}\033[1;30m:\033[0;36m{module}\033[0;35m :\033[0m {text}".format(file=os.path.basename(frame[0]), linenum=frame[1], module=frame[2], text=frame[3]) for frame in tb if not trace_exclude_paths.search(frame[0]))
    #return '\n \033[0;35m>\033[0m '.join("\033[0;34m{file}\033[1;30m:\033[0;37m{linenum:<3} \033[0;36m{module}\033[0;35m:\033[0m {text}".format(file=os.path.basename(frame[0]), linenum=frame[1], module=frame[2], text=frame[3]) for frame in tb if not trace_exclude_paths.search(frame[0]))
    return '\n \033[0;35m>\033[0m '.join("\033[0;34m{file}\033[1;30m:\033[0;37m{linenum:<3} \033[0;36m{module}\033[0m {text}".format(file=os.path.basename(frame[0]), linenum=frame[1], module=frame[2], text=frame[3]) for frame in tb if not trace_exclude_paths.search(frame[0]))

def _get_location(tb):
    relevant_frames = [frame for frame in tb if not trace_exclude_paths.search(frame[0])]
    if len(relevant_frames) == 0:
        return ""
    frame = relevant_frames[-1]

    return "\033[0;34m{file}\033[1;30m:\033[0;37m{linenum:<3} \033[0;36m{module}\033[0m {text}".format(file=os.path.basename(frame[0]), linenum=frame[1], module=frame[2], text=frame[3])


def sqlcount(data, filtersmall=False):
    '''
    "Count SQL queries": {
		"prefix": "dbusqlcount",
		"body": [
			"from django.db import connection; # TODO: remove this debug\nfrom dbu import sql; sql.sqlcount(connection.queries) # TODO: remove this debug"
		],
		"description": "count number and total time of sql queries, show originating lines"
	}
    '''
    counts = defaultdict(lambda: {'count':0.0, 'time':0.0, 'location': set()})

    for row in data:
        #m = md5()
        #m.update(row['sql'])
        #key = m.hexdigest()
        key = row['sql']
        counts[key]['count'] += 1.0

        time = float(row['time'])
        if time == 0.001:
            time = 0.0007
        elif time == 0.000:
            time = 0.0004

        counts[key]['time'] += time
        if row.has_key('trace'):
            counts[key]['location'].add(_format_traceback(row['trace']))

    results = [(val['count'], val['time'], val['location']) for key, val in counts.items() if val['time'] > 0.01 or not filtersmall]

    results.sort(key=lambda x: (x[0], x[1]), reverse=True)

    out = ''
    for count, time, location in results:
        if '' in location:
            location.remove('')
        out += "{: 4} / {:05.3f} [{}]: {}\n".format(int(count), time, _minilogbars(time), _indent_newlines('\n'.join(location), 22))
    log.info('counts: \n{}'.format(out))

def stack_position():
    return ' > '.join([f[2] for f in traceback.extract_stack()])



# ADD THIS TO django > db > backends > utils.py > CursorDebugWrapper
# self.db.queries_log.append({
#     'sql': sql,
#     'time': "%.3f" % duration,
#     'trace': stack_position(),  # < THIS
# })


# STACK
def format_stack():
    # file, ln, function, text

    for frame in traceback.extract_stack():
        simple_file = os.path.basename(frame[0])
        print u"{m:>20.20}:{l:<4} > {t}".format(f=frame[0], fs=simple_file, l=frame[1], m=frame[2], t=frame[3])
