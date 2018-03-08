#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import re
import string
import time
from base import BaseInfluxtor
from config import BaseIpMeasurement, BasePortMeasurement, BaseSwitchMeasurement, BaseTenantMeasurement, MIN_RESOLUTION, IP_TAG_MEASUREMENT, TENANT_TAG_MEASUREMENT, TCP_STATUS_MEASUREMENT, DDOS_TRAFFIC_MEASUREMENT
from tornado.gen import coroutine, Return
from utils.handle_time import get_influxdb_ts


def parse_result_set(result_set, field='', func='', method='mean'):
    _res_dict = {}
    _res_list = []
    pattern = re.compile('mean_.*')

    if result_set:
        res_raw = result_set.raw
        res_series = res_raw.get('series')[0]
        res_values = res_series.get('values')
        res_key = res_series.get('columns')

        for res_value in res_values:
            for i in range(len(res_value)):
                key = res_key[i]
                if key == func:
                    key = field

                if pattern.match(key):
                    key = key[5:len(key)]
                _res_dict.update({key: res_value[i]})
            _res_dict_bak = copy.deepcopy(_res_dict)
            _res_list.append(_res_dict_bak)
    return _res_list


class Influxtor(BaseInfluxtor):
    ip_measurement = BaseIpMeasurement + "_" + str(MIN_RESOLUTION) + "s"
    port_measurement = BasePortMeasurement + "_" + str(MIN_RESOLUTION) + "s"
    switch_measurement = BaseSwitchMeasurement + "_" + str(MIN_RESOLUTION) + "s"
    tenant_measurement = BaseTenantMeasurement + "_" + str(MIN_RESOLUTION) + "s"
    ip_tag = IP_TAG_MEASUREMENT
    tenant_tag = TENANT_TAG_MEASUREMENT
    ddos_traffic = DDOS_TRAFFIC_MEASUREMENT

    def __init__(self, idc):
        super(Influxtor, self).__init__(idc)

    @coroutine
    def get_all_ip(self, now, measurement=ip_measurement):
        statement = "SELECT * FROM %s where time=%s" % (measurement, now)
        res_set = yield self.query(statement)
        res_list = parse_result_set(res_set)
        raise Return(res_list)

    @coroutine
    def ym_get_ip(self, now, ip, measurement=ip_measurement):
        statement = "SELECT * FROM %s where time=%s AND ip='%s'" % (measurement, now, ip)
        res_set = yield self.query(statement)
        res_list = parse_result_set(res_set)
        raise Return(res_list)

    @coroutine
    def get_ip_tag(self, now, ip, measurement=ip_tag):
        statement = "SELECT * FROM %s WHERE time='%s' AND ip='%s'" % (measurement, now, ip)
        res_set = yield self.query(statement)
        res_list = parse_result_set(res_set)
        raise Return(res_list)

    @coroutine
    def batch_get_ips_tag(self, now, ips, measurement=ip_tag):
        qstr = "SELECT * FROM %s WHERE time='%s' GROUP BY ip ORDER BY time DESC LIMIT 1" % (measurement, now)
        res = yield self.query(qstr)
        ret_dic = {}
        for ip in ips:
            ret_dic[ip] = None
        for item in res.items():
            if item[0][1]["ip"] in ips:
                points = list(item[1])
                if points:
                    ret_dic[item[0][1]["ip"]] = points[0]
        raise Return(ret_dic)

    @coroutine
    def ym_get_ips_tags(self, now, measurement=ip_tag):
        statement = "SELECT * FROM %s WHERE time=%s GROUP BY ip ORDER BY time DESC LIMIT 1" % (measurement, now)
        res = yield self.query(statement)
        ret_dic = {}
        for item in res.items():
            if item[0][1]["ip"]:
                points = list(item[1])
                if points:
                    ret_dic[item[0][1]["ip"]] = points[0]
        raise Return(ret_dic)

    @coroutine
    def batch_get_ip_tcp_status(self, ips, dports, measurement=TCP_STATUS_MEASUREMENT):  # tcp_status的查询
        qstr = "SELECT * FROM %s GROUP BY ipv4_dst, dport ORDER BY time DESC LIMIT 1" % measurement
        res = self.query(qstr)
        ret_dic = {}
        for ip in ips:
            if not ret_dic.has_key(ip):
                ret_dic[ip] = {}
            for dport in dports:
                ret_dic[ip][dport] = None
        res = yield res
        for item in res.items():
            try:
                if item[0][1]["ipv4_dst"] in ips and int(item[0][1]["dport"]) in dports:
                    points = list(item[1])
                    if points:
                        ret_dic[item[0][1]["ipv4_dst"]][item[0][1]["dport"]] = points[0]
            except Exception as e:
                continue
        raise Return(ret_dic)

    @coroutine
    def get_port_tcp_status(self, now, ips, dports, measurement=ip_measurement):
        qstr = "SELECT * FROM %s WHERE time=%s GROUP BY ip, dport" % (measurement, now)
        res = self.query(qstr)
        ret_dic = {}
        for ip in ips:
            if not ret_dic.has_key(ip):
                ret_dic[ip] = {}
            for dport in dports:
                ret_dic[ip][dport] = None
        res = yield res
        for item in res.items():
            try:
                if item[0][1]["ip"] in ips and int(item[0][1]["dport"]) in dports:

                    points = list(item[1])
                    if points:
                        ret_dic[item[0][1]["ip"]][item[0][1]["dport"]] = points[0]
            except Exception as e:
                continue
        raise Return(ret_dic)

    @coroutine
    def get_tenant_tag(self, tenant, measurement=tenant_tag):
        statement = "SELECT * FROM %s WHERE tenant='%s' ORDER BY time DESC limit 1" % (measurement, tenant)
        res_set = yield self.query(statement)
        res_list = parse_result_set(res_set)
        raise Return(res_list)

    @coroutine
    def batch_get_tenants_tag(self, tenants, measurement=tenant_tag):
        qstr = "SELECT * FROM %s GROUP BY tenant ORDER BY time DESC LIMIT 1" % measurement
        res = yield self.query(qstr)
        ret_dic = {}
        for tenant in tenants:
            ret_dic[tenant] = 0

        for item in res.items():
            if item[0][1]["tenant"] in tenants:
                points = list(item[1])
                if points:
                    ret_dic[item[0][1]["tenant"]] = points[0]
        raise Return(ret_dic)

    @coroutine
    def get_ips_tag(self, now, tenant, measurement=ip_tag):
        statement = "SELECT * FROM %s WHERE time='%s' AND tenant='%s'" % (measurement, now, tenant)
        res_set = yield self.query(statement)
        res_list = parse_result_set(res_set)
        raise Return(res_list)

    @coroutine
    def ym_get_tenants_tags(self, now, measurement=tenant_tag):
        statement = "SELECT * FROM %s WHERE time=%s GROUP BY tenant ORDER BY time DESC limit 1" % (measurement, now)
        res = yield self.query(statement)
        ret_dic = {}
        for item in res.items():
            if item[0][1]["tenant"]:
                points = list(item[1])
                if points:
                    ret_dic[item[0][1]["tenant"]] = points[0]
        raise Return(ret_dic)

    @coroutine
    def get_all_tenant(self, now, measurement=tenant_measurement):
        statement = "SELECT * FROM %s WHERE time=%s" % (measurement, now)
        res_set = yield self.query(statement)
        res_list = parse_result_set(res_set)
        raise Return(res_list)

    @coroutine
    def get_one_tenant(self, meters,  now, measurement=tenant_measurement):
        str = ("' or meter_id='").join(meters)
        statement = "SELECT * FROM %s WHERE time=%s AND (meter_id='%s')" % (measurement, now, str)
        res_set = yield self.query(statement)
        res_list = parse_result_set(res_set)
        raise Return(res_list)

    @coroutine
    def query_by_port(self, dpid, port, now, measurement=port_measurement):
        statement = "SELECT * FROM %s where dpid='%i' and port='%i' and time='%s'" % (
            measurement, dpid, port, now)
        res_set = yield self.query(statement)
        res_list = parse_result_set(res_set)
        raise Return(res_list)

    @coroutine
    def query_by_switch(self, dpid, now, measurement=port_measurement):
        statement = "SELECT SUM(bit_count) AS bit_count, SUM(packet_count) AS packet_count FROM %s where dpid='%i' and time=%s GROUP BY type" % (measurement, dpid, now)
        res_set = yield self.query(statement)
        ret = {
            "in_bit_count":0,
            "in_packet_count": 0,
            "out_bit_count": 0,
            "out_packet_count": 0,
        }
        for (m, groups), points in res_set.items():
            if groups.get('type') in ['in', 'out']:
                points = list(points)
                assert len(points) <= 1
                if len(points) == 1:
                    ret["%s_bit_count" % groups.get('type')] = points[0]['bit_count']
                    ret["%s_packet_count" % groups.get('type')] = points[0]['packet_count']
        raise Return(ret)

    # @coroutine
    # def query_by_ip(self, ip, _type, now, measurement=ip_measurement):
    #     statement = "SELECT * FROM %s where ip='%s' and type='%s' and time=%s " % (measurement, ip, _type, now)
    #     res_set = yield self.query(statement)
    #     res_list = parse_result_set(res_set)
    #     raise Return(res_list)

    @coroutine
    def query_by_condition(self, condition, now, measurement=ip_measurement):
        statement = "SELECT * FROM %s where time=%s %s " % (measurement, now, condition)
        res_set = yield self.query(statement)
        res_list = parse_result_set(res_set)
        raise Return(res_list)

    @coroutine
    def query_by_time(self, measurement, start, end, method='', **kwargs):
        other_condition = ''
        for k in kwargs.keys():
            v = str(kwargs[k].encode("utf8"))
            if " OR " in v or " or " in v:
                values = re.split(r" or | OR ", v)
                qs_list = ["{0}='{1}'".format(k, v) for v in values]
                other_condition += "and ({0})".format(string.join(qs_list, " OR "))
            else:
                other_condition += "and %s='%s'" % (k, v)
        if not method:
            statement = "SELECT bit_count , packet_count , meter_id, mac, dport, type FROM %s where time >= '%s' and time <= '%s' %s " % (
                measurement, start, end, other_condition)
        else:
            bit_count = '_'.join([method, 'bit_count'])
            packet_count = '_'.join([method, 'packet_count'])
            statement = "SELECT %s AS bit_count, %s AS packet_count, meter_id, dport, type FROM %s where time >= '%s' and time <= '%s' %s " % (
                bit_count, packet_count, measurement, start, end, other_condition
            )
        res_set = yield self.query(statement)
        res_list = parse_result_set(res_set)
        raise Return(res_list)

    @coroutine
    def query_switch_ports(self, dpid, now, measurement=port_measurement):
        statement = "SELECT * FROM %s where dpid='%i' and time=%s" % (measurement, dpid, now)
        res_set = yield self.query(statement)
        res_list = parse_result_set(res_set)
        raise Return(res_list)

    @coroutine
    def get_continuous_queries(self):
        res_set = yield self.query("SHOW CONTINUOUS QUERIES")
        cq_list = res_set.raw.get('series')
        _cq = []

        for cq in cq_list:
            if cq.get('name') == self.db_name:
                _cq = cq.get('values')
        raise Return(_cq)

    @coroutine
    def add_continuous_query(self, cq_name, cq_query):
        cq = "CREATE CONTINUOUS QUERY %s ON %s \
                  BEGIN\
                    %s\
                END" % (cq_name, self.db_name, cq_query)
        yield self.client.query(cq)


    @coroutine
    def get_attack_flow(self, start, end=None, measurement='ddos_traffic_10s', defend_ip=''):
        if not end:
            query_res = "SELECT MAX(bit_count::INTEGER) as bit_sum,packet_count FROM %s WHERE time>'%s' AND ipv4_dst='%s'"%(
                measurement,start,defend_ip
            )
        else:
            query_res = "SELECT MAX(bit_count::INTEGER) as bit_sum,packet_count FROM %s WHERE time>'%s' AND time <'%s' AND ipv4_dst='%s'" % (
                measurement, start, end, defend_ip
            )
        s = time.time()
        res = yield self.query(query_res)
        res = parse_result_set(res)
        raise Return(res)

    @coroutine
    def get_attack_ip(self, start, end=None, measurement=ddos_traffic, defend_ip=''):
        if not end:
            query_res = "SELECT COUNT(tot) FROM (SELECT first(bit_count::INTEGER) as tot FROM %s WHERE time>'%s' AND ipv4_dst='%s' GROUP BY ipv4_src limit 1)"%(
                measurement,start,defend_ip
            )
        else:
            query_res = "SELECT COUNT(tot) FROM (SELECT first(bit_count::INTEGER) as tot FROM %s WHERE time>'%s' AND  time<'%s' AND ipv4_dst='%s' GROUP BY ipv4_src limit 1)" % (
                measurement, start, end, defend_ip
            )
        s = time.time()
        res = yield self.query(query_res)
        res = parse_result_set(res)
        raise Return(res)

    @coroutine
    def get_current_attack_info(self, now, measurement=ddos_traffic + "_10s"):
        query_res = "SELECT ipv4_dst, bit_count::INTEGER FROM %s WHERE time = %s GROUP BY ipv4_dst" % (measurement, now)
        res = yield self.query(query_res)
        res = parse_result_set(res)
        raise Return(res)

    @coroutine
    def get_attack_event_info(self, start, end, defend_ip, measurement=ddos_traffic):
        query_res = "SELECT max(bit_count) as bit_count,max(packet_count) as packet_count from %s where time>'%s' and time<'%s' and ipv4_dst='%s' group by time(3m) fill(0)" % (measurement, start, end, defend_ip)
        res = yield self.query(query_res)
        res = parse_result_set(res)
        raise Return(res)



if __name__ == "__main__":
    now = get_influxdb_ts(time.time())
    print now