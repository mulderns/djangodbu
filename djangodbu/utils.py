#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from shell import RED_B, RESET, GREEN_B, BLUE_B, BLACK_B, YELLOW_B

def get_types(thing):
    try:
        import types
        _all_types = types.__all__

        thing_type = type(thing)
        return [t for t in _all_types if thing_type is getattr(types, t)]
    except:
        pass

def dse(*args, **kwargs):
    import ipdb
    try:
        ds(*args, **kwargs)
    except Exception as e:
        ipdb.post_mortem()

def ds(dictlike, searchstring, case_insensitive=True):
    if isinstance(dictlike, list):
        _list_search(dictlike, searchstring, case_insensitive=case_insensitive)
    elif isinstance(dictlike, dict):
        _dict_search(dictlike, searchstring, case_insensitive=case_insensitive)

def _dict_search(somedict, string, case_insensitive=True, path='', done=None):
    dictid = id(somedict)

    if done is None:
        done = set([dictid])
    elif not dictid in done:
        done.add(dictid)

    if isinstance(somedict, list):
        _list_search(somedict, string, done=done)
        return

    for key, value in somedict.iteritems():
        if (
            case_insensitive and (key.lower().find(string.lower()) != -1) or
            not case_insensitive and (key.find(string) != -1)
        ):
            # print path, 'KEY:', key
            print "{path} {col2}{key}{col0}:{rst} {value}".format(
                col0=BLACK_B,
                # col1=YELLOW_B,
                col2=RED_B,
                rst=RESET,
                key=key,
                value=repr(value),
                path=path + BLACK_B + " >" + RESET if path else ''
            )
            # print YELLOW_B + path, RED_B + 'KEY:' + RESET, repr(value)

        if isinstance(value, str) or isinstance(value, unicode):
            if (
                case_insensitive and (value.lower().find(string.lower()) != -1) or
                not case_insensitive and (value.find(string) != -1)
            ):
                print "{path} {col2}{key} {col0}:{rst} {value}".format(
                    col0=BLACK_B,
                    col1=YELLOW_B,
                    col2=RED_B,
                    rst=RESET,
                    key=key,
                    value=repr(value),
                    path=path + BLACK_B + " >" + RESET if path else ''
                )
                # print BLACK_B + path, BLUE_B + 'VALUE:' + RESET, repr(value)

        elif isinstance(value, dict):
            valueid = id(value)
            if valueid in done:
                continue
            # print '+', valueid
            done.add(valueid)
            new_path = "{path} {col0}> {col2}{key}{rst}".format(col2=RED_B, col0=BLACK_B, rst=RESET, path=path, key=key) if path else RED_B + key + RESET
            _dict_search(value, string, case_insensitive=case_insensitive, path=new_path, done=done)
        elif isinstance(value, list):
            valueid = id(value)
            if valueid in done:
                continue
            # print '-', valueid
            done.add(valueid)
            new_path = "{path} {col0}> {col2}{key}{rst}".format(col2=RED_B, col0=BLACK_B, rst=RESET, path=path, key=key) if path else RED_B + key + RESET
            _list_search(value, string, case_insensitive=case_insensitive, path=new_path, done=done)




def _list_search(somelist, string, case_insensitive=True, path='', done=None):
    listid = id(somelist)

    if done is None:
        done = set([listid])
    elif not listid in done:
        done.add(listid)

    if isinstance(somelist, dict):
        _dict_search(somelist, string, case_insensitive=case_insensitive, done=done)
        return

    for i, value in enumerate(somelist):
        if isinstance(value, str) or isinstance(value, unicode):
            if (
                case_insensitive and (value.lower().find(string.lower()) != -1) or
                not case_insensitive and (value.find(string) != -1)
            ):
                print "{path} {col2}{key}{rst} {col0}:{rst} {value}".format(
                    col0=BLACK_B,
                    col1=YELLOW_B,
                    col2=BLUE_B,
                    rst=RESET,
                    key=i,
                    value=repr(value),
                    path=path + BLACK_B + ' >' + RESET if path else ''
                )
                # print BLACK_B + path, i, BLUE_B + 'VALUE:' + RESET, value
        elif isinstance(value, dict):
            valueid = id(value)
            if valueid in done:
                continue
            # print '+', valueid
            done.add(valueid)
            new_path = "{path} {col0}> {col2}{key}{rst}".format(col2=BLUE_B, col0=BLACK_B, rst=RESET, path=path, key=i) if path else BLUE_B + i + RESET
            _dict_search(value, string, case_insensitive=case_insensitive, path=new_path, done=done)
        elif isinstance(value, list):
            valueid = id(value)
            if valueid in done:
                continue
            # print '-', valueid
            done.add(valueid)
            new_path = "{path} {col0}> {col2}{key}{rst}".format(col2=BLUE_B, col0=BLACK_B, rst=RESET, path=path, key=i) if path else BLUE_B + i + RESET
            _list_search(value, string, case_insensitive=case_insensitive, path=new_path, done=done)


def ruler(length=71, pad=0, start_from_zero=True):
    rulermrks = "|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|"
    rulerdata = "0        10        20        30        40        50        60        70        80        90        100       110       120       130       140       150"

    if start_from_zero:
        return "{}\n{}".format(
            ''.join([' ' for _ in xrange(pad)]) + rulermrks[:length],
            ''.join([' ' for _ in xrange(pad)]) + rulerdata[:length]
        )

    return "{}\n{}".format(
        ''.join([' ' for _ in xrange(pad)]) + rulermrks[1:(length + 1)],
        ''.join([' ' for _ in xrange(pad)]) + rulerdata[1:(length + 1)]
    )

_encodings = [
    'utf-8',
    'latin1',
    'ascii',
    'ISO-8859-1',
    'ISO-8859-15',
]


def ascfix(input_text):
    if isinstance(input_text, str):
        print input_text
        # print type(input_text),
        print 'str',
        print "-decode-> unicode",
        try:
            import chardet
            res = chardet.detect(input_text)
            print "({en} at ~{con})".format(en=res.get('encoding'), con=res.get('confidence'))
        except:
            print

        for enc in _encodings:
            print "{}: ".format(enc)

            try:
                data = input_text.decode(enc, 'replace')
                # print "-> OK"

                for enc2 in _encodings:
                    print "  -> {}:".format(enc2),
                    try:
                        data2 = str(data.encode(enc2, 'replace'))
                        print data2
                    except Exception as e:
                        print 'Error'
                print

            except Exception as e:
                print "-> Error"

    elif isinstance(input_text, unicode):
        print input_text
        # print type(input_text),
        print 'unicode'
        print "-encode-> str"

        for enc in _encodings:
            print "{}: ".format(enc)
            print "  e: ",
            try:
                data = str(input_text.encode(enc, 'replace'))
                print data, input_text.encode(enc, 'replace')
            except Exception as e:
                print "Error", e,
                try:
                    data = input_text.encode(enc, 'replace')
                    print "-> OK"
                except Exception as e:
                    print "-> Error"

    else:
        print "-> not string"
        return
import logging
log = logging.getLogger(__name__)
import chardet
def uni(thing):
    if thing is None:
        return None

    if isinstance(thing, unicode):
        # log.debug(u'unicode: {}'.format(thing))
        # log.debug('is unicode')
        return thing

    if isinstance(thing, str):
        # log.debug('str {}'.format(thing))
        # log.debug('is str')
        try:
            return thing.decode('utf-8')
        except UnicodeDecodeError as e:
            # log.debug(' not utf-8')
            result = chardet.detect(thing)
            charenc = result['encoding']
            return thing.decode(charenc, 'replace')

    if isinstance(thing, (int, float, long)):
        # log.debug(u'number: {}'.format(thing))
        # log.debug('is number')
        return '{}'.format(thing)

    if hasattr(thing, '__unicode__'):
        try:
            # log.debug('__unicode__ {} -> {}'.format(repr(thing), thing.__unicode__()))
            # log.debug('has __unicode__()')
            return thing.__unicode__()
        except:
            # log.debug('  could not __unicode__()')
            pass
    if hasattr(thing, '__str__') and not isinstance(thing, type):
        # log.debug('__str__() {} -> {}'.format(repr(thing), uni(thing.__str__())))

        return uni(thing.__str__())

    return repr(thing)

def get_subqueus_req(elements, first=True):
    if not elements:
        # print '-'
        yield None
    elif len(elements) == 1:
        # print ' .', [elements]
        yield [elements]
    else:
        for w in range(1, len(elements)):
            for rest in get_subqueus_req(elements[w:], first=False):
                # if first:
                #     print '=> ', [elements[:w]], '+', rest
                # else:
                #     print '  <-', [elements[:w]], '+', rest
                yield [elements[:w]] + rest if rest else [elements]
        # yield [elements] if first else [elements]
        # if first:
        #     print '=> ', elements
        # else:
        #     print ' <=', [elements]
        yield [elements]



class _dict2props(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

cols = _dict2props(**{
    'black'         : (30, 40),
    'red'           : (31, 41),
    'green'         : (32, 42),
    'yellow'        : (33, 43),
    'blue'          : (34, 44),
    'magenta'       : (35, 45),
    'cyan'          : (36, 46),
    'white'         : (37, 47),
    'bright_black'  : (90, 100),
    'bright_red'    : (91, 101),
    'bright_green'  : (92, 102),
    'bright_yellow' : (93, 103),
    'bright_blue'   : (94, 104),
    'bright_magenta': (95, 105),
    'bright_cyan'   : (96, 106),
    'bright_white'  : (97, 107 ),
})


# 0	Reset / Normal
# 1	Bold or increased intensity
# 2	Faint (decreased intensity)
# 3	Italic
# 4	Underline
# 5	Slow Blink
# 6	Rapid Blink
# 7	reverse video
# 8	Conceal
# 9	Crossed-out
# 10	Primary(default) font
# 11–19	Alternative font


def shc(fg=None, bg=None, rev=None, under=None, bold=None, faint=None, italic=None, blinks=None, blinkr=None, con=None, cross=None):
    '''
Colors:
- [bright_]black
- [bright_]red
- [bright_]green
- [bright_]yellow
- [bright_]blue
- [bright_]magenta
- [bright_]cyan
- [bright_]white
    '''
    esc = '\x1b['
    sep = ';'
    end = 'm'
    command = []
    if bold is not None and bold: command.append('1')
    if bold is not None and not bold: command.append('22')
    if faint is not None and faint: command.append('2')
    if faint is not None and not faint: command.append('22')
    if italic is not None and italic: command.append('3')
    if italic is not None and not italic: command.append('23')
    if under is not None and under: command.append('4')
    if under is not None and not under: command.append('24')
    # if blinks: command.append('5')
    # if blinkr: command.append('6')
    if rev is not None and rev: command.append('7')
    if rev is not None and not rev: command.append('27')
    # if con: command.append('8')
    # if cross: command.append('9')

    if fg:
        command.append(str(getattr(cols, fg)[0]))

    if bg:
        command.append(str(getattr(cols, bg)[1]))

    if not command:
        command.append('0')

    return esc + sep.join(command) + end

def print_colors():
    colornames = [
        'black',
        'red',
        'green',
        'yellow',
        'blue',
        'magenta',
        'cyan',
        'white',
    ]

    for c in colornames:
        print '{name:9}{norm}{name:9}{rst}{bold}{name:9}{rst}{bright}{name:9}{rst}{faint}{name:9}{rst}{rev}{name:9}{rst}'.format(
            name=c,
            rst=shc(),
            norm=shc(c),
            bold=shc(c, bold=True),
            bright=shc('bright_'+c),
            faint=shc(c, faint=True),
            rev=shc(c, rev=True),
        )

