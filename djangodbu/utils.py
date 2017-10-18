#!/usr/bin/env python

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
            ''.join([' ' for _ in xrange(pad)]) + rulermrks[:length - pad],
            ''.join([' ' for _ in xrange(pad)]) + rulerdata[:length - pad]
        )

    return "{}\n{}".format(
        ''.join([' ' for _ in xrange(pad)]) + rulermrks[1:length + 1 - pad],
        ''.join([' ' for _ in xrange(pad)]) + rulerdata[1:length + 1 - pad]
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
        return thing

    if isinstance(thing, str):
        # log.debug('str {}'.format(thing))
        try:
            return thing.decode('utf-8')
        except UnicodeDecodeError as e:
            result = chardet.detect(thing)
            charenc = result['encoding']
            return thing.decode(charenc, 'replace')

    if isinstance(thing, (int, float, long)):
        # log.debug(u'number: {}'.format(thing))
        return '{}'.format(thing)

    if hasattr(thing, '__unicode__'):
        try:
            # log.debug('__unicode__ {} -> {}'.format(repr(thing), thing.__unicode__()))
            return thing.__unicode__()
        except:
            pass
    if hasattr(thing, '__str__') and not isinstance(thing, type):
        # log.debug('__str__() {} -> {}'.format(repr(thing), thing.__str__()))
        return thing.__str__()

    return repr(thing)
