# coding: utf-8

from handlers import *

url = [
    (r"/topo", TopoHandler),
    (r"/", IndexViewHandler),
    (r"/tenant", TenantOverviewHandler),
    (r"/tenant/detail", TenantDetailHandler),
    (r"/tenant_manage", TenantManageHandler),
    (r"/ip",IpHandler),
    (r"/ip/detail",IpDetailHandler),
    (r'/ip_group/detail', IpGroupDetailHandler),
    (r"/switch/detail",SwitchDetailHandler),
    (r"/switch/detail/port",SwitchDetailPortHandler),
    (r"/switch/manage",SwitchManageHandler),
    (r"/subAccount",SubAccountHandler),
    (r"/password", ModifyPasswordHandler),
    (r"/idcsystem", IdcSystemHandler),
]