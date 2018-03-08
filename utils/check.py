# coding: utf-8

import re



def check_subaccount_name(subaccount_name):
    if not isinstance(subaccount_name, unicode):
        try:
            subaccount_name = subaccount_name.decode("utf-8")
        except:
            return False
    if not (subaccount_name and 1 <= len(subaccount_name) <= 16):
        return False
    for ch in subaccount_name:
        if not (u'\u0041' <= ch <= u'\u005a' or u'\u0061' <= ch <= u'\u007a' or u'\u0030' <= ch <= u'\u0039'):
            # 只允许英文和数字
            return False
    return True


def check_subaccount_alias(alias):
    if not isinstance(alias, unicode):
        try:
            alias = alias.decode("utf-8")
        except:
            return False
    if not (alias and 3 <= len(alias) <= 16):
        return False
    for ch in alias:
        if not (u'\u4e00' <= ch <= u'\u9fff' or u'\u0041' <= ch <= u'\u005a' or u'\u0061' <= ch <= u'\u007a' or u'\u0030' <= ch <= u'\u0039'):
            # or连接的第1个检查汉字，2、3个检查英文，4检查数字
            return False
    return True


def check_email( s):
    if len(s) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", s) != None:
            return True
    return False


def check_ip(ip_range):
    if re.match("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip_range):
        return True
    else:
        return False


def check_mask(mask):
    if re.match('^(254|252|248|240|224|192|128|0)\.0\.0\.0$|^(255\.(254|252|248|240|224|192|128|0)\.0\.0)$|^(255\.255\.(254|252|248|240|224|192|128|0)\.0)$|^(255\.255\.255\.(255|254|252|248|240|224|192|128|0))$', mask):
        return True
    else:
        return False


def check_mac(mac):
    if re.match(r"^\s*([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}\s*$", mac):
        return True
    return False


def check_role_name(name):
    if not isinstance(name, unicode):
        try:
            name = str(name).decode("utf-8")
        except:
            return False
    if not (name and 1 <= len(name) <= 8):
        return False
    for ch in name:
        if not (u'\u4e00' <= ch <= u'\u9fff' or u'\u0041' <= ch <= u'\u005a' or u'\u0061' <= ch <= u'\u007a' or u'\u0030' <= ch <= u'\u0039'):
            return False
    if name[0] == "_":
        return False
    return True


def check_any_name(name, min, max):
    if not isinstance(name, unicode):
        try:
            name = str(name).decode("utf-8")
        except:
            return False
    if not (name and min <= len(name) <= max):
        return False
    for ch in name:
        if not (u'\u4e00' <= ch <= u'\u9fff' or u'\u0041' <= ch <= u'\u005a' or u'\u0061' <= ch <= u'\u007a' or u'\u0030' <= ch <= u'\u0039' or ch in ['(', ')']):
            return False
    if name[0] == "_":
        return False
    return True
