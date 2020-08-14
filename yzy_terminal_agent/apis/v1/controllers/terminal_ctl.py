import time
import functools
import copy
import random
from datetime import datetime, timedelta
import json
import sys
import os
import struct
import datetime as dt
import logging
import traceback
import base64
import common.errcode as errcode
import hashlib
# from .desktop_ctl import BaseController
from flask import current_app
from yzy_terminal_agent.database import api as db_api
from common.utils import build_result, create_uuid, find_ips, is_ip_addr, create_md5, terminal_post
from common.utils import Singleton, voi_terminal_post, get_error_result, get_error_name
from yzy_terminal_agent.extensions import get_controller_image_ip
from yzy_terminal_agent.redis_client import RedisClient
from yzy_terminal_agent.http_client import HttpClient
from yzy_terminal_agent.ext_libs.redis_pub_sub import RedisMessageCenter
from yzy_terminal_agent.ext_libs.yzy_protocol import YzyTorrentStruct
from common import constants
from common.config import SERVER_CONF
import redis_lock
from simplepam import authenticate
import subprocess


logger = logging.getLogger(__name__)


class TerminalStatus:
    OFF = 0
    UEFI = 1
    LINUX = 2
    WINDOWS = 3
    SERVER = 4
    U_LINUX = 5


class TerminalTaskHandler(object):

    def __init__(self):
        self.name = os.path.basename(__file__).split('.')[0]
        self.type = "TerminalTaskHandler"
        self.msg_center = RedisMessageCenter()
        self.rds = RedisClient()
        self.http_client = HttpClient()

    def create_batch_no(self):
        key_name = "voi_web_command_batch_no"
        return self.rds.incr(key_name)

    def push_torrent_task_list(self, torrent_task):
        """ 种子任务队列 push"""
        pass

    def pop_torrent_task_list(self, task_id):
        pass

    def deal_process(self, data):
        try:
            cmd = data.get("cmd", "")
            func = getattr(self, cmd)
            return func(data)
        except Exception as err:
            logger.error("Error: {}".format(err))
            logger.error(''.join(traceback.format_exc()))
            return build_result("OtherError", msg="en")

    def get_md5(self, input_str):
        md5 = hashlib.md5()
        md5.update(input_str.encode('utf8'))
        md5_value = md5.hexdigest()
        return md5_value

    def set_default_terminal_info(self, mac, ip, status):
        setup_info = {
            'mode': {
                'show_desktop_type': 0,
                'auto_desktop': 0
            },
            'program': {
                'server_ip': ""
            }
        }
        terminal_values = {
            'uuid': create_uuid(),
            'terminal_id': 1,
            'mac': mac,
            'ip': ip,
            'mask': "",
            'gateway': "",
            'dns1': "",
            'dns2': "",
            'is_dhcp': 0,
            'name': "",
            'platform': "",
            'soft_version': "",
            'status': status,
            'register_time': dt.datetime.now(),
            'conf_version': "-1",
            'setup_info': json.dumps(setup_info),
            'disk_residue': 0
        }
        return terminal_values

    def restart_reset_terminals(self, data):
        resp = errcode.get_error_result("Success", msg="en")
        table_api = db_api.YzyVoiTerminalTableCtrl(current_app.db)
        table_api.reset_all_terminal_offline()
        return resp

    def terminal_login(self, data):
        logger.debug("login data: {}".format(data))
        resp = errcode.get_error_result("Success", msg="en")
        insert_data = data.get("data")  # include status of terminal type
        ip_port = "%s:%s" % (insert_data['ip'], insert_data['port'])
        insert_data.pop('port')
        try:
            table_api = db_api.YzyVoiTerminalTableCtrl(current_app.db)
            qry = table_api.select_terminal_by_mac(insert_data['mac'])
            if qry:
                insert_data['register_time'] = dt.datetime.now()
                table_api.update_terminal_by_mac(**insert_data)
                logger.debug('mac: {} set online'.format(insert_data['mac']))
            else:
                terminal_values = self.set_default_terminal_info(insert_data['mac'], insert_data['ip'],
                                                                 insert_data['status'])
                table_api.add_terminal(terminal_values)
                logger.debug('mac: {} add new default yzy_voi_terminal record'.format(insert_data['mac']))
            resp["data"] = {}
            resp["data"]["token"] = self.get_md5(ip_port)
            return resp
        except Exception as err:
            logger.error(err)
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
            return resp

    def terminal_logout(self, data):
        logger.debug("logout data: {}".format(data))
        resp = errcode.get_error_result("Success", msg="en")
        insert_data = data.get("data")
        insert_data['status'] = TerminalStatus.OFF
        try:
            table_api = db_api.YzyVoiTerminalTableCtrl(current_app.db)
            qry = table_api.select_terminal_by_mac(insert_data['mac'])
            if qry:
                table_api.update_terminal_by_mac(**insert_data)
                logger.info('mac: {} set offline'.format(insert_data['mac']))
                request_server_data = {
                    "mac": qry.mac,
                    "cmd": "logout"
                }
                request_url = "/api/v1/voi/terminal/education/update_desktop_bind"
                logger.debug("request yzy_server {}, {}".format(request_url, request_server_data))
                server_ret = self.http_client.post(request_url, request_server_data)
                logger.debug("get yzy_server return {}, {}".format(request_url, server_ret))
                ret_code = server_ret.get("code", -1)
                if ret_code != 0:
                    logger.error("request yzy_server update_desktop_bind return error: %s" % server_ret)
                    resp["msg"] = errcode.get_error_name(ret_code)
                    resp["code"] = ret_code
                logger.info('mac: {} set desktop offline'.format(insert_data['mac']))
            else:
                logger.debug('mac: {} not in yzy_voi_terminal'.format(insert_data['mac']))
            return resp
        except Exception as err:
            logger.error(err)
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
            return resp

    def terminal_except_exit(self, data):
        logger.debug("except_exit data: {}".format(data))
        resp = errcode.get_error_result("Success", msg="en")
        insert_data = data.get("data")
        insert_data['status'] = 0
        try:
            table_api = db_api.YzyVoiTerminalTableCtrl(current_app.db)
            qry = table_api.select_terminal_by_mac(insert_data['mac'])
            if qry:
                table_api.update_terminal_by_mac(**insert_data)
                logger.debug('mac: {} set offline '.format(insert_data['mac']))
                request_server_data = {
                    "mac": qry.mac,
                    "cmd": "logout"
                }
                request_url = "/api/v1/voi/terminal/education/update_desktop_bind"
                logger.debug("request yzy_server {}, {}".format(request_url, request_server_data))
                server_ret = self.http_client.post(request_url, request_server_data)
                logger.debug("get yzy_server return {}, {}".format(request_url, server_ret))
                ret_code = server_ret.get("code", -1)
                if ret_code != 0:
                    logger.error("request yzy_server update_desktop_bind return error: %s" % server_ret)
                    resp["msg"] = errcode.get_error_name(ret_code)
                    resp["code"] = ret_code
                logger.info('mac: {} set desktop offline'.format(insert_data['mac']))
            else:
                logger.debug('mac: {} not in yzy_voi_terminal'.format(insert_data['mac']))
            return resp
        except Exception as err:
            logger.error(err)
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
            return resp

    def get_date_time(self, data):
        logger.debug("get_date_time data: {}".format(data))
        resp = errcode.get_error_result("Success", msg="en")
        resp["data"] = {}
        resp["data"]["datetime"] = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return resp

    def get_config_version_id(self, data):
        logger.debug("data: {}".format(data))
        resp = errcode.get_error_result("Success", msg="en")
        request_data = data.get("data")
        conf_version = -1
        try:
            table_api = db_api.YzyVoiTerminalTableCtrl(current_app.db)
            qry = table_api.select_terminal_by_mac(request_data["mac"])
            if qry:
                conf_version = int(qry['conf_version'])
                logger.debug('conf_version {}'.format(conf_version))
        except Exception as err:
            logger.error('err {}'.format(err))
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
        logger.debug("Return terminal: version = {}".format(conf_version))
        resp["data"] = {}
        resp["data"]["conf_version"] = conf_version
        return resp

    def get_config_info(self, data):
        logger.debug("data: {}".format(data))
        request_data = data.get("data")
        resp = errcode.get_error_result("Success", msg="en")
        try:
            table_api = db_api.YzyVoiTerminalTableCtrl(current_app.db)
            qry = table_api.select_terminal_by_mac(request_data["mac"])
            if qry:
                logger.debug("qry.mac {}, qry.setup_info {}".format(qry.mac, qry.setup_info))
                resp["data"] = qry.to_json()
                logger.debug('resp {}'.format(resp))
            else:
                logger.debug('no mac in yzy_voi_terminal {}'.format(request_data["mac"]))
                resp = errcode.get_error_result(error="OtherError")
        except Exception as err:
            logger.error('err {}'.format(err))
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
        return resp

    def check_config(self, input_data):
        logger.debug(input_data)
        try:
            ret = errcode.get_error_result("Success", msg='en')
            if input_data["terminal_id"] < 0:
                ret = errcode.get_error_result("TerminalIdError", msg="en")
            elif len(input_data["mac"]) == 0:
                ret = errcode.get_error_result("TerminalMacError", msg="en")
            elif not is_ip_addr(input_data["ip"]):
                ret = errcode.get_error_result("TerminalIpError", msg="en")
            elif not is_ip_addr(input_data["mask"]):
                ret = errcode.get_error_result("TerminalMaskError", msg="en")
            #elif not is_ip_addr(input_data["gateway"]):
            #    ret = errcode.get_error_result("TerminalGatewayError", msg="en")
            #elif not is_ip_addr(input_data["dns1"]):
            #    ret = errcode.get_error_result("TerminalDns1Error", msg="en")
            elif len(input_data["name"]) == 0:
                ret = errcode.get_error_result("TerminalNameError", msg="en")
            elif len(input_data["platform"]) == 0:
                ret = errcode.get_error_result("TerminalPlatformError", msg="en")
            elif len(input_data["soft_version"]) == 0:
                ret = errcode.get_error_result("TerminalSoftVersionError", msg="en")
            elif input_data["setup_info"]["mode"]["show_desktop_type"] not in [0, 1, 2]:
                ret = errcode.get_error_result("TerminalModeTypeError", msg="en")
            elif input_data["setup_info"]["mode"]["auto_desktop"] < 0:
                ret = errcode.get_error_result("TerminalModeAutoDesktopError", msg="en")
            elif not is_ip_addr(input_data["setup_info"]["program"]["server_ip"]):
                ret = errcode.get_error_result("TerminalServerIpError", msg="en")
            elif input_data["conf_version"] < -2:
                ret = errcode.get_error_result("TerminalConfVersionError", msg="en")
            return ret
        except Exception as err:
            logger.error('err {}'.format(err))
            logger.error(''.join(traceback.format_exc()))
            ret = errcode.get_error_result("OtherError", msg="en")
        return ret

    def update_config_info(self, data):
        logger.debug("data: {}".format(data))
        request_data = data.get("data")
        resp = get_error_result("Success", msg="en")
        try:
            ret = self.check_config(request_data)
            if ret.get("code"):
                logger.debug("Return terminal: ret = {}".format(ret))
                return ret
            # get group_uuid
            group_uuid = None
            request_server_data = {'terminal_ip': request_data["ip"]}
            request_url = "/api/v1/voi/terminal/education/group"
            logger.debug("request yzy_server {}, {}".format(request_url, request_server_data))
            server_ret = self.http_client.post(request_url, request_server_data)
            logger.debug("get yzy_server return {}, {}".format(request_url, server_ret))
            if server_ret.get("code", -1) == 0:
                ret_data = server_ret.get('data', None)
                if ret_data:
                    group_uuid = ret_data['uuid']
            else:
                logger.error("return code: {}, message: {}".format(server_ret["code"], server_ret["msg"]))
            terminal_values = {
                'group_uuid': group_uuid,
                'terminal_id': request_data["terminal_id"],
                'mac': request_data["mac"],
                'ip': request_data["ip"],
                'mask': request_data["mask"],
                'gateway': request_data["gateway"],
                'dns1': request_data["dns1"],
                'dns2': request_data.get("dns2", ""),
                'is_dhcp': request_data["is_dhcp"],
                'name': request_data["name"],
                'platform': request_data["platform"],
                'soft_version': request_data["soft_version"],
                'register_time': dt.datetime.now(),
                'conf_version': request_data["conf_version"],
                'setup_info': json.dumps(request_data["setup_info"]),
                'disk_residue': request_data["disk_residue"]
            }
            terminal_update_values = terminal_values.copy()
            logger.debug(terminal_update_values)
            table_api = db_api.YzyVoiTerminalTableCtrl(current_app.db)
            qry = table_api.select_terminal_by_mac(request_data["mac"])
            update_group_uuid = group_uuid
            if qry:
                # if yzy_voi_terminal is not null, then need to check group valid
                if qry.group_uuid != group_uuid:
                    request_url = "/api/v1/voi/terminal/education/groups"
                    logger.debug("request yzy_server {}, {}".format(request_url, {}))
                    server_ret = self.http_client.post(request_url, {})
                    logger.debug("get yzy_server return {}, {}".format(request_url, server_ret))
                    if server_ret.get("code", -1) == 0:
                        ret_data = server_ret.get('data', None)
                        if ret_data and qry.group_uuid in ret_data['groups']:
                            terminal_update_values["group_uuid"] = qry.group_uuid
                            update_group_uuid = qry.group_uuid
                table_api.update_terminal_by_mac(**terminal_update_values)
            else:
                # table_api.add_terminal(terminal_values)
                logger.error("TerminalRecordNotExist: {}".format(request_data["mac"]))
                resp = errcode.get_error_result("TerminalRecordNotExist", msg="en")
                logger.debug("Return terminal: ret = {}".format(resp))
                return resp

            # create voi terminal desktops
            # if request_data['status'] == TerminalStatus.U_LINUX:
            request_server_data = {
                'group_uuid': update_group_uuid,
                'terminal_uuid': qry.uuid,
                'terminal_id': request_data["terminal_id"],
                'mac': request_data["mac"],
                'ip': request_data["ip"],
                'mask': request_data["mask"],
                'gateway': request_data["gateway"],
                'dns1': request_data["dns1"],
                'dns2': request_data.get("dns2", ""),
                'is_dhcp': request_data["is_dhcp"],
            }
            request_url = "/api/v1/voi/terminal/education/create_desktop_bind"
            logger.debug("request yzy_server {}, {}".format(request_url, request_server_data))
            server_ret = self.http_client.post(request_url, request_server_data)
            logger.debug("get yzy_server return {}, {}".format(request_url, server_ret))
            if server_ret.get("code", -1) != 0:
                resp = errcode.get_error_result("OtherError", msg="en")
            logger.debug("Return terminal: ret = {}".format(resp))
            return resp
        except Exception as err:
            logger.error('err {}'.format(err))
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result("OtherError", msg="en")
            logger.debug("Return terminal: ret = {}".format(resp))
            return resp

    def sync_desktop_info(self, data):
        """
        bt 上层客户端
        上传下载信息同步
        {
            "uuid": "f15a1759-789e-4e17-a3e1-e723121e9314",
            "sys_type":1,
            "name": "桌面名称",
            "desc": "描述",
            "disks": [
                {
                  "uuid":"91f9d1ba-cb4a-41ba-971a-618f9e306571",
                  "type":1,
                  "dif_level":1,
                  "prefix": "voi",
                  "real_size":8888888888
                },
                {
                  "uuid":"92f9d1ba-cb4a-41ba-971a-618f9e306571",
                  "type":1,
                  "dif_level":1,
                  "prefix": "voi",
                  "real_size":8888888888
                }
            ]
        }
        :param data:
        :return:
        """
        logger.debug("sync desktop info data: {}".format(data))
        request_data = data.get("data")
        try:
            request_url = "/api/v1/voi/template_disk/sync"
            logger.debug("request yzy_server {}, {}".format(request_url, request_data))
            server_ret = self.http_client.post(request_url, request_data)
            logger.debug("get yzy_server return {}, {}".format(request_url, server_ret))
            ret_code = server_ret.get("code", -1)
            if ret_code != 0:
                logger.error("request yzy_server sync_desktop_info return error: %s" % server_ret)
                msg = get_error_name(ret_code)
                server_ret["msg"] = msg
                return server_ret
            mac = request_data.get("mac")
            # 分发上传下载命令
            desktop = server_ret["data"]["desktop"]
            upload_disks = desktop.get("upload_disks")
            if upload_disks:
                logger.info("sync desktop info upload_disks : %s" % upload_disks)
                _desktop = copy.deepcopy(desktop)
                _desktop.pop("download_disks")
                _desktop.pop("disks")
                _desktop.pop("upload_disks")
                _desktop["disks"] = upload_disks
                # _desktop["tracker"] =
                # 上传
                send_data = {
                    "cmd": "upload_disk",
                    "data": {
                        "mac": mac,
                        "params":{
                            "batch_no": self.create_batch_no(),
                            "desktop": _desktop
                        }
                    }
                }
                msg = json.dumps(send_data)
                self.msg_center.public(msg)
            download_disks = desktop.get("download_disks")
            if download_disks:
                logger.info("sync desktop info download_disks : %s"% download_disks)
                # 需下载的磁盘
                # todo 提交bt服务，创建下载任务
                _desktop = copy.deepcopy(desktop)
                _desktop.pop("download_disks")
                _desktop.pop("disks")
                _desktop.pop("upload_disks")
                _desktop["disks"] = download_disks
                # 上传
                send_data = {
                    "cmd": "send_torrent",
                    "data": {
                        "mac": mac,
                        "batch_no": self.create_batch_no(),
                        "desktop": _desktop
                    }
                }
                msg = json.dumps(send_data)
                self.msg_center.public(msg)

            logger.info("sync desktop info command send success!!!")
            return errcode.get_error_result("Success")
        except Exception as err:
            logger.error('err {}'.format(err))
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
            return resp

    def upload_desktop_info(self, data):
        """ bt 上层客户端
            获取当前桌面信息
        {
            "boot_disk": "voi_0_92f9d1ba-cb4a-41ba-971a-618f9e306571"
        }
        """
        logger.debug("data: {}".format(data))
        request_data = data.get("data")
        try:
            request_url = "/api/v1/voi/template_disk/desktop"
            logger.debug("request yzy_server {}, {}".format(request_url, request_data))
            server_ret = self.http_client.post(request_url, request_data)
            logger.debug("get yzy_server return {}, {}".format(request_url, server_ret))
            ret_code = server_ret.get("code", -1)
            if ret_code != 0:
                logger.error("request yzy_server upload_desktop_info return error: %s"% server_ret)
            msg = get_error_name(ret_code)
            server_ret["msg"] = msg
            return server_ret
        except Exception as err:
            logger.error('err {}'.format(err))
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
        return resp

    def get_desktop_info(self, data):
        """ bt 上层客户端
            获取当前桌面信息
        {
            "boot_disk": "voi_0_92f9d1ba-cb4a-41ba-971a-618f9e306571"
        }
        """
        logger.debug("get desktop info data: {}".format(data))
        request_data = data.get("data")
        try:
            boot_disk = request_data["boot_disk"]
            _data = {
                "uuid": boot_disk.split("_")[-1]
            }
            request_url = "/api/v1/voi/template_disk/desktop"
            logger.debug("request yzy_server {}, {}".format(request_url, _data))
            server_ret = self.http_client.post(request_url, _data)
            logger.debug("get desktop info yzy_server return {}, {}".format(request_url, server_ret))
            ret_code = server_ret.get("code", -1)
            if ret_code != 0:
                logger.error("request yzy_server get_desktop_info return error: %s"% server_ret)
            msg = get_error_name(ret_code)
            server_ret["msg"] = msg
            return server_ret
        except Exception as err:
            logger.error('err {}'.format(err))
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
        return resp

    def get_desktop_group_list(self, data):
        logger.debug("data: {}".format(data))
        request_data = data.get("data")
        mac = request_data["mac"]
        ip = request_data["ip"]
        resp = get_error_result("Success", msg="en")
        desktop_group_list = []
        if not len(request_data["mac"]):
            logger.error("request parameter error")
            resp = get_error_result("MessageError", msg='en')
            return resp
        # verify mac and get id and ip, if not exists return directly
        try:
            table_api = db_api.YzyVoiTerminalTableCtrl(current_app.db)
            qry = table_api.select_terminal_by_mac(mac)
            if qry:
                logger.debug("qry.mac {}, qry.ip {}".format(qry.mac, qry.ip))
                server_ret = {}
                # classroom scene
                request_data = {
                    "terminal_id": qry.terminal_id,
                    "terminal_ip": qry.ip,
                    "group_uuid": qry.group_uuid,
                    "terminal_uuid": qry.uuid
                }
                request_url = "/api/v1/voi/template_disk/list"
                logger.debug("request yzy_server {}, {}".format(request_url, request_data))
                server_ret = self.http_client.post(request_url, request_data)
                logger.debug("get yzy_server {} {},".format(request_url, server_ret))
                ret_code = server_ret.get("code", -1)
                if ret_code != 0:
                    msg = get_error_name(ret_code)
                    resp["code"] = ret_code
                    resp["msg"] = msg
                    return resp
                else:
                    # add desktop ip info
                    ret_data = server_ret.get('data', {})
                    if ret_data:
                        for desktop_group in ret_data['desktop_group_list']:
                            if desktop_group['desktop_enable_bottom_ip']:
                                desktop_group["desktop_is_dhcp"] = int(qry.is_dhcp)
                                desktop_group["desktop_ip"] = qry.ip
                                desktop_group["desktop_mask"] = qry.mask
                                desktop_group["desktop_gateway"] = qry.gateway
                                desktop_group["desktop_dns1"] = qry.dns1
                                desktop_group["desktop_dns2"] = qry.dns2
                                logger.debug("desktop_group: {} set bottom ip".format(
                                    desktop_group['desktop_group_uuid']))
                            desktop_group.pop('desktop_enable_bottom_ip')
                    resp["data"] = ret_data
                    logger.debug("Return terminal: {}".format(resp))
                    return resp
            else:
                resp = get_error_result("TerminalRecordNotExist", msg='en')
                return resp
        except Exception as err:
            logger.error(err)
            logger.error(''.join(traceback.format_exc()))
            resp = get_error_result("OtherError", msg='en')
            return resp


    def verify_admin_user(self, data):
        logger.debug("data: {}".format(data))
        request_data = data.get("data")
        resp = get_error_result("Success", msg="en")
        try:
            username = request_data["username"]
            password = request_data["password"]
            mac = request_data["mac"]
            table_api = db_api.YzyAdminUserTableCtrl(current_app.db)
            obj = table_api.select_by_username(username)
            if not obj or (create_md5(password) != obj.password):
                resp = errcode.get_error_result("UserOrPasswordError", msg="en")
            logger.debug("Return terminal: ret = {}".format(resp))
            return resp
        except Exception as err:
            logger.error(err)
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result("OtherError", msg="en")
            logger.debug("Return terminal: {}".format(resp))
            return resp

    # useless maybe
    def order_confirm(self, data):
        logger.debug("data: {}".format(data))
        request_data = data.get("data")
        mac = request_data["mac"]
        batch_no = request_data["batch_no"]
        resp = get_error_result("Success", msg="en")
        try:
            # from mac get group_uuid
            table_api = db_api.YzyVoiTerminalTableCtrl(current_app.db)
            qry = table_api.select_terminal_by_mac(mac)
            if not qry:
                logger.debug("Mac not in yzy_voi_terminal, Return terminal error")
                resp = get_error_result("TerminalNotLogin", msg="en")
                return resp

            cmd_name = data.get("data").get("service_name")
            with redis_lock.Lock(self.rds, '{}_lock'.format(cmd_name), 2):
                # 1. search batch_num, mac
                if self.rds.ping_server():
                    redis_key = 'voi_command:order:{}:{}'.format(qry.group_uuid, batch_no)
                    confirm_num = str(request_data['terminal_id'])
                    json_data = self.rds.get(redis_key)
                    if json_data:
                        data_dict = json.loads(json_data)
                        macs = data_dict['order_macs'].split(',')
                        confirm_macs = [] if 0 == len(data_dict['confirm_macs']) else data_dict['confirm_macs'].split(',')
                        confirm_ids = [] if 0 == len(data_dict['confirm_ids']) else data_dict['confirm_ids'].split(',')
                        if int(confirm_num) < data_dict['start_id']:
                            logger.debug(
                                'order confirm_num {} little than start_id'.format(confirm_num, data_dict['start_id']))
                            resp = get_error_result("TerminalOrderIdLittleStartId", msg="en")
                        elif mac not in macs:
                            logger.debug('mac {} not in order session macs {}'.format(mac, macs))
                            resp = get_error_result("TerminalOrderMacError", msg="en")
                        elif confirm_num in confirm_ids:
                            logger.debug('mac already ordered {}'.format(mac))
                            resp = get_error_result("TerminalAlreadyOrdered", msg="en")
                        else:
                            macs.remove(mac)
                            confirm_macs.append(mac)
                            confirm_ids.append(confirm_num)
                            data_dict['order_macs'] = ','.join(macs)
                            data_dict['confirm_macs'] = ','.join(confirm_macs)
                            data_dict['confirm_ids'] = ','.join(confirm_ids)
                            data_dict['current_id'] = int(confirm_num) + 1
                            self.rds.set(redis_key, json.dumps(data_dict))
                            logger.debug(
                                "confirm mac = {} , id = {} now redis data = {}".format(mac, confirm_num, data_dict))
                            # send order to other macs
                            # next_terminal_id = data_dict['start_id']
                            next_terminal_id = data_dict['current_id']
                            while str(next_terminal_id) in confirm_ids:
                                next_terminal_id += 1
                            for mac_name in macs:
                                # redis add a record to save order session for order next id
                                send_data = {
                                    "cmd": "order",
                                    "data": {
                                        "mac": mac_name,
                                        "params": {
                                            "batch_no": batch_no,
                                            "terminal_id": next_terminal_id
                                        }
                                    }
                                }
                                msg = json.dumps(send_data)
                                self.msg_center.public(msg)
                    else:
                        logger.error('Redis no key {}'.format(redis_key))
                        resp = get_error_result("OtherError", msg="en")
                else:
                    logger.error('Redis server error')
                    resp = get_error_result("OtherError", msg="en")
                return resp
        except Exception as err:
            logger.error('err {}'.format(err))
            logger.error(''.join(traceback.format_exc()))
            resp = get_error_result("OtherError", msg="en")
            return resp

    def order_query(self, data):
        logger.debug("data: {}".format(data))
        request_data = data.get("data")
        mac = request_data["mac"]
        terminal_id = -1
        batch_no = 0
        resp = get_error_result("Success", msg="en")
        # 1. search redis keys like "command:order:*"
        # 2. search "order_macs"
        # 3. return current_id
        try:
            # from mac get group_uuid
            table_api = db_api.YzyVoiTerminalTableCtrl(current_app.db)
            qry = table_api.select_terminal_by_mac(mac)
            if not qry:
                resp["data"] = {}
                resp["data"]["batch_no"] = 0
                resp["data"]["terminal_id"] = -1
                logger.debug("Mac not in yzy_voi_terminal, Return terminal: {}".format(resp))
                return resp
            if self.rds.ping_server():
                redis_key = 'voi_command:order:{}:*'.format(qry.group_uuid)
                redis_keys = self.rds.keys(redis_key)
                batch_no = max([int(key.decode().split(':')[-1]) for key in redis_keys]) if redis_keys else 0
                key = 'voi_command:order:{}:{}'.format(qry.group_uuid, batch_no)
                if batch_no:
                    json_data = self.rds.get(key)
                    data_dict = json.loads(json_data)
                    logger.debug("order_macs = {}".format(data_dict['order_macs']))
                    if mac in data_dict['order_macs']:
                        confirm_ids = [] if 0 == len(data_dict['confirm_ids']) else data_dict['confirm_ids'].split(',')
                        terminal_id = data_dict['current_id']
                        logger.debug("batch_no: {} current_id: {}".format(batch_no, terminal_id))
            else:
                logger.error('Redis server error')
                resp = get_error_result("OtherError", msg="en")
        except Exception as err:
            logger.error('err {}'.format(err))
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
        resp["data"] = {}
        resp["data"]["batch_no"] = batch_no
        resp["data"]["terminal_id"] = terminal_id
        return resp

    def terminal_report_desktop(self, data):
        """ 终端上报桌面更新消息
            {
                "mac": "xxxxxx",
                "ip": "xxxxxx",
                "desktop_uuid": "xxxxxxxxxxxxx"
            }
        """
        logger.debug("terminal report desktop: {}".format(data))
        resp = errcode.get_error_result("Success", msg="en")
        request_data = data.get("data")  # include status of terminal type
        try:
            mac = request_data.get("mac")
            table_api = db_api.YzyVoiTerminalTableCtrl(current_app.db)
            qry = table_api.select_terminal_by_mac(mac)
            if qry:
                # table_api.update_terminal_by_mac(**insert_data)
                # logger.debug('mac: {} set online'.format(insert_data['mac']))
                data = {
                    "terminal_uuid":  qry.uuid,
                    "desktop_uuid": request_data["desktop_uuid"]
                }
                request_url = "/voi/terminal/education/desktop_bind"
                logger.debug("request yzy_server {}, {}".format(request_url, request_data))
                server_ret = self.http_client.post(request_url, request_data)
                logger.debug("get yzy_server {} {},".format(request_url, server_ret))
                ret_code = server_ret.get("code", -1)
                if ret_code != 0:
                    msg = get_error_name(ret_code)
                    resp["code"] = ret_code
                    resp["msg"] = msg
                    return resp

            else:
                resp = get_error_result("TerminalRecordNotExist", msg='en')
                return resp
            resp["data"] = {}
            resp["data"]["token"] = self.get_md5(ip_port)
            return resp
        except Exception as err:
            logger.error(err)
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
            return resp

    def send_desktop_callback(self, mac, data):
        """
        下发桌面回调
        :param data:
        :return:
        """
        logger.info("mac %s send desktop callback: %s" % (mac, data))
        table_api = db_api.YzyVoiTerminalTableCtrl(current_app.db)
        terminal = table_api.select_terminal_by_mac(mac)
        if not terminal:
            logger.error("send desktop callback error: %s terminal not exist"% mac)
            return

        desktop = data.get("desktop", {})
        # todo 下发种子， 提交bt服务，记录bt任务
        logger.info("send torrent desktop: {}  mac: {}".format(desktop, mac))
        disks = desktop.get("disks", [])
        for disk in disks:
            torrent_file = disk.get("torrent_file", "")
            if not os.path.exists(torrent_file):
                logger.error("do send torrent file not exist: %s, mac: %s"% (torrent_file, mac))
                continue
            params = dict()
            params["uuid"]= disk["uuid"]
            params["type"] =  disk["type"]
            params["sys_type"] = desktop["os_sys_type"]
            params["dif_level"] = disk["dif_level"]
            params["real_size"] = disk["real_size"]
            params["reserve_size"] = disk["reserve_size"]
            params["torrent_file"] = disk["torrent_file"]
            # 调bt服务添加任务
            save_path = os.path.dirname(params["torrent_file"])
            ret = current_app.bt_api.add_bt_task(params["torrent_file"], save_path)
            if ret["code"] != 0:
                logger.error("bt server add task fail:%s"% params)
                continue
            logger.info('mac: {} add bt task api return {}'.format(mac, ret))
            torrent_id = ret["torrent_id"]

            # torrent_id = "%s"% random.randint(1, 100000000)
            send_data = {
                "cmd" : "send_torrent",
                "data": {
                    "mac": mac,
                    "params": params
                }
            }

            torrent_file = params["torrent_file"]
            disk_name = "voi_%s_%s"% (params["dif_level"], params["uuid"])
            task_uuid = create_uuid()
            task_values = {
                "uuid": task_uuid,
                "torrent_id": torrent_id,
                "torrent_name": os.path.basename(torrent_file),
                "torrent_path": torrent_file,
                "torrent_size": str(os.path.getsize(torrent_file)),
                "template_uuid": desktop["template_uuid"],
                "disk_uuid": disk["uuid"],
                "disk_name": disk_name,
                "terminal_mac": mac,
                "terminal_ip": terminal.ip,
                "type": constants.BT_DOWNLOAD_TASK,
                "status": 0,
                "process": 0,
                "download_rate": 0
            }
            # 计入任务队列
            # 判断是否已经存在任务
            logger.info("mac %s do send torrent task is exist or not ???"% mac)
            task_api = db_api.YzyVoiTorrentTaskTableCtrl(current_app.db)
            task = task_api.select_task_by_torrent_id(torrent_id)
            if not task:
                task_api.add_task(task_values)
            # 进入消息队列
            msg = json.dumps(send_data)
            self.msg_center.public(msg)
            logger.info("send desktop callback push msg success: %s"% msg)

    def command_response(self, data):
        logger.debug('{}.{} be called'.format(self.__class__.__name__, sys._getframe().f_code.co_name))
        logger.debug("command_response: {}".format(data))
        resp = errcode.get_error_result("Success", msg="en")
        cmd_name = data.get("data").get("service_name")
        ignore_cmds = ["order"]
        if cmd_name in ignore_cmds:
            logger.debug("need not handle response message: {}".format(ignore_cmds))
            return resp
        try:
            if data.get("code"):
                logger.error("terminal return error: {}-{}}}}".format(data.get("code"), data.get("msg")))
                return resp
            response_data = data.get("data").get("data")
            batch_no = response_data["batch_no"]
            mac = response_data["mac"]
            # get redis original message
            if self.rds.ping_server():
                with redis_lock.Lock(self.rds, '{}_lock'.format(cmd_name), 2):
                    redis_key = 'voi_command:{}:{}'.format(cmd_name, batch_no)
                    logger.debug("redis_key: {}".format(redis_key))
                    redis_data = self.rds.get(redis_key).decode('utf-8')
                    data_dict = json.loads(redis_data)
                    confirm_macs = [] if 0 == len(data_dict['confirm_macs']) else data_dict['confirm_macs'].split(',')
                    confirm_macs.append(mac)
                    data_dict["confirm_macs"] = ','.join(confirm_macs)
                    self.rds.set(redis_key, json.dumps(data_dict))
                callback = "%s_callback" % cmd_name
                if hasattr(self, callback) and data_dict.get("params"):
                    func = getattr(self, callback)
                    func(mac, data_dict["params"])
            else:
                logger.error('redis ping err, please check redis service!!!')

        except Exception as err:
            logger.error('err {}'.format(err))
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
        return resp

    def get_template_list(self, data):
        pass

    def torrent_upload(self, data):
        """
        上传种子
        {
            "cmd": "upload_torrent",
            "data":
                {
                     "mac": "00:50:56:C0:00:08",
                     "template_uuid": "f15a1759-789e-4e17-a3e1-e723121e9314",
                     "template_name": "voi_test1",
                     "disk_name": "xxxxxxx",
                     "torrent_name": "xxxx",
                     "torrent_size": 10234,
                     "torrent_path": "xxxxx"
                }
        }
        :param data:
        :return:
        """
        logger.info("client upload template torrent file: %s" % data["cmd"])
        # 保存种子
        try:
            _data = data.get("data")
            torrent_base64 = _data["payload"]

            # torrent_dir = constants.DEFAULT_SYS_PATH
            # torrent_dir = constants.DEFAULT_SYS_PATH
            torrent_bin = base64.b64decode(torrent_base64.encode("utf-8"))
            torrent_file = YzyTorrentStruct().save(torrent_bin, "/opt/slow/instances/_base/")
            # 添加上传任务
            save_path = torrent_file.replace(".torrent", "")
            ret = current_app.bt_api.add_bt_task(torrent_file, save_path)
            if ret["code"] != 0:
                logger.error("bt server add task fail:%s , %s", torrent_file, save_path)
                return get_error_result("TerminalTorrentUploadFail", msg="en")

            resp = get_error_result("Success", msg="en")
            logger.info("client upload template torrent file success!!!!")
            return resp
        except Exception as err:
            logger.error('err {}'.format(err))
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
        return resp

    def init_desktop(self, data):
        """
        {
            "cmd": "init_desktop",
            "data": {
                "mac": "xxxxx-xxxxxx"
            }
        }
        :param data:
        :return:
        """
        logger.debug("data: {}".format(data))
        request_data = data.get("data")
        try:
            request_url = "/api/v1/voi/template_disk/init"
            logger.debug("request yzy_server init desktop info {}, {}".format(request_url, request_data))
            server_ret = self.http_client.post(request_url, request_data)
            logger.debug("get yzy_server return {}, {}".format(request_url, server_ret))
            ret_code = server_ret.get("code", -1)
            if ret_code != 0:
                logger.error("request yzy_server init_desktop_info return error: %s" % server_ret)
            msg = get_error_name(ret_code)
            server_ret["msg"] = msg
            return server_ret
        except Exception as err:
            logger.error('err {}'.format(err))
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
        return resp

    def win_login(self, data):
        """
        {
            "cmd": "win_login",
            "data": {
                "username": "user1",
                "password": "xxxx"
            }
        }
        :param data:
        :return:
        """
        logger.debug("win_login data: {}".format(data))
        request_data = data.get("data")
        try:
            request_url = "/api/v1/voi/template_disk/init"
            logger.debug("request yzy_server init desktop info {}, {}".format(request_url, request_data))
            server_ret = self.http_client.post(request_url, request_data)
            logger.debug("get yzy_server return {}, {}".format(request_url, server_ret))
            ret_code = server_ret.get("code", -1)
            if ret_code != 0:
                logger.error("request yzy_server init_desktop_info return error: %s" % server_ret)
            msg = get_error_name(ret_code)
            server_ret["msg"] = msg
            return server_ret
        except Exception as err:
            logger.error('err {}'.format(err))
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
        return resp

    def bt_tracker(self, data):
        logger.debug("bt_tracker data: {}".format(data))
        resp = errcode.get_error_result("Success", msg="en")
        try:
            image_ip = get_controller_image_ip()
            bt_port = constants.BT_FILE_TRANS_PORT
            tracker_list = list()
            tracker = "http://%s:%s/announce" % (image_ip, bt_port)
            tracker_list.append(tracker)
            resp["data"]  = {"tracker": tracker_list}
            return resp
        except Exception as err:
            logger.error(err)
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
            return resp

    def check_upload_state(self, data):
        logger.debug("check_upload_state data: {}".format(data))
        request_data = data.get("data", None)
        resp = errcode.get_error_result("Success", msg="en")
        try:
            desktop_group_uuid = request_data.get("desktop_group_uuid", "")
            mac = request_data['mac']
            if not (mac and desktop_group_uuid):
                resp = errcode.get_error_result("MessageError", msg="en")
                return resp
            table_api = db_api.YzyVoiTerminalTableCtrl(current_app.db)
            qry = table_api.select_terminal_by_mac(mac)
            if qry:
                request_server_data = {
                    "desktop_group_uuid": desktop_group_uuid,
                }
                request_url = "/api/v1/voi/template/check_upload_state"
                logger.debug("request yzy_server {}, {}".format(request_url, request_server_data))
                server_ret = self.http_client.post(request_url, request_server_data)
                logger.debug("get yzy_server return {}, {}".format(request_url, server_ret))
                ret_code = server_ret.get("code", -1)
                if ret_code != 0:
                    logger.error("request yzy_server check_upload_state return error: %s" % server_ret)
                server_ret["msg"] = errcode.get_error_name(ret_code)
                logger.debug("Return terminal: server_ret = {}".format(server_ret))
                return server_ret
            else:
                logger.error("TerminalRecordNotExist: {}".format(mac))
                resp = errcode.get_error_result("TerminalRecordNotExist", msg="en")
                logger.debug("Return terminal: resp = {}".format(resp))
                return resp
        except Exception as err:
            logger.error(err)
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
            return resp

    def task_result(self, data):
        logger.debug("task_result data: {}".format(data))
        resp = errcode.get_error_result("Success", msg="en")
        try:
            # resp["data"] = {
            #     "mac": "223333333",
            #     "file_size": "2342334",
            #     "file_name": "file_name234234",
            # }
            
            return resp
        except Exception as err:
            logger.error(err)
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
        return resp

    def p_to_v_start(self, data):
        """
        {
                "mac": "AA:50:CC:C0:DD:08",
                "name": "ysr_template",
                "desc": "add qq soft",
                "classify": 1, # 1-education 2-personal
                "system_disk": {
                        "size": 100, # size unit GB
                        "real_size": 8.5
                },
                "data_disks": [
                        {
                                "size": 100,
                                "read_size": 8.5
                        },
                        {
                                "size": 100,
                                "read_size": 8.5
                        }
                ]
        }

        * return:
          {
              "code": 0,
              "msg": "Success",
              "data": {
                   "image_names": "voi_0_92f9d1ba-cb4a-41ba-971a-618f9e306571,voi_0_88f9d1ba-cb4a-41ba-971a-618f9e306571,voi_0_99f9d1ba-cb4a-41ba-971a-618f9e306571",
                   "user": "root",
                   "password": "123qwe,.",
                   "storage": "opt"
               }
          }

        """
        logger.debug("data: {}".format(data))
        request_data = data.get("data")
        resp = errcode.get_error_result("Success", msg="en")
        pool_name = "template-voi"
        try:
            _data = request_data.copy()
            _data.pop('mac')
            _data["pool_name"] = pool_name
            request_url = "/api/v1/voi/template/start_upload"
            logger.debug("request yzy_server {}, {}".format(request_url, _data))
            server_ret = self.http_client.post(request_url, _data)
            logger.debug("get yzy_server return {}, {}".format(request_url, server_ret))
            ret_code = server_ret.get("code", -1)
            if ret_code != 0:
                logger.error("request yzy_server start_upload return error: {}".format(server_ret))
                resp["msg"] = errcode.get_error_name(ret_code)
                resp["code"] = ret_code
                return resp
            sys_uuid = server_ret.get("data").get("system_disk").get("uuid")
            data_uuids = []
            if server_ret.get("data").get("data_disks"):
                data_uuids = [x['uuid'] for x in server_ret.get("data").get("data_disks")]
            data_uuids.insert(0, sys_uuid)
            #user = "voi_guest"
            #password = "qwe123,."
            user = "root"
            password = "123qwe,."
            resp["data"] = {
                "user": user,
                "password": password,
                "storage": pool_name
            }
            resp["data"]["image_names"] = data_uuids
            logger.debug("sys_uudi: {}, data_uuids: {}".format(sys_uuid, data_uuids))
            # check voi_guest user
            
            #if not authenticate(user, password, 'system-auth'):
            #    ret = subprocess.run("adduser -m {}".format(user), shell=True)
            #    logger.debug("adduser {} return: {}".format(user, ret.returncode))
            #    ret = subprocess.run("echo {}:{} | chpasswd".format(user, password), shell=True)
            #    logger.debug("chpasswd {} return: {}".format(password, ret.returncode))
            return resp
        except Exception as err:
            logger.error('err {}'.format(err))
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
            return resp

    def p_to_v_state(self, data):
        """
        {
                "os_type": "windows_7_x64",  # "windows_10_x64" "windows_7" "windows_10" "other"
                "image_name": "92f9d1ba-cb4a-41ba-971a-618f9e306571"
                "progress": 11,
                "status": 1,
                "mac": "AA:50:CC:C0:DD:08",
                "storage": "opt",
        }

        * return:
          {
              "code": 0,
              "msg": "Success"
          }
        """
        logger.debug("data: {}".format(data))
        request_data = data.get("data")
        resp = errcode.get_error_result("Success", msg="en")
        try:
            _data = {}
            _data["uuid"] = request_data["image_name"].split('_')[-1]
            _data["progress"] = request_data["progress"]
            _data["os_type"] = request_data["os_type"]
            _data["status"] = request_data["status"]
            if not request_data["status"] or request_data["progress"] == 100:
                request_url = "/api/v1/voi/template/upload_end"
                logger.debug("request yzy_server {}, {}".format(request_url, _data))
                server_ret = self.http_client.post(request_url, _data)
                logger.debug("get yzy_server return {}, {}".format(request_url, server_ret))
                ret_code = server_ret.get("code", -1)
                if ret_code != 0:
                    logger.error("request yzy_server get_desktop_info return error: %s" % server_ret)
                    resp["msg"] = errcode.get_error_name(ret_code)
                    resp["code"] = ret_code
                    return resp
            return resp
        except Exception as err:
            logger.error('err {}'.format(err))
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
            return resp

    def diff_disk_upload(self, data):
        """
        {
                "mac": "AA:50:CC:C0:DD:08",
                "desktop_group_uuid": "xxxxxxxxxxxxxxxxx",
                "diff_disk_uuid": "xxxxxxxxxxxxxxxxx",
                "diff_level": 3
        * return:
          {
              "code": 0,
              "msg": "Success"
          }
        """
        logger.debug("diff disk upload data: {}".format(data))
        request_data = data.get("data")
        resp = errcode.get_error_result("Success", msg="en")
        try:
            request_url = "/api/v1/voi/terminal_disk/upload"
            logger.debug("request yzy_server {}, {}".format(request_url, data))
            server_ret = self.http_client.post(request_url, data)
            logger.debug("diff disk upload yzy_server return {}, {}".format(request_url, server_ret))
            ret_code = server_ret.get("code", -1)
            if ret_code != 0:
                logger.error("request yzy_server get_desktop_info return error: %s" % server_ret)
                resp["msg"] = errcode.get_error_name(ret_code)
                resp["code"] = ret_code
                return resp
        except Exception as err:
            logger.error('err {}'.format(err))
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
            return resp

    def diff_disk_download(self, data):
        """
        {
            "mac": "AA:50:CC:C0:DD:08",
            "desktop_group_uuid": "92f9d1ba-cb4a-41ba-971a-2222222222",
            "diff_disk_uuid": "92f9d1ba-cb4a-41ba-971a-618f9e306571",
            "diff_level": 3
        }

        * return:
          {
              "code": 0,
              "msg": "Success"
          }
        """
        logger.debug("data: {}".format(data))
        try:
            resp = errcode.get_error_result("Success", msg="en")
            request_data = data.get("data")
            mac = request_data.get("mac", None)
            desktop_group_uuid = request_data.get("desktop_group_uuid", None)
            diff_disk_uuid = request_data.get("diff_disk_uuid", None)
            diff_level = request_data.get("diff_level", None)
            if not (mac and desktop_group_uuid and diff_disk_uuid):
                return errcode.get_error_result("MessageError", msg='en')
            table_api = db_api.YzyVoiTerminalTableCtrl(current_app.db)
            terminal = table_api.select_terminal_by_mac(mac)
            if not terminal:
                logger.error("%s terminal yzy_voi_terminal record not exist" % mac)
                resp = errcode.get_error_result("TerminalRecordNotExist", msg="en")
                return resp
            # check diff_disk info, get torrent info
            _data = {
                "desktop_group_uuid": desktop_group_uuid,
                "diff_disk_uuid": diff_disk_uuid,
                "diff_level": diff_level
            }
            request_url = "/api/v1/voi/template_disk/download"
            logger.debug("request yzy_server {}, {}".format(request_url, _data))
            server_ret = self.http_client.post(request_url, _data)
            logger.debug("get_torrent_info yzy_server return {}, {}".format(request_url, server_ret))
            ret_code = server_ret.get("code", -1)
            server_ret_data = server_ret.get("data", None)
            if ret_code != 0 or not server_ret_data:
                logger.error("request yzy_server download return error: {}".format(server_ret))
                resp["msg"] = errcode.get_error_name(ret_code)
                resp["code"] = ret_code
                return resp

            params = dict()
            params["uuid"] = diff_disk_uuid
            params["type"] = server_ret_data.get("diff_disk_type", "")
            params["sys_type"] = server_ret_data.get("os_sys_type", 0)
            params["dif_level"] = diff_level
            params["real_size"] = server_ret_data.get("real_size", 0)
            params["reserve_size"] = server_ret_data.get("reserve_size", 0)
            params["torrent_file"] = server_ret_data.get("torrent_file", "")
            save_path = os.path.dirname(params["torrent_file"])
            logger.info('add bt task api request: {}, {}'.format(params["torrent_file"], save_path))
            ret = current_app.bt_api.add_bt_task(params["torrent_file"], save_path)
            logger.info('add bt task api return {}'.format(ret))
            if ret["code"] != 0:
                logger.error("bt server add task fail:%s" % params)
                resp = errcode.get_error_result("TerminalAddBtTaskError", msg="en")
                return resp
            torrent_id = ret["torrent_id"]

            # torrent_id = "%s"% random.randint(1, 100000000)
            send_data = {
                "cmd": "send_torrent",
                "data": {
                    "mac": mac,
                    "params": params
                }
            }

            torrent_file = params["torrent_file"]
            disk_name = "voi_%s_%s" % (params["dif_level"], params["uuid"])
            task_uuid = create_uuid()
            task_values = {
                "uuid": task_uuid,
                "torrent_id": torrent_id,
                "torrent_name": os.path.basename(torrent_file),
                "torrent_path": torrent_file,
                "torrent_size": str(os.path.getsize(torrent_file)),
                "template_uuid": server_ret_data.get("template_uuid", ""),
                "disk_uuid": diff_disk_uuid,
                "disk_name": disk_name,
                "terminal_mac": mac,
                "terminal_ip": terminal.ip,
                "type": constants.BT_DOWNLOAD_TASK,
                "status": 0,
                "process": 0,
                "download_rate": 0
            }
            task_api = db_api.YzyVoiTorrentTaskTableCtrl(current_app.db)
            task = task_api.select_task_by_torrent_id(torrent_id)
            if not task:
                task_api.add_task(task_values)
            msg = json.dumps(send_data)
            self.msg_center.public(msg)
            return resp
        except Exception as err:
            logger.error('err {}'.format(err))
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
            return resp

    def desktop_login(self, data):
        logger.debug("desktop login data: {}".format(data))
        resp = errcode.get_error_result("Success", msg="en")
        desktop_info = data.get("data")  # include status of terminal type
        try:
            table_api = db_api.YzyVoiTerminalTableCtrl(current_app.db)
            qry = table_api.select_terminal_by_mac(desktop_info['mac'])
            if qry:
                request_server_data = {
                    "cmd": "login",
                }
                request_server_data.update(desktop_info)
                request_url = "/api/v1/voi/terminal/education/update_desktop_bind"
                logger.debug("request yzy_server {}, {}".format(request_url, request_server_data))
                server_ret = self.http_client.post(request_url, request_server_data)
                logger.debug("get yzy_server return {}, {}".format(request_url, server_ret))
                ret_code = server_ret.get("code", -1)
                if ret_code != 0:
                    logger.error("request yzy_server update_desktop_bind return error: %s" % server_ret)
                    resp["msg"] = errcode.get_error_name(ret_code)
                    resp["code"] = ret_code
            else:
                logger.error("TerminalRecordNotExist: {}".format(desktop_info['mac']))
                resp = errcode.get_error_result("TerminalRecordNotExist", msg="en")
            logger.debug("Return terminal: resp = {}".format(resp))
            return resp
        except Exception as err:
            logger.error(err)
            logger.error(''.join(traceback.format_exc()))
            resp = errcode.get_error_result(error="OtherError", msg="en")
            return resp
