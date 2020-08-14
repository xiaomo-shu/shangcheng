# -*- coding: utf-8 -*-
from copy import deepcopy


ERROR_CODE = {
    "Success": {"code": 0, "msg": "成功"},
    # 10001 ~ 10999 WEB层错误码
    "LoginFailError": {"code": 10001, "msg": "用户名或密码错误"},
    "UsernameError": {"code": 10002, "msg": "用户名错误"},
    "UpdateNoChangeError": {"code": 10003, "msg": "修改{param}值相同"},
    "NetworkInterfaceNotExist": {"code": 10004, "msg": "节点{node}网络接口{interface}不存在"},
    "NotPasswordInputError": {"code": 10005, "msg": "请输入管理员密码"},
    "BaseImageFileError": {"code": 10006, "msg": "基础镜像文件异常"},
    "BaseImageMd5Error": {"code": 10007, "msg": "基础镜像文件MD5校验失败"},
    "BaseImageSaveError": {"code": 10008, "msg": "基础镜像文件保存失败"},
    "BaseImageNameRepeatError": {"code": 10009, "msg": "基础镜像名称重复"},
    "BaseImageOsTypeError": {"code": 10010, "msg": "基础镜像系统类型错误"},
    "ISOFileUploadError": {"code": 10011, "msg": "ISO文件上传失败"},
    "ISOFileExistError": {"code": 10012, "msg": "ISO文件已存在"},
    "ISOFileNotExistError": {"code": 10012, "msg": "ISO文件不存在"},
    "ISOFileUpdateError": {"code": 10012, "msg": "ISO文件更新失败"},
    "NetworkIpInfoError": {"code": 10013, "msg": "IP信息异常"},
    "NetworkIpMuchError": {"code": 10014, "msg": "网卡IP超出数量"},
    "PasswordCheckError": {"code": 10015, "msg": "密码校验失败"},
    "AdminUsernameExist": {"code": 10016, "msg": "管理员账号已存在"},
    "AdminUserNotExist": {"code": 10017, "msg": "管理员账号不存在"},
    "EndIPLessThanStartIP": {"code": 10018, "msg": "结束IP不能小于开始IP并且要在同一网段"},
    "GatewayAndIpError" : {"code": 10019, "msg": "ip和网关不在同一网段"},
    "SubnetMaskError": {"code": 10020, "msg": "子网掩码不正确"},
    "ParameterError": {"code": 10021, "msg": "参数错误"},
    "CreateGroupError": {"code": 10022, "msg": "添加失败，分组最多只能创建50个"},
    "IpAddressError": {"code": 10023, "msg": "请输入正确的ip地址"},
    "DnsAddressError": {"code": 10024, "msg": "请输入正确的dns地址"},
    "GatewayError": {"code": 10025, "msg": "请输入正确的网关"},
    "IpAddressSegmentError": {"code": 10026, "msg": "输入的起始ip不在所选择终端预设ip段"},
    "IpResourcesError": {"code": 10027, "msg": "可用ip资源数不足"},
    "TerminalGroupError": {"code": 10028, "msg": "该分组下没有终端"},
    "IpAddressGatewayDnsAddressError": {"code": 10029, "msg": "ip、dns或子网掩码不正确"},
    "LocalNetworkIpAddressError": {"code": 10030, "msg": "不同网卡不能存在相同网段的IP"},
    "BaseImageUpdateError": {"code": 10031, "msg": "基础镜像更新错误"},
    "StaticIPTypeWithoutIPAddress": {"code": 10032, "msg": "已选择IP类型为固定IP，请输入IP地址"},
    "RebootServiceTimeout": {"code": 10033, "msg": "{name}服务重启超时"},
    "VoiShareDiskNotExist": {"code": 10034, "msg": "共享数据盘不存在"},
    "SuperAdminNotDeleteError": {"code": 10035, "msg": "超级管理员不允许删除"},
    "UserNotExistError": {"code": 10036, "msg": "用户不存在"},
    "AccountDisabledError": {"code": 10037, "msg": "该账号已被禁用"},
    "AccountPermissionDisabledError": {"code": 10038, "msg": "该账号权限已被禁用"},
    "LoginAccountOtherDevices": {"code": 10039, "msg": "账号在其他设备登陆"},
    "BondModeNotSupport": {"code": 10040, "msg": "不支持该Bond类型"},
    "BondNameRepeatError": {"code": 10041, "msg": "Bond名称重复"},
    "SlaveLessThanTwoError": {"code": 10042, "msg": "请至少选择两张网卡进行绑定"},
    "SlaveNICNotExist": {"code": 10043, "msg": "被绑定网卡信息不存在"},
    "AlreadySlaveError": {"code": 10044, "msg": "网卡已绑定Bond"},
    "SlaveVSUplinksError": {"code": 10045, "msg": "网卡'{nic}'已关联分布式虚拟交换机，Bond失败"},
    "BondIpLessThanOne": {"code": 10046, "msg": "Bond至少需添加一个IP"},
    "NoGatewayInfoError": {"code": 10047, "msg": "请提供网关、DNS信息"},
    "BondNICNotExist": {"code": 10048, "msg": "Bond网卡信息不存在"},
    "BondVSUplinksError": {"code": 10049, "msg": "Bond网卡已关联分布式虚拟交换机，删除失败"},
    "InheritIPNotExist": {"code": 10050, "msg": "继承IP信息不存在"},
    "InheritNicNotSlave": {"code": 10051, "msg": "继承IP的网卡不是被绑定网卡"},
    "ManageNetworkNotInherit": {"code": 10052, "msg": "管理网络IP未指定继承网卡"},
    "ImageNetworkNotInherit": {"code": 10053, "msg": "镜像网络IP未指定继承网卡"},
    "SlaveInheritIpMuchError": {"code": 10054, "msg": "一个网卡最多继承2个IP"},
    "InactiveSlaveCannotInheritIP": {"code": 10055, "msg": "网卡'{nic}'未启用，不能继承IP"},
    "AllSlavesInactiveError": {"code": 10056, "msg": "所选网卡都未启用，编辑失败"},
    "IPUsedError": {"code": 10057, "msg": "IP地址'{ip}'已被集群中节点使用"},
    "RoleAlreadyReferencedError": {"code": 10058, "msg": "该角色已被引用，不能删除"},
    "RoleNotExistError": {"code": 10059, "msg": "该角色不存在"},
    "SuperAdminOnlySetError": {"code": 10060, "msg": "只有超级管理员才能设置"},


    "TerminalNotExistError": {"code": 10200, "msg": "终端不存在"},
    "TerminalCloseOperateError": {"code": 10201, "msg": "终端关机失败"},
    "TerminalRebootOperateError": {"code": 10202, "msg": "终端重启失败"},
    "TerminalDeleteOperateError": {"code": 10203, "msg": "终端删除失败"},
    "TerminalUpdateNameError": {"code": 10204, "msg": "终端更新名称失败"},
    "TerminalWebGroupNotExist": {"code": 10205, "msg": "终端分组不存在"},
    "TerminalGroupSortError": {"code": 10206, "msg": "终端组排序失败"},
    "TerminalStopSortError": {"code": 10207, "msg": "停止终端组排序失败"},
    "TerminalSortIpError": {"code": 10208, "msg": "终端重排IP异常"},
    "TerminalNotPersonalGroupError": {"code": 10209, "msg": "终端不是个人分组"},
    "TerminalSetupInfoError": {"code": 10210, "msg": "终端配置错误"},
    "TerminalSetupInfoParamError": {"code": 10211, "msg": "终端配置参数错误"},
    "TerminalLogNotExist": {"code": 10212, "msg": "终端日志不存在"},
    "TerminalLogFiveLimitError": {"code": 10213, "msg": "终端日志导出超过五个"},
    "TerminalUpgradeFileError": {"code": 10214, "msg": "终端升级文件错误"},
    "TerminalUpgradeNameError": {"code": 10215, "msg": "终端升级文件包名称不规范"},
    "TerminalUpgradeNotNeedError": {"code": 10216, "msg": "没有需要升级的终端"},
    "ISOAlreadyMounted": {"code": 10217, "msg": "ISO'{name}'已挂载"},
    "TemplateAlreadyUsed": {"code": 10218, "msg": "该分组下已基于该模板创建教学桌面组"},
    "NameAlreadyUseError": {"code": 10219, "msg": "名称已被占用"},
    "AuthExpired": {"code": 10220, "msg": "授权已过期"},
    "ComputeNodeShutdownError": {"code": 10221, "msg": "存在计算节点未关闭，导致关闭主控操作中断"},
    "AuthFailed": {"code": 10222, "msg": "序列号或单位名称错误，授权失败"},


    # 20001 ~ 20999 SEVER层错误码
    "ParamError": {"code": 20001, "msg": "参数异常"},
    "ReturnError": {"code": 20002, "msg": "返回值异常"},
    "NameAlreadyExistsError": {"code": 20003, "msg": "名称已存在，请重新输入"},
    "CreateWarnSetupFailError": {"code": 20004, "msg": "创建告警设置记录失败"},
    "UpdateWarnSetupFailError": {"code": 20005, "msg": "更新告警设置记录失败"},

    "ResourcePoolAddError": {"code": 20101, "msg": "资源池'{name}'创建失败"},
    "ResourcePoolListError": {"code": 20102, "msg": "获取资源池列表失败"},
    "ResourcePoolNameExistErr": {"code": 20103, "msg": "资源池'{name}'已存在"},
    "ResourcePoolNotExist": {"code": 20104, "msg": "资源池信息不存在"},
    "ResourcePoolUpdateError": {"code": 20105, "msg": "资源池{name}更新失败"},
    "ResourceDefaultError": {"code": 20106, "msg": "无法删除默认资源池{name}"},
    "ResourceImageSyncError": {"code": 20107, "msg": "资源池镜像同步失败"},
    "ResourceImageListError": {"code": 20108, "msg": "获取基础镜像列表失败"},
    "ResourceImageAddError": {"code": 20109, "msg": "基础镜像创建失败"},
    "ResourceImageReError": {"code": 20110, "msg": "基础镜像重传失败"},
    "ResourceImageNotExist": {"code": 20111, "msg": "基础镜像不存在"},
    "ResourceImageDelFail": {"code": 20112, "msg": "基础镜像删除失败"},
    "ResourcePoolDeleteFail": {"code": 20113, "msg": "此资源池删除失败"},
    "ResourcePoolHaveNodeDeleteFail": {"code": 20114, "msg": "此资源池下有计算节点，无法删除"},
    "ResourcePoolHaveTemplateDeleteFail": {"code": 20115, "msg": "该资源池已被引用，无法删除"},

    "CreateNodeFail": {"code": 20201, "msg": "节点'{node}'添加失败"},
    "NodeCheckFail": {"code": 20202, "msg": "节点'{node}'检测失败"},
    "NodeNotExist": {"code": 20203, "msg": "节点信息不存在"},
    "NodeAlreadyExist": {"code": 20204, "msg": "节点'{host_name}'已存在"},
    "NodeCheckPasswordFail": {"code": 20205, "msg": "节点'{node}'检测密码失败"},
    "NodeNotSupportvirtual": {"code": 20206, "msg": "节点'{node}'不支持硬件虚拟化"},
    "InstanceExist": {"code": 20207, "msg": "节点'{node}'存在模板或者桌面"},
    "NodeShutdownFailed": {"code": 20208, "msg": "节点'{node}'关机失败"},
    "NodeRebootFailed": {"code": 20209, "msg": "节点'{node}'重启失败"},
    "ControllerCannotDelete": {"code": 20209, "msg": "控制节点'{node}'不能删除"},
    "ControllerExists": {"code": 20210, "msg": "主控节点'{node}'已存在"},
    "ControllerNodeInitFail": {"code": 20211, "msg": "主控节点'{node}'初始化失败"},
    "NodeNotExistMsg": {"code": 20212, "msg": "节点'{hostname}'信息不存在"},
    "NodeInfoGetFail": {"code": 20213, "msg": "节点'{node}'网卡或存储信息获取失败"},
    "NodeStorageError": {"code": 20214, "msg": "节点'{node}'存储信息与主控不一致，缺少分区'{path}'"},
    "NodeNICNotExist": {"code": 20215, "msg": "节点网卡信息不存在"},
    "NodeNICIpTooManyError": {"code": 20216, "msg": "节点网卡IP设置超过限制"},
    "NodeNICIpAddError": {"code": 20217, "msg": "节点网卡IP设置异常"},
    "NodeServiceNotExist": {"code": 20218, "msg": "节点服务信息不存在"},
    "ModifyNodeFail": {"code": 20219, "msg": "节点'{node}'修改失败"},
    "NodeIPAlreadyExist": {"code": 20220, "msg": "节点'{ip}'已存在"},
    "NodeIPConnetFail": {"code": 20221, "msg": "节点'{ip}'连接失败"},
    "NetworkCardVirtualSwitchError": {"code": 20222, "msg": "网卡数小于当前分布式虚拟交换机数量"},
    "SystemNotRestoreError": {"code": 20223, "msg": "需手动删除对应桌面/系统桌面，才可删除该计算节点"},
    "NodeNetworkInfoError": {"code": 20224, "msg": "节点网络数据异常"},
    "BondAddError": {"code": 20225, "msg": "节点{node}网卡bond添加失败"},
    "BondEditError": {"code": 20226, "msg": "节点{node}网卡bond编辑失败"},
    "BondDeleteError": {"code": 20227, "msg": "节点{node}网卡bond删除失败"},

    "IPAddrError": {"code": 20301, "msg": "IP地址'{ipaddr}'不正确"},
    "NetworkInitFail": {"code": 20302, "msg": "网络信息初始化失败"},
    "NetworkCreateFail": {"code": 20303, "msg": "网络'{name}'创建失败"},
    "NetworkInfoNotExist": {"code": 20304, "msg": "数据网络不存在"},
    "SubnetCreateError": {"code": 20305, "msg": "子网'{name}'创建失败"},
    "VlanIDError": {"code": 20306, "msg": "Vlan ID'{vid}'错误"},
    "NetworkNotVSError": {"code": 20307, "msg": "数据网络未关联虚拟交换机"},
    "NetworkNameRepeatError": {"code": 20308, "msg": "数据网络名称'{name}'重复"},
    "SubnetNameRepeatError": {"code": 20309, "msg": "子网'{name}'名称重复"},
    "SubnetNotExist": {"code": 20310, "msg": "子网信息不存"},
    "NetworkDeleteFail": {"code": 20311, "msg": "网络删除失败"},
    "NetworkUpdateError": {"code": 20312, "msg": "数据网络'{name}'更新失败"},
    "SubnetInfoError": {"code": 20313, "msg": "子网'{name}'信息错误"},
    "NetworkInUse": {"code": 20314, "msg": "数据网络'{name}'已被使用"},
    "VlanIDExistError": {"code": 20315, "msg": "Vlan ID已存在"},
    "IpAddressConflictError": {"code": 20316, "msg": "所填IP地址段与已有IP地址段IP存在交集"},
    "ImageNetworkConnectFail": {"code":20317, "msg": "镜像网络选择与主控镜像网络连接不通，请重选"},
    "ImageNetworSpeedFail": {"code":20318, "msg": "镜像网络速率与主控镜像网络不匹配，将影响镜像同传速度"},
    "SubnetDeleteInfo": {"code": 20319, "msg": "该网络正在使用，删除失败"},
    "SubnetDeleteFail": {"code": 20320, "msg": "子网删除失败"},
    "DataNetworkDeleteInfo": {"code": 20321, "msg": "数据网络部分删除失败：{info}"},
    "DataNetworkDeleteFail": {"code": 20322, "msg": "数据网络删除失败"},

    "VSwitchCreateError": {"code": 20401, "msg": "虚拟交换机'{name}'创建失败"},
    "VSwitchNotExist": {"code": 20402, "msg": "虚拟交换机信息不存在"},
    "VSwitchExistError": {"code": 20403, "msg": "虚拟交换机'{name}'已存在"},
    "VSwitchUsedError": {"code": 20404, "msg": "虚拟交换机'{name}'已在使用，无法修改"},

    "GroupCreateError": {"code": 20601, "msg": "分组'{name}'创建失败"},
    "GroupInUse": {"code": 20602, "msg": "分组'{name}'已有桌面组使用"},
    "GroupNotExists": {"code": 20602, "msg": "分组'{name}'不存在"},
    "GroupUpdateError": {"code": 20603, "msg": "分组'{name}'更新失败"},
    "GroupDeleteError": {"code": 20604, "msg": "分组删除失败"},
    "GroupAlreadyExists": {"code": 20605, "msg": "分组'{name}'已存在"},
    "GroupUserCreateError": {"code": 20606, "msg": "分组用户'{user_name}'创建失败"},
    "GroupUserNotExists": {"code": 20607, "msg": "分组用户'{user_name}'不存在"},
    "GroupUserUpdateError": {"code": 20608, "msg": "分组用户'{user_name}'更新失败"},
    "GroupUserExists": {"code": 20609, "msg": "分组用户'{user_name}'已存在"},
    "GroupUserDeleteError": {"code": 20610, "msg": "分组用户删除失败"},
    "GroupUserEnableError": {"code": 20611, "msg": "分组用户'{user_name}'启用失败"},
    "GroupUserDisableError": {"code": 20612, "msg": "分组用户'{user_name}'禁用失败"},
    "GroupUserMoveError": {"code": 20612, "msg": "分组用户'{user_name}'移动到'{group}'失败"},
    "GroupUserExportError": {"code": 20612, "msg": "用户导出到'{file}'失败"},
    "GroupSubnetError": {"code": 20613, "msg": "分组已被桌面组引用，不允许修改网络"},

    "TemplateCreateFail": {"code": 20701, "msg": "模板'{name}'创建失败"},
    "TemplateNotExist": {"code": 20702, "msg": "模板不存在"},
    "TemplateRecreateFail": {"code": 20703, "msg": "模板'{name}'差异盘重建失败"},
    "TemplateStartFail": {"code": 20704, "msg": "模板'{name}'启动失败"},
    "TemplateDeleteFail": {"code": 20705, "msg": "模板'{name}'删除失败"},
    "TemplateCopyFail": {"code": 20706, "msg": "复制模板'{name}'失败"},
    "TemplateAlreadyExist": {"code": 20707, "msg": "模板'{name}'已存在"},
    "TemplateUpdateError": {"code": 20708, "msg": "模板'{name}'更新失败"},
    "TemplateLoadIsoFail": {"code": 20709, "msg": "模板'{name}'加载ISO失败"},
    "TemplateDownloadFail": {"code": 20710, "msg": "下载模板'{name}'失败"},
    "TemplateEducationError": {"code": 20711, "msg": "模板'{name}'为教学模板"},
    "TemplatePersonalError": {"code": 20712, "msg": "模板'{name}'为个人模板"},
    "TemplateResyncError": {"code": 20713, "msg": "模板镜像重传失败"},
    "TemplateImageNotExist": {"code": 20714, "msg": "模板镜像不存在"},
    "TemplateNeedResync": {"code": 20715, "msg": "模板镜像异常，请先在节点'{node}'重传"},
    "TemplateIsActive": {"code": 20716, "msg": "模板'{name}'在线，请先关机"},
    "TemplateSendKeyFail": {"code": 20717, "msg": "模板'{name}'发送命令失败"},

    "DesktopCreateFail": {"code": 20711, "msg": "桌面组'{name}'创建失败"},
    "DesktopNotExist": {"code": 20712, "msg": "桌面组'{name}'不存在"},
    "InstanceCreateFail": {"code": 20713, "msg": "桌面组'{desktop}'添加桌面失败"},
    "InstanceStartFail": {"code": 20714, "msg": "桌面实例'{name}'启动失败"},
    "InstanceStopFail": {"code": 20715, "msg": "桌面实例'{name}'停止失败"},
    "InstanceDeleteFail": {"code": 20716, "msg": "桌面实例'{name}'删除失败"},
    "IPNotEnough": {"code": 20717, "msg": "可用IP不足"},
    "IPNotInRange": {"code": 20718, "msg": "IP'{ipaddr}'不在子网范围内"},
    "IPInUse": {"code": 20719, "msg": "此IP已被集群中节点使用"},
    "DesktopDeleteFail": {"code": 20720, "msg": "桌面组删除失败"},
    "DesktopUpdateFail": {"code": 20721, "msg": "桌面组'{name}'更新失败"},
    "DesktopRebootError": {"code": 20722, "msg": "桌面组'{name}'重启失败"},
    "DesktopStartError": {"code": 20723, "msg": "桌面组'{name}'开机失败"},
    "DesktopStopError": {"code": 20724, "msg": "桌面组'{name}'关机失败"},
    "DesktopAlreadyExist": {"code": 20725, "msg": "桌面组'{name}'已存在"},
    "InstanceRebootFail": {"code": 20726, "msg": "桌面实例'{name}'重启失败"},
    "TemplateInUse": {"code": 20727, "msg": "模板'{name}'已被桌面组引用，不允许删除"},
    "TemplateActive": {"code": 20728, "msg": "模板'{name}'已开机，请先关机"},
    "TemplateDiskSizeError": {"code": 20729, "msg": "模板的磁盘只能扩容不能缩减"},
    "TemplateStopError": {"code": 20730, "msg": "模板'{name}'关机失败"},
    "TemplateResetError": {"code": 20731, "msg": "模板'{name}'重置失败"},
    "NameExistsError": {"code": 20732, "msg": "该名称'{name}'已被占用，请重新输入"},
    "DatabaseBackFail": {"code": 20800, "msg": "数据库备份失败"},
    "DatabaseBackCrontabError": {"code": 20801, "msg": "设置数据库备份定时任务错误"},
    "AddInstanceCrontabError": {"code": 20802, "msg": "添加桌面定时任务失败"},
    "InstanceGetError": {"code": 20802, "msg": "桌面不存在或者不属于该桌面组"},
    "InstanceNotExist": {"code": 20803, "msg": "桌面'{name}'不存在"},
    "InstancePowerOff": {"code": 20804, "msg": "桌面'{name}'不在线，请先开机"},
    "DatabaseBackNotExist": {"code": 20805, "msg": "数据库备份'{name}'不存在"},
    "DatabaseDownloadError": {"code": 20806, "msg": "数据库备份下载失败"},

    "TerminalUserLoginError": {"code": 20900, "msg": "终端用户登录失败"},
    "TerminalUserNotExistError": {"code": 20901, "msg": "终端用户不存在"},
    "TerminalAccountError": {"code": 20902, "msg": "终端用户账号密码错误"},
    "TerminalUserPasswdError": {"code": 20903, "msg": "终端用户密码错误"},
    "TerminalUserUnenabledError": {"code": 20904, "msg": "终端用户账号被禁用"},
    "TerminalUserIsOnlineError": {"code": 20905, "msg": "终端用户账号已登录"},
    "TerminalGroupNotExist": {"code": 20906, "msg": "终端组不存在"},
    "TerminalUserNotExist": {"code": 20907, "msg": "终端用户不存在"},
    "TerminalPersonInstanceNotAlloc": {"code": 20908, "msg": "终端用户个人桌面没有分配"},
    "TerminalUserSessionInvalid": {"code": 20909, "msg": "终端用户session失效"},
    "TerminalUserLogout": {"code": 20910, "msg": "终端用户已注销"},
    "TerminalPersonMaintenance": {"code": 20911, "msg": "桌面组处于维护模式"},
    "TerminalPersonStartError": {"code": 20912, "msg": "桌面启动失败"},
    "TerminalEducationStartError": {"code": 20913, "msg": "桌面启动失败"},
    "TerminalEduInstanceNotAlloc": {"code": 20914, "msg": "终端教学桌面未分配"},
    "TerminalPersonalInstanceNumError": {"code": 20915, "msg": "终端个人桌面连接不能大于2"},
    "TerminalEduInstanceRepeatError": {"code": 20916, "msg": "教学终端序号冲突"},
    "TerminalInstanceNotExist": {"code": 20917, "msg": "终端桌面不存在"},
    "TerminalInstanceCloseFail": {"code": 20918, "msg": "终端桌面关闭失败"},


    # 30001 ~ 30999 COMPUTER层错误码
    "UndefinedNetworkType": {"code": 30001, "msg": "不支持的网络类型"},
    "NetworkNamespaceNotFound": {"code": 30002, "msg": "网络命名空间不存在"},
    "NetworkInterfaceNotFound": {"code": 30003, "msg": "网络设备不存在"},
    "InterfaceOperationNotSupported": {"code": 30004, "msg": "不支持的设备操作"},
    "InterfaceNameTooLong": {"code": 30005, "msg": "网络设备名称过长"},
    "InvalidArgument": {"code": 30006, "msg": "无效的设备参数值"},
    "InstanceNotFound": {"code": 30007, "msg": "虚拟机不存在"},
    "InstancePowerOffFailure": {"code": 30008, "msg": "虚拟机关机失败"},
    "HypervisorUnavailable": {"code": 30009, "msg": "hypervisor连接失败"},
    "NBDConnectException": {"code": 30010, "msg": "NBD设备连接失败"},
    "NBDDisconnectException": {"code": 30011, "msg": "NBD断开连接失败"},
    "ModifyComputeNameException": {"code": 30012, "msg": "修改虚拟机名异常"},
    "SetIPAddressException": {"code": 30013, "msg": "设置虚拟机IP异常"},
    "ImageNotFound": {"code": 30014, "msg": "镜像不存在"},
    "ImageVersionError": {"code": 30015, "msg": "镜像版本错误"},
    "ImageCopyIOError": {"code": 30016, "msg": "复制镜像失败"},
    "CdromNotExist": {"code": 30017, "msg": "cdrom设备不存在"},
    "ChangeCdromPathError": {"code": 30018, "msg": "修改cdrom设备路径失败"},
    "ImageResizeError": {"code": 30019, "msg": "镜像扩容失败"},
    "ImageCommitError": {"code": 30020, "msg": "镜像合并失败"},
    "InstanceAutostartError": {"code": 30021, "msg": "虚拟机设置开机启动失败"},
    "AttachDiskError": {"code": 30022, "msg": "添加磁盘失败"},
    "SetVcpuMemoryError": {"code": 30023, "msg": "设置cpu或者内存错误"},
    "DetachDiskError": {"code": 30024, "msg": "删除磁盘失败"},
    "DiskNotExist": {"code": 30025, "msg": "磁盘不存在"},
    "ConfigBondError": {"code": 30026, "msg": "Bond配置失败"},
    "UnBondError": {"code": 30027, "msg": "Bond解绑失败"},
    "IPUsedByOtherHost": {"code": 30028, "msg": "其他MAC'{mac}'已使用IP地址'{ip}'"},


    # 40001 ~ 40999 MONITOR层错误码
    "GetCpuInfoFailure": {"code": 40001, "msg": "获取CPU信息失败"},
    "GetCpuVtInfoFailure": {"code": 40002, "msg": "获取CPU虚拟化信息失败"},
    "GetMemoryInfoFailure": {"code": 40101, "msg": "获取内存信息失败"},
    "GetDiskInfoFailure": {"code": 40201, "msg": "获取存储信息失败"},
    "GetDiskIoInfoFailure": {"code": 40202, "msg": "获取磁盘IO信息失败"},
    "GetNetworkInfoFailure": {"code": 40301, "msg": "获取网络信息失败"},
    "GetNetworkIoInfoFailure": {"code": 40302, "msg": "获取网络IO信息失败"},
    "IpInfoParamError": {"code": 40303, "msg": "IP信息参数异常"},
    "NotPhysicalNICError": {"code": 40304, "msg": "非物理网卡"},
    "MainNICIpDelError": {"code": 40305, "msg": "物理网卡的IP不能删除"},
    "IpConfFileNoFound": {"code": 40306, "msg": "IP配置文件不存在"},
    "AddIpConfFileFailure": {"code": 40307, "msg": "新增IP配置文件失败"},
    "UpdateIpConfFileFailure": {"code": 40308, "msg": "更新IP配置文件失败"},
    "DeleteIpConfFileFailure": {"code": 40309, "msg": "删除IP配置文件失败"},
    "ExchangeIpConfFileFailure": {"code": 40310, "msg": "互换IP配置文件失败"},
    "IpConfFileExistsError": {"code": 40311, "msg": "IP配置文件存在"},

    "GetHardwareInfoFailure": {"code": 40401, "msg": "获取机器硬件信息失败"},
    "GetServiceInfoFailure": {"code": 40501, "msg": "获取系统服务信息失败"},
    "GetVmInfoFailure": {"code": 40502, "msg": "获取虚拟机信息失败"},
    "NotFoundCrontabRecord": {"code": 40601, "msg": "没有找到相应的Crontab记录"},
    "FoundMultipleCrontabRecord": {"code": 40602, "msg": "找到多条同名的Crontab记录"},
    "CrontabTaskNotExists": {"code": 40603, "msg": "定时任务'{name}'不存在"},
    "CrontabTaskAlreadyExists": {"code": 40604, "msg": "定时任务'{name}'已存在"},
    "CrontabTaskUpdateError": {"code": 40605, "msg": "定时任务'{name}'更新失败"},


    # 50001 ~ 50999 TERMINAL层错误码
    "TerminalCommunicationError": {"code": 50001, "msg": "终端通信错误"},
    "OnlineDoNotDeleteError": {"code": 50002, "msg": "终端在线不允许删除"},
    "RedisServerError": {"code": 50003, "msg": "Redis服务异常"},
    "RequestParamError": {"code": 50004, "msg": "请求参数异常"},
    "TerminalConfigNotFound": {"code": 50005, "msg": "终端配置信息不存在"},

    "MessageError": {"code": 88888, "msg": "报文错误，请修正重试"},
    "ComputeServiceUnavaiable": {"code": 80000, "msg": "节点'{ipaddr}'compute服务连接失败"},
    "ComputeServiceTimeout": {"code": 80001, "msg": "节点'{ipaddr}'compute服务连接超时"},
    "ServerServiceUnavaiable": {"code": 80002, "msg": "节点server服务连接失败"},
    "ServerServiceTimeout": {"code": 80003, "msg": "节点server服务连接超时"},
    "MonitorServiceUnavaiable": {"code": 88889, "msg": "节点 {ipaddr} monitor服务连接失败"},
    "TerminalServiceUnavaiable": {"code": 88890, "msg": "terminal管理服务连接失败"},
    "SystemError": {"code": 99999, "msg": "系统异常，请稍后重试"},
    "OtherError": {"code": -1, "msg": "未知异常"},
}


def get_error_result(error="Success", data=None, **kwargs):
    error_code = deepcopy(ERROR_CODE)
    error_msg = error_code.get(error, error_code.get("OtherError"))
    message = error_msg['msg'].format(**kwargs)
    if data is not None and isinstance(data, (dict, list, str)):
        error_msg.update({"data": data})
    error_msg['msg'] = message
    return error_msg
