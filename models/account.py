# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pymongo
from config import MongodbHost, MongodbPort, MongodbUser, MongodbPassword, MongodbAuthDb,  MongoBasicInfoDb, USER_NAME_COLLECTION, PERMISSION_NAME_COLLECTION, OPEN_ID_COLLECTION, MONGO_USE_RS, MONGO_RS_HOST_PORT
import string
from utils.tools import to_unicode,to_string
from utils.hashers import make_password
from utils.check import check_role_name



class BaseAccount(object):
    def __init__(self):
        mongo_client = MongoClient(host=MongodbHost, port=MongodbPort)
        if MongodbUser and MongodbPassword and MongodbAuthDb:
            mongo_client[MongodbAuthDb].authenticate(MongodbUser, MongodbPassword)
        self._mongo_client = mongo_client
        self._user_collection = self._mongo_client[MongoBasicInfoDb][USER_NAME_COLLECTION]
        self._open_id_collection = self._mongo_client[MongoBasicInfoDb][OPEN_ID_COLLECTION]
        self._permission_collection = self._mongo_client[MongoBasicInfoDb][PERMISSION_NAME_COLLECTION]

    @staticmethod
    def add_new_main_account(**kwargs):
        raise NotImplementedError("can't add new main_account by this object now")

    @staticmethod
    def find_by_open_id(open_id):
        mongo_client = MongoClient(host=MongodbHost, port=MongodbPort)
        if MongodbUser and MongodbPassword and MongodbAuthDb:
            mongo_client[MongodbAuthDb].authenticate(MongodbUser, MongodbPassword)
        open_id_coll = mongo_client[MongoBasicInfoDb][OPEN_ID_COLLECTION]
        open_id_doc = open_id_coll.find_one({"_id": open_id})
        if not open_id_doc:
            return None
        return Account(open_id_doc['main_account_id'], open_id_doc['subaccount_id'])


class Account(BaseAccount):
    def __init__(self, main_account_id, subaccount_id=None):
        super(Account, self).__init__()
        if subaccount_id is None:
            self.is_subaccount = False
            self.is_main_account = True
            self.account_id = main_account_id
        else:
            self.is_subaccount = True
            self.is_main_account = False
            self.account_id = subaccount_id
        self.main_account_id = main_account_id
        self.subaccount_id = subaccount_id
        if self.is_main_account:
            self.superior_accounts_id = [self.main_account_id]
        else:
            self.superior_accounts_id = []
        self.all_subaccounts = []
        self.subordinate_accounts_id = []
        self.document = {}
        self._set_account_info()
        self.role = to_string(self.document.get("role", ""))
        self.group = to_string(self.document.get("group", ""))
        self.own_roles = self.document.get("own_roles", [])



    def _get_account_info_recursively(self, superior_account_id, subaccounts):
        """
        递归查询到指定的子账户，设置对象的属性
        :param superior_account_id:
        :param subaccounts:
        :return:
        """
        if subaccounts.has_key(self.subaccount_id):
            self.document = subaccounts[self.subaccount_id]
            # self.alert_group = to_string(self.document["alertGroup"], True)
            self.status = to_string(self.document["status"], True)
            self.tel = to_string(self.document["tel"], True)
            self.email = to_string(self.document["user_email"], True)
            self.account_name = to_string(self.document["user_name"], True)

            self.direct_superior_account_id = superior_account_id

            return True
        else:
            for subaccount_id in subaccounts:
                ret = self._get_account_info_recursively(subaccount_id,
                                                         subaccounts[subaccount_id].get("subaccount", {}))
                if not ret is None:
                    self.superior_accounts_id.insert(1, to_string(subaccount_id))
                    return ret

    def _set_account_info(self):
        """
        初始化中调用设置类的各种属性
        :return:
        """
        doc = self._user_collection.find_one({"_id": self.main_account_id})
        if doc is None:
            raise AccountNotExistError("main_account does not exist")
        else:
            subaccount_exists = self._get_account_info_recursively(self.main_account_id, doc.get("subaccount"))
            self.idcs = map(to_string, doc.get("idcs", []))
            if not subaccount_exists and self.is_subaccount:
                raise AccountNotExistError("subaccount does not exist")
            elif self.is_main_account:
                self.document = doc
                self.alert_group = doc["alertGroup"]
                self.status = to_string(doc["status"], True)
                self.tel = to_string(doc["tel"], True)
                self.email = to_string(doc["user_email"], True)
                self.account_name = to_string(doc["user_name"], True)
                self.own_roles = to_string(doc["own_roles"], True)
                self._traversal_account_tree(doc)

    def _traversal_account_tree(self, account_tree):
        """
        递归遍历整个用户树，获取并设置下级账号及当前账号能看到的客户
        :param account_tree:
        :return:
        """
        self.subordinate_accounts_id += map(to_string, account_tree.get('subaccount', {}).keys())
        subs = [[sub, account_tree['subaccount'][sub]['user_name'], account_tree['subaccount'][sub]['role'], account_tree['subaccount'][sub]['group']] for sub in account_tree.get("subaccount", {})]
        self.all_subaccounts += subs
        if account_tree.has_key("subaccount"):
            for subordinate_account in account_tree['subaccount'].values():
                self._traversal_account_tree(subordinate_account)

    def add_subaccount(self, subaccount_id, password, alertGroup, permission, role, tel, user_email, user_name,
                       group=None, wechat_id=None, status=True, direct_superior_account_id=None):
        subaccount_id = to_string(subaccount_id, True)
        password = make_password(password)
        role = to_string(role, True)
        tel = to_string(tel, True)
        user_email = to_string(user_email, True)
        user_name = to_string(user_name, True)
        status = bool(status)
        local_account_info = {
            "password": password,
            "role": role,
            'group': group,
            "status": status,
            "subaccount": {},
            "tel": tel,
            "user_email": user_email,
            "user_name": user_name,
        }
        if direct_superior_account_id is None:
            direct_superior_account_id = self.subaccount_id if self.is_subaccount else self.main_account_id
        if self.account_exist(subaccount_id):
            raise AccountExistError("subaccount already exists!")
        else:
            account_obj = Account(self.main_account_id)
            flag = account_obj.setSubPermission(subaccount_id, permission)
            if flag:
                return self._add_or_update_subaccount(subaccount_id, direct_superior_account_id=direct_superior_account_id,
                                                  **local_account_info)
            else:
                return False

    def setSubPermission(self, sub_id, permission_list):
        p_coll = self._permission_collection
        data = {}
        for arr in permission_list:
            if arr[1] == 'w':
                data[arr[0]] = {
                    'w': True,
                    'r': True
                }
            elif arr[1] == 'r':
                data[arr[0]] = {
                    'w': False,
                    'r': True
                }
        res = p_coll.update_one({'_id': self.main_account_id}, {
            '$set': {
                sub_id: data
            }
        })
        if res.modified_count or res.matched_count:
            return True
        else:
            return False

    def getSubaccountPermission(self, subaccount_id):
        collection = self._permission_collection
        main_account = self.main_account_id
        result = collection.find_one({'_id': str(main_account)})
        if result is None:
            return False
        if result.get(subaccount_id, None):
            return result[subaccount_id]
        else:
            return False

    def get_all_roles(self):
        collection = self._user_collection
        main_account = self.main_account_id
        result = collection.find_one({'_id': str(main_account)})
        if result is None:
            return False
        if result.get('own_roles', None):
            return [role for role in result['own_roles']]
        else:
            return False

    def get_roles_and_groups(self):
        collection = self._user_collection
        main_account = self.main_account_id
        result = collection.find_one({'_id': str(main_account)})
        if result is None:
            return False
        if result.get('own_roles', None):
            data = {}
            for key in result['own_roles']:
                    data[key] = [g_name for g_name in result['own_roles'][key]['own_groups']]
            return data
        else:
            return False

    def is_exist_group_in_role(self, role_name, group_name):
        collection = self._user_collection
        main_account = self.main_account_id
        result = collection.find_one({'_id': str(main_account)})
        if result is None:
            return False
        if result.get('own_roles', None):
            group_list = [g for g in result['own_roles'][to_unicode(role_name)]['own_groups']]
            if group_name in group_list:
                return True
        else:
            return False

    def get_self_rank(self):
        collection = self._user_collection
        main_account = self.main_account_id
        result = collection.find_one({'_id': str(main_account)})
        if not result:
            return False
        if result.get('own_roles', None):
            role_doc = result['own_roles']
            rank = role_doc[to_unicode(self.role)]['own_groups'][to_unicode(self.group)]['rank']
            return rank
        else:
            return False

    def del_subaccount(self, subaccount_id):
        """
        删除子账户
        :param subaccount_id:子账户id
        :param direct_superior_account_id:子账户的直接上级账户id
        :return:
        """
        subaccount_to_be_modified = Account(self.main_account_id, subaccount_id)
        direct_superior_account_id = subaccount_to_be_modified.direct_superior_account_id
        if self.is_main_account and direct_superior_account_id == self.main_account_id:
            res = self._user_collection.update_one(
                {"_id": self.main_account_id},
                {
                    "$unset": {
                        "subaccount.{0}".format(subaccount_id): ""
                    }
                },
                True
            )
            return res.raw_result['ok'] == 1
        elif self.is_subaccount and direct_superior_account_id == self.subaccount_id:
            set_index = string.join(["subaccount.%s" % sub_id for sub_id in self.superior_accounts_id[1:]], ".")
            if set_index:
                set_index += "."
            set_index += "subaccount.%s" % direct_superior_account_id
            set_index = "{0}.subaccount.{1}".format(set_index, subaccount_id)
            res = self._user_collection.update_one(
                {"_id": self.main_account_id},
                {
                    "$unset": {
                        set_index: ""
                    }
                },
                True
            )
            return res.raw_result['ok'] == 1
        else:
            sub_account_obj = Account(self.main_account_id, direct_superior_account_id)
            ret = sub_account_obj.del_subaccount(subaccount_id)
            return ret

    def add_role(self, role_name):
        user_coll = self._user_collection
        own_roles = self.own_roles
        if not own_roles:
            return False, '不存在角色字段'
        if not check_role_name(role_name):
            return False, '角色名称不符合规定'
        if own_roles.has_key(role_name):
            return False, '角色名称已存在'

        res = user_coll.update_one({'_id': self.main_account_id}, {
            '$set': {
                'own_roles.{0}'.format(role_name): {
                    'type': 'set',
                    'own_groups': {
                        '{0}组长'.format(role_name): {
                            'rank': 3,
                            'type': 'preset'
                        },
                        '{0}组员'.format(role_name): {
                            'rank': 4,
                            'type': 'preset'
                        },
                    }
                }
            }
        })
        if res.modified_count or res.matched_count:
            return True, ""
        else:
            return False, "添加失败"

    def modify_role_name(self, old_name, new_name):
        user_coll = self._user_collection
        own_roles = self.own_roles
        if not own_roles:
            return False, '不存在角色字段'
        if not check_role_name(new_name):
            return False, '角色名称不符合规定'
        if not own_roles.has_key(old_name):
            return False, '角色不存在'
        if old_name in ['管理', '教师', '学生']:
            return False, '不能修改内置角色名称'

        res = user_coll.update_one({'_id': self.main_account_id}, {
            '$rename': {
                'own_roles.{0}'.format(old_name): 'own_roles.{0}'.format(new_name)
            }
        })
        if res.modified_count or res.matched_count:
            return True, ""
        else:
            return False, "修改失败"

    def del_role(self, role_name):
        user_coll = self._user_collection
        own_roles = self.own_roles
        if not own_roles:
            return False, '不存在角色字段'
        if not check_role_name(role_name):
            return False, '角色名称不符合规定'
        if role_name in [u'管理', u'教师', u'学生']:
            return False, '内置角色不许删除'
        if role_name not in own_roles.keys():
            return False, '不存在的角色信息'
        res = user_coll.update_one({'_id': self.main_account_id}, {
            '$unset': {
                'own_roles.{0}'.format(role_name): ''
            }
        })
        if res.modified_count or res.matched_count:
            return True, ""
        else:
            return False, '删除角色失败'

    def add_group_for_role(self, role_name, group_name, rank):
        user_coll = self._user_collection
        own_roles = self.own_roles
        if not own_roles:
            return False, '不存在角色字段'
        if not (check_role_name(group_name) and check_role_name(role_name)):
            return False, '角色名称或分组名称不符合规定'
        if role_name not in own_roles.keys():
            return False, '不存在的角色'
        group_doc = own_roles[role_name].get(group_name, '')
        if group_doc:
            return False, '分组信息已存在'
        if not isinstance(rank, int):
            return False, '等级参数不合理'
        if not (1 < rank < 10):
            return False, '等级值参数须在1到10之间'
        exist_ranks = [own_roles[role_name]['own_groups'][group]['rank'] for group in own_roles[role_name]['own_groups']]
        if rank in exist_ranks:
            return False, '等级值参数已存在'
        res = user_coll.update_one({'_id': self.main_account_id}, {
            '$set': {
                'own_roles.{0}.own_groups.{1}'.format(role_name, group_name): {
                    'rank': rank,
                    'type': 'set'
                }
            }
        })
        if res.modified_count or res.matched_count:
            return True, ""
        else:
            return False, '添加分组失败'

    def del_group_for_role(self, role_name, group_name):
        user_coll = self._user_collection
        own_roles = self.own_roles
        if not own_roles:
            return False, '不存在角色字段'
        if not (check_role_name(group_name) and check_role_name(role_name)):
            return False, '角色名称或分组名称不符合规定'
        if role_name not in own_roles.keys():
            return False, '不存在的角色'
        if group_name in ['组长组', '组员组']:
            return False, '内置分组不许删除'
        group_doc = own_roles[role_name]['own_groups'].get(group_name, '')
        if not group_doc:
            return False, '分组信息不存在'

        res = user_coll.update_one({'_id': self.main_account_id}, {
            '$unset': {
                'own_roles.{0}.own_groups.{1}'.format(role_name, group_name): ''
            }
        })
        if res.modified_count or res.matched_count:
            return True, ""
        else:
            return False, '删除分组失败'

    def modify_group_for_role(self, role_name, old_group_name, new_group_name, rank):
        user_coll = self._user_collection
        own_roles = self.own_roles
        if not own_roles:
            return False, '不存在角色字段'
        if not (check_role_name(new_group_name) and check_role_name(role_name)):
            return False, '角色名称或分组名称不符合规定'
        if role_name not in own_roles.keys():
            return False, '不存在的角色'
        if new_group_name in ['组长组', '组员组']:
            return False, '内置分组不许修改'
        group_doc = own_roles[role_name]['own_groups'].get(old_group_name, '')
        if not group_doc:
            return False, '分组信息不存在'
        if not isinstance(rank, int):
            return False, '级别参数不合理'
        if not (1 < rank < 10):
            return False, '级别值参数须在1-10之间'
        exist_ranks = [own_roles[role_name]['own_groups'][group]['rank'] for group in own_roles[role_name]['own_groups']]
        if rank in exist_ranks:
            return False, '等级值参数已存在'
        res = user_coll.update_one({'_id': self.main_account_id}, {
            '$set': {
                'own_roles.{0}.own_groups.{1}.rank'.format(role_name, old_group_name): rank
            }
        })
        if res.modified_count or res.matched_count:
            if old_group_name != new_group_name:
                result = user_coll.update_one({'_id': self.main_account_id}, {
                    '$rename': {
                        'own_roles.{0}.own_groups.{1}'.format(role_name, old_group_name): 'own_roles.{0}.own_groups.{1}'.format(role_name, new_group_name)
                    }
                })
                if result.modified_count:
                    return True, ''
                else:
                    return False, '修改分组名称失败'
            else:
                return True, ''
        else:
            return False, '修改分组失败'



    def modify_subaccount(self, subaccount_id, modify_args):
        assert isinstance(modify_args, dict)
        subaccount_to_be_modified = Account(self.main_account_id, subaccount_id)
        direct_superior_account_id = subaccount_to_be_modified.direct_superior_account_id
        subaccount_id = to_string(subaccount_id, True)
        modify_dict = {}
        if modify_args.has_key("status"):
            modify_dict["status"] = modify_args["status"]
        if modify_args.has_key("alertGroup"):
            alertGroup = modify_args["alertGroup"]
            alertGroup = {
                "warn": bool(alertGroup["warn"]),
                "info": bool(alertGroup["info"]),
                "critical": bool(alertGroup["critical"])
            }
            modify_dict["alertGroup"] = alertGroup
        if modify_args.has_key("role"):
            role = to_string(modify_args["role"], True)
            if role == '管理':
                modify_dict['group'] = None
            modify_dict["role"] = role
        if modify_args.has_key('permission'):
            permission_list = modify_args['permission'] if isinstance(modify_args['permission'], list) else list(modify_args['permission'])
            main_account = Account(self.main_account_id)
            set_res = main_account.setSubPermission(subaccount_id, permission_list)
            if not set_res:
                return False
        accept_strings = ["group", "tel", "user_email", "user_name"]
        for k in accept_strings:
            if modify_args.has_key(k):
                v = to_string(modify_args[k], True)
                modify_dict[k] = v

        return self._add_or_update_subaccount(subaccount_id, insert=False,
                                              direct_superior_account_id=direct_superior_account_id, **modify_dict)

    def get_subaccount_document(self, subaccount_id):
        """
        获取一个子账户在mongo中的document
        :param subaccount_id:
        :return:
        """
        if subaccount_id in self.subordinate_accounts_id:
            return self._get_subaccount_recursively(self.document, subaccount_id)

    def _get_subaccount_recursively(self, document, subaccount_id):
        """
        递归查询一个账户的document，直到查找到指定子账户
        :param document:
        :param subaccount_id:
        :return:
        """
        if document.get("subaccount", {}).has_key(subaccount_id):
            subaccount = document["subaccount"][subaccount_id]
            subaccount["id"] = subaccount_id
            return subaccount
        elif document.get("subaccount", {}).has_key(to_unicode(subaccount_id)):
            subaccount = document["subaccount"][to_unicode(subaccount_id)]
            subaccount["id"] = subaccount_id
            return subaccount
        else:
            for sub_doc in document.get("subaccount", {}).values():
                ret = self._get_subaccount_recursively(sub_doc, subaccount_id)
                if not ret is None:
                    return ret

    def _add_or_update_subaccount(self, subaccount_id, direct_superior_account_id=None, insert=True, **subaccount_info):
        if direct_superior_account_id is None:
            direct_superior_account_id = self.subaccount_id if self.is_subaccount else self.main_account_id
        if not insert:
            self.verify_permission(subaccount_id)
        if self.is_main_account and direct_superior_account_id == self.main_account_id:
            if insert:
                set_dict = {"subaccount.{0}".format(subaccount_id): subaccount_info}
            else:
                set_dict = {}
                for k in subaccount_info:
                    set_dict["subaccount.{0}.{1}".format(subaccount_id, to_string(k))] = subaccount_info[k]

            res = self._user_collection.update_one(
                {"_id": self.main_account_id},
                {
                    "$set": set_dict
                },
                insert
            )
            return res.raw_result['ok'] == 1
        elif self.is_subaccount and direct_superior_account_id == self.subaccount_id:

            set_index = string.join(["subaccount.%s" % sub_id for sub_id in self.superior_accounts_id[1:]], ".")
            if len(set_index) > 0:
                set_index += '.'
            set_index += "subaccount.%s" % direct_superior_account_id
            set_index = "{0}.subaccount.{1}".format(set_index, subaccount_id)
            if insert:
                set_dict = {set_index: subaccount_info}
            else:
                set_dict = {}
                for k in subaccount_info:
                    set_dict["{0}.{1}".format(set_index, k)] = subaccount_info[k]

            res = self._user_collection.update_one(
                {"_id": self.main_account_id},
                {
                    "$set": set_dict
                },
                insert
            )
            return res.raw_result['ok'] == 1
        else:
            subaccount_obj = Account(self.main_account_id,
                                     None if direct_superior_account_id == self.main_account_id else direct_superior_account_id)
            ret = subaccount_obj._add_or_update_subaccount(subaccount_id,
                                                           direct_superior_account_id=direct_superior_account_id,
                                                           insert=insert, **subaccount_info)
            return ret

    def del_group_for_role(self, role_name, group_name):
        user_coll = self._user_collection
        own_roles = self.own_roles
        if not own_roles:
            return False, '不存在角色字段'
        if not (check_role_name(group_name) and check_role_name(role_name)):
            return False, '角色名称或分组名称不符合规定'
        if role_name not in own_roles.keys():
            return False, '不存在的角色'
        if group_name in ['组长组', '组员组']:
            return False, '内置分组不许删除'
        group_doc = own_roles[role_name]['own_groups'].get(group_name, '')
        if not group_doc:
            return False, '分组信息不存在'

        res = user_coll.update_one({'_id': self.main_account_id}, {
            '$unset': {
                'own_roles.{0}.own_groups.{1}'.format(role_name, group_name): ''
            }
        })
        if res.modified_count or res.matched_count:
            return True, ""
        else:
            return False, '删除分组失败'

    def modify_group_for_role(self, role_name, old_group_name, new_group_name, rank):
        user_coll = self._user_collection
        own_roles = self.own_roles
        if not own_roles:
            return False, '不存在角色字段'
        if not (check_role_name(new_group_name) and check_role_name(role_name)):
            return False, '角色名称或分组名称不符合规定'
        if role_name not in own_roles.keys():
            return False, '不存在的角色'
        if new_group_name in ['组长组', '组员组']:
            return False, '内置分组不许修改'
        group_doc = own_roles[role_name]['own_groups'].get(old_group_name, '')
        if not group_doc:
            return False, '分组信息不存在'
        if not isinstance(rank, int):
            return False, '级别参数不合理'
        if not (1 < rank < 10):
            return False, '级别值参数须在1-10之间'
        exist_ranks = [own_roles[role_name]['own_groups'][group]['rank'] for group in
                       own_roles[role_name]['own_groups']]
        if rank in exist_ranks:
            return False, '等级值参数已存在'
        res = user_coll.update_one({'_id': self.main_account_id}, {
            '$set': {
                'own_roles.{0}.own_groups.{1}.rank'.format(role_name, old_group_name): rank
            }
        })
        if res.modified_count or res.matched_count:
            if old_group_name != new_group_name:
                result = user_coll.update_one({'_id': self.main_account_id}, {
                    '$rename': {
                        'own_roles.{0}.own_groups.{1}'.format(role_name,
                                                              old_group_name): 'own_roles.{0}.own_groups.{1}'.format(
                            role_name, new_group_name)
                    }
                })
                if result.modified_count:
                    return True, ''
                else:
                    return False, '修改分组名称失败'
            else:
                return True, ''
        else:
            return False, '修改分组失败'

    def verify_permission(self, account_id):
        self.update()
        if self.is_main_account and not (
                account_id == self.main_account_id or account_id in self.subordinate_accounts_id):
            # 是主账户，且负责人账户不等于主账户，且负责人不是此账户的下级账户
            raise AccountNotExistError("account dose not exist '%s'" % account_id)
        if self.is_subaccount and not (account_id == self.subaccount_id or account_id in self.subordinate_accounts_id):
            # 是子账户，且负责人账户不是这个子账户，且负责人不是此子账户的下级账户
            raise PermissionInsufficientError("No permission to operate account '%s'" % account_id)

    def account_exist(self, account_id):
        self.update()
        main_account = Account(self.main_account_id)
        return account_id in main_account.subordinate_accounts_id or account_id == self.main_account_id

    def update(self):
        """
        将当前对象的各项属性和数据库中同步
        :return:
        """
        self.__init__(self.main_account_id, self.subaccount_id)

    def __str__(self):
        if self.is_main_account:
            return "MainAccount(%s)" % to_string(self.main_account_id)
        else:
            return "Subaccount(%s:%s)" % (to_string(self.main_account_id), to_string(self.subaccount_id))

    def __unicode__(self):
        if self.is_main_account:
            return u"MainAccount(%s)" % to_unicode(self.main_account_id)
        else:
            return u"Subaccount(%s:%s)" % (to_unicode(self.main_account_id), to_unicode(self.subaccount_id))


class AccountNotExistError(Exception):
    pass


class AccountExistError(Exception):
    pass


class CustomerExistError(Exception):
    pass


class CustomerNotExistError(Exception):
    pass


class PermissionInsufficientError(Exception):
    pass


if __name__ == "__main__":
    password = 'asdasd'
    password = make_password(password)
    print password