#!/usr/bin/env python

from shell import RED_B, RESET, GREEN_B, BLUE_B, BLACK_B, YELLOW_B

def get_types(thing):
    try:
        import types
        _all_types = types.__all__

        thing_type = type(thing)
        return [t for t in _all_types if thing_type is getattr(types, t)]
    except:
        pass

def dict_search(somedict, string, case_insensitive=True, path='', done=None):
    dictid = id(somedict)

    if done is None:
        done = set([dictid])
    elif not dictid in done:
        done.add(dictid)

    if isinstance(somedict, list):
        list_search(somedict, string, done=done)
        return

    for key, value in somedict.iteritems():
        if (
            case_insensitive and (key.lower().find(string.lower()) != -1) or
            not case_insensitive and (key.find(string) != -1)
        ):
            # print path, 'KEY:', key
            print YELLOW_B + path, RED_B + 'KEY:' + RESET, repr(value)

        if isinstance(value, str) or isinstance(value, unicode):
            if (
                case_insensitive and (value.lower().find(string.lower()) != -1) or
                not case_insensitive and (value.find(string) != -1)
            ):
                print BLACK_B + path, BLUE_B + 'VALUE:' + RESET, repr(value)

        elif isinstance(value, dict):
            valueid = id(value)
            if valueid in done:
                continue
            # print '+', valueid
            done.add(valueid)
            dict_search(value, string, path=path+' > '+key if path else key, done=done)
        elif isinstance(value, list):
            valueid = id(value)
            if valueid in done:
                continue
            # print '-', valueid
            done.add(valueid)
            list_search(value, string, path=path+' > '+key if path else key, done=done)




def list_search(somelist, string, case_insensitive=True, path='', done=None):
    listid = id(somelist)

    if done is None:
        done = set([listid])
    elif not listid in done:
        done.add(listid)

    if isinstance(somelist, dict):
        dict_search(somelist, string, done=done)
        return

    for i, value in enumerate(somelist):
        if isinstance(value, str) or isinstance(value, unicode):
            if (
                case_insensitive and (value.lower().find(string.lower()) != -1) or
                not case_insensitive and (value.find(string) != -1)
            ):
                print BLACK_B + path, i, BLUE_B + 'VALUE:' + RESET, value
        elif isinstance(value, dict):
            valueid = id(value)
            if valueid in done:
                continue
            # print '+', valueid
            done.add(valueid)
            dict_search(value, string, path="{} > {}".format(path, i) if path else i, done=done)
        elif isinstance(value, list):
            valueid = id(value)
            if valueid in done:
                continue
            # print '-', valueid
            done.add(valueid)
            list_search(value, string, path="{} > {} ".format(path, i) if path else i, done=done)


def ruler(length=71, pad=0, start_from_zero=True):
    #        12345678901234567890123456789012345678901234567890123456789012345678901234567890
    #rulermrks = "|._._:_._.|....:....|....:....|....:....|....:....|....:....|....:....|....:....|....:....|....:....|....:....|....:....|....:....|....:....|....:...."
    rulermrks = "|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|._._:_._.|"
    rulerdata = "0        10        20        30        40        50        60        70        80        90        100       110       120       130       140       150"
    #rulerdata = "01234567890....|....2....|....3....|....4....|....5....|....6....|....7....|....8....|....9....|....0....|....1....|....2....|....3....|....4....|....5"

    if start_from_zero:
        return u"{}\n{}".format(
            u''.join([u' ' for _ in xrange(pad)]) + rulermrks[:length - pad],
            u''.join([u' ' for _ in xrange(pad)]) + rulerdata[:length - pad]
        )

    return u"{}\n{}".format(
        u''.join([u' ' for _ in xrange(pad)]) + rulermrks[1:length + 1 - pad],
        u''.join([u' ' for _ in xrange(pad)]) + rulerdata[1:length + 1 - pad]
    )
