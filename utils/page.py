# -*- coding: utf-8 -*-
from config import permission_list
import json
from tools import to_string

def get_page_permission(permission_session):
    data = []
    if not isinstance(permission_session, dict):
        permission_session = json.loads(permission_session)
    for key in permission_session:
        if key in permission_list:
            if permission_session[key]['r']:
                data.append(to_string(key))
    return data