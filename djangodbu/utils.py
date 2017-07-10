#!/usr/bin/env python
import types

_all_types = types.__all__

def get_types(thing):
    thing_type = type(thing)
    return [t for t in _all_types if thing_type is getattr(types, t)]
