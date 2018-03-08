# -*- coding: utf-8 -*-
def to_string(obj, raise_err=False):
    if obj is None:
        return ""
    if isinstance(obj, unicode):
        return obj.encode("utf-8")
    else:
        if raise_err:
            return str(obj)
        else:
            try:
                return str(obj)
            except:
                return ""


def to_unicode(obj):
    if isinstance(obj, unicode):
        return obj
    else:
        try:
            return str(obj).decode("utf-8")
        except:
            return unicode("")