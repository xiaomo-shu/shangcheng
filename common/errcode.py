# -*- coding: utf-8 -*-
from copy import deepcopy


ERROR_CODE = {
    "Success": {"code": 0, "msg": "成功"},
    # 10001 ~ 10999 WEB层错误码
    "LoginFailError": {"code": 10001, "msg": "登录失败"},
    "UsernameError": {"code": 10002, "msg": "用户名错误"},
    "UpdateNoChangeError": {"code": 10003, "msg": "修改'{param}'值相同"},
    "NetworkInterfaceNotExist": {"code": 10004, "msg": "节点'{node}'网络接口'{interface}'不存在"},
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

    # 20001 ~ 20999 SEVER层错误码
    "ParamError": {"code": 20001, "msg": "参数异常"},
    "ReturnError": {"code": 20002, "msg": "返回值异常"},
    "NameAlreadyExistsError": {"code": 20003, "msg": "名称已存在，请重新输入"},
    "SpaceNotEnough": {"code": 20004, "msg": "存储空间不足"},
    "WarnSetupRecordExistsError": {"code": 20005, "msg": "告警设置记录已存在"},
    "CreateWarnSetupFailError": {"code": 20006, "msg": "创建告警设置记录失败"},
    "UpdateWarnSetupFailError": {"code": 20007, "msg": "更新告警设置记录失败"},

    "ResourcePoolAddError": {"code": 20101, "msg": "资源池'{name}'创建失败"},
    "ResourcePoolListError": {"code": 20102, "msg": "获取资源池列表失败"},
    "ResourcePoolNameExistErr": {"code": 20103, "msg": "资源池'{name}'已存在"},
    "ResourcePoolNotExist": {"code": 20104, "msg": "资源池信息不存在"},
    "ResourcePoolUpdateError": {"code": 20105, "msg": "资源池'{name}'更新失败"},
    "ResourceDefaultError": {"code": 20106, "msg": "无法删除默认资源池'{name}'"},
    "ResourceImageSyncError": {"code": 20107, "msg": "资源池镜像同步失败"},
    "ResourceImageListError": {"code": 20108, "msg": "获取基础镜像列表失败"},
    "ResourceImageAddError": {"code": 20109, "msg": "基础镜像创建失败"},
    "ResourceImageReError": {"code": 20110, "msg": "基础镜像重传失败"},
    "ResourceImageNotExist": {"code": 20111, "msg": "基础镜像不存在"},
    "ResourceImageDelFail": {"code": 20112, "msg": "基础镜像删除失败"},
    "ResourcePoolDeleteFail": {"code": 20113, "msg": "此资源池删除失败"},
    "ResourcePoolHaveNodeDeleteFail": {"code": 20114, "msg": "此资源池下有计算节点，无法删除"},

    "CreateNodeFail": {"code": 20201, "msg": "节点'{node}'添加失败"},
    "NodeCheckFail": {"code": 20202, "msg": "节点'{node}'检测失败"},
    "NodeNotExist": {"code": 20203, "msg": "节点信息不存在"},
    "NodeAlreadyExist": {"code": 20204, "msg": "节点'{host_name}'已存在"},
    "NodeNotSupportvirtual": {"code": 20206, "msg": "节点'{node}'不支持硬件虚拟化"},
    "InstanceExist": {"code": 20207, "msg": "节点'{node}'存在模板或者桌面"},
    "NodeShutdownFailed": {"code": 20208, "msg": "节点'{node}'关机失败"},
    "NodeRebootFailed": {"code": 20209, "msg": "节点'{node}'重启失败"},
    "ControllerCannotDelete": {"code": 20209, "msg": "控制节点'{node}'不能删除"},
    "ControllerExists": {"code": 20210, "msg": "主控节点'{node}'已存在"},
    "ControllerNodeInitFail": {"code": 20211, "msg": "主控节点'{node}'初始化失败"},
    "NodeNotExistMsg": {"code": 20212, "msg": "节点'{hostname}'信息不存在"},
    "NodeInfoGetFail": {"code": 20212, "msg": "节点'{node}'网卡或存储信息获取失败"},
    "NodeStorageError": {"code": 20213, "msg": "节点'{node}'存储信息与主控不一致，缺少分区'{path}'"},
    "NodeNICNotExist": {"code": 20214, "msg": "节点网卡信息不存在"},
    "NodeNICIpTooManyError": {"code": 20215, "msg": "节点网卡IP设置超过限制"},
    "NodeStorageException": {"code": 20213, "msg": "新增的存储'{name}'名称，与主控不符，添加失败"},
    "NodeNICIpAddError": {"code": 20217, "msg": "节点网卡IP设置异常"},
    "ManageNetCanNotUpdate": {"code": 20219, "msg": "管理和镜像网络不能修改"},
    "ModifyNodeFail": {"code": 20219, "msg": "节点'{node}'修改失败"},
    "NodeIPAlreadyExist": {"code": 20220, "msg": "节点{ip}已存在"},
    "NodeIPConnetFail": {"code": 20221, "msg": "节点{ip}连接失败"},
    "NetworkCardVirtualSwitchError": {"code": 20222, "msg": "网卡数小于当前分布式虚拟交换机数量"},
    "SystemNotRestoreError": {"code": 20223, "msg": "需手动删除对应桌面/系统桌面，才可删除该计算节点"},
    "NodeNetworkInfoError": {"code": 20224, "msg": "节点网络数据异常"},
    "BondAddError": {"code": 20225, "msg": "节点{node}网卡bond添加失败"},
    "BondEditError": {"code": 20226, "msg": "节点{node}网卡bond编辑失败"},
    "BondDeleteError": {"code": 20227, "msg": "节点{node}网卡bond删除失败"},
    "HaNotRunningError": {"code": 20228, "msg": "HA运行处于故障状态，不允许操作"},
    "HaNodeChangeManagementIPError": {"code": 20229, "msg": "已启用HA的节点不能修改管理IP"},
    "QuorumIPConnectError": {"code": 20230, "msg": "仲裁IP连接不通，请重新输入"},
    "HaNotSyncingError": {"code": 20231, "msg": "HA数据同步未完成，不允许操作"},
    "ServerExistError": {"code": 20233, "msg": "远端服务器已存在"},
    "RemoteStorageNameExistError": {"code": 20234, "msg": "远端存储名称已存在"},
    "RemoteStorageNotExistError": {"code": 20235, "msg": "远端存储不存在"},
    "RemoteStorageAlreadyAllocatedError": {"code": 20236, "msg": "远端存储已分配"},
    "RemoteStorageNotAllocatedError": {"code": 20237, "msg": "远端存储未分配"},
    'MountNfsError': {"code": 20238, "msg": "远端存储在节点'{host}'挂载失败"},
    'UmountNfsError': {"code": 20239, "msg": "远端存储在节点'{host}'取消挂载失败"},
    'RemoteStorageUsedError': {"code": 20240, "msg": "远端存储已被资源池使用"},
    'RemoteStorageHasImage': {"code": 20241, "msg": "远端存储含有镜像文件"},

    "IPAddrError": {"code": 20301, "msg": "IP地址'{ipaddr}'不正确"},
    "NetworkInitFail": {"code": 20302, "msg": "网络信息初始化失败"},
    "NetworkCreateFail": {"code": 20303, "msg": "网络'{name}'创建失败"},
    "NetworkInfoNotExist": {"code": 20304, "msg": "数据网络不存在"},
    "SubnetCreateError": {"code": 20305, "msg": "子网'{name}'创建失败"},
    "VlanIDError": {"code": 20306, "msg": "Vlan ID {vid} 错误"},
    "NetworkNotVSError": {"code": 20307, "msg": "数据网络未关联虚拟交换机"},
    "NetworkNameRepeatError": {"code": 20308, "msg": "数据网络名称'{name}'重复"},
    "SubnetNameRepeatError": {"code": 20309, "msg": "子网'{name}'名称重复"},
    "SubnetNotExist": {"code": 20310, "msg": "子网信息不存在"},
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
    "DataNetworkDeleteInfo": {"code": 20321, "msg": "数据网络部分删除失败:{info}"},
    "DataNetworkDeleteFail": {"code": 20322, "msg": "数据网络删除失败"},
    "GatewayAndIpError" : {"code": 20323, "msg": "网关和IP不在同一网段"},

    "VSwitchCreateError": {"code": 20401, "msg": "虚拟交换机'{name}'创建失败"},
    "VSwitchNotExist": {"code": 20402, "msg": "虚拟交换机信息不存在"},
    "VSwitchExistError": {"code": 20403, "msg": "虚拟交换机'{name}'已存在"},
    "VSwitchUsedError": {"code": 20404, "msg": "虚拟交换机'{name}'已在使用，无法修改"},
    "VSwitchDeletedError": {"code": 20405, "msg": "虚拟交换机'{name}'被关联，无法删除"},
    "VSwitchFlatInUse": {"code": 20406, "msg": "Flat类型虚拟交换机只能被一个数据网络使用"},

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
    "EduGroupNotExist": {"code": 20614, "msg": "教学分组不存在"},
    "EduDesktopNotExist": {"code": 20615, "msg": "教学桌面组不存在"},
    "EduDesktopNotBelongGroup": {"code": 20616, "msg": "教学桌面组不属于教学分组"},
    "CourseNotEduGroup": {"code": 20617, "msg": "排课管理只能应用于教学分组"},
    "TermEndPassedError": {"code": 20618, "msg": "学期结束日期不能为过去时间"},
    "CourseScheduleNotExist": {"code": 20619, "msg": "课表不存在"},
    "TermStartLaterThanEndError": {"code": 20620, "msg": "学期开始日期不能晚于学期结束日期"},
    "AddCourseScheduleCrontabError": {"code": 20621, "msg": "课表启用失败"},
    "DisableCourseScheduleError": {"code": 20622, "msg": "课表禁用失败"},
    "TermDuplicateError": {"code": 20623, "msg": "开学时间和结束时间与'{name}'存在交集，创建失败"},
    "TermNotExist": {"code": 20624, "msg": "学期不存在"},
    "TermNameExist": {"code": 20625, "msg": "学期名称已存在"},
    "TermOccupiedError": {"code": 20626, "msg": "该学期已存在课表，只能修改学期名称"},
    "GroupInUseByCourseSchedule": {"code": 20627, "msg": "分组'{name}'有关联的课表，请先清除课表"},
    "DesktopInUseByCourseSchedule": {"code": 20628, "msg": "桌面组'{name}'有关联的课表，请先清除课表"},
    "TermDetailError": {"code": 20629, "msg": "{detail_msg}"},

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
    "UpdateTimeError": {"code": 20718, "msg": "定时更新时间不能小于当前服务端系统时间"},
    "TemplateVersionNotExist": {"code": 20719, "msg": "模板更新点信息不存在"},
    "TemplateRollbackError": {"code": 20720, "msg": "模板回滚失败"},
    "TemplateCopying": {"code": 20721, "msg": "模板正在复制中，不可进行更新操作"},
    "TemplateDownloading": {"code": 20722, "msg": "模板正在下载中，不可进行更新操作"},
    "SystemIsActive": {"code": 20723, "msg": "该系统桌面处于开机状态，请先执行关机操作"},
    "InstancePathNotExist": {"code": 20724, "msg": "系统盘或数据盘存储设备不存在"},
    "TemplateNotAllowUpdateError": {"code": 20725, "msg": "该模板所处状态不允许自动更新"},

    "DesktopCreateFail": {"code": 20731, "msg": "桌面组'{name}'创建失败"},
    "DesktopNotExist": {"code": 20732, "msg": "桌面组'{name}'不存在"},
    "InstanceCreateFail": {"code": 20733, "msg": "桌面组'{desktop}'添加桌面失败"},
    "InstanceStartFail": {"code": 20734, "msg": "桌面实例'{name}'启动失败"},
    "InstanceStopFail": {"code": 20735, "msg": "桌面实例'{name}'停止失败"},
    "InstanceDeleteFail": {"code": 20736, "msg": "桌面实例'{name}'删除失败"},
    "IPNotEnough": {"code": 20737, "msg": "可用IP不足"},
    "IPNotInRange": {"code": 20738, "msg": "IP'{ipaddr}'不在子网范围内"},
    "IPInUse": {"code": 20739, "msg": "此IP已被占用，请重新输入"},
    "DesktopDeleteFail": {"code": 20740, "msg": "桌面组删除失败"},
    "DesktopUpdateFail": {"code": 20741, "msg": "桌面组'{name}'更新失败"},
    "DesktopRebootError": {"code": 20742, "msg": "桌面组'{name}'重启失败"},
    "DesktopStartError": {"code": 20743, "msg": "桌面组'{name}'开机失败"},
    "DesktopStopError": {"code": 20744, "msg": "桌面组'{name}'关机失败"},
    "DesktopAlreadyExist": {"code": 20745, "msg": "桌面组'{name}'已存在"},
    "InstanceRebootFail": {"code": 20746, "msg": "桌面实例'{name}'重启失败"},
    "TemplateInUse": {"code": 20747, "msg": "模板'{name}'已被桌面组引用， 不允许删除"},
    "TemplateActive": {"code": 20748, "msg": "模板'{name}'已开机，请先关机"},
    "TemplateDiskSizeError": {"code": 20749, "msg": "模板的磁盘只能扩容不能缩减"},
    "TemplateStopError": {"code": 20750, "msg": "模板'{name}'关机失败"},
    "TemplateResetError": {"code": 20751, "msg": "模板'{name}'重置失败"},
    "VOIDesktopGroupNotExist": {"code": 20752, "msg": "桌面组不存在"},
    "DatabaseBackFail": {"code": 20800, "msg": "数据库备份失败"},
    "DatabaseBackCrontabError": {"code": 20801, "msg": "设置数据库备份定时任务错误"},
    "AddInstanceCrontabError": {"code": 20802, "msg": "添加桌面定时任务失败"},
    "InstanceGetError": {"code": 20803, "msg": "桌面不存在或者不属于该桌面组"},
    "InstanceNotExist": {"code": 20804, "msg": "桌面'{name}'不存在"},
    "InstancePowerOff": {"code": 20805, "msg": "桌面'{name}'不在线，请先开机"},
    "DatabaseBackNotExist": {"code": 20806, "msg": "数据库备份'{name}'不存在"},
    "CrontabDeleteError": {"code": 20807, "msg": "删除定时任务失败"},
    "CrontabUpdateError": {"code": 20808, "msg": "定时任务更新失败'{info}'"},
    "CrontabTaskNotExists": {"code": 20809, "msg": "定时任务'{name}'不存在"},
    "AddNodeCrontabError": {"code": 20810, "msg": "添加节点定时任务失败"},
    "PersonalInstanceActive": {"code": 20811, "msg": "桌面'{name}'已开机，无法删除"},
    "InstanceStartConflict": {"code": 20812, "msg": "桌面组'{desktop_name}'对应桌面'{name}'已开机，启动失败"},
    "AddWarningLogCronError": {"code": 20813, "msg": "添加警告日志自动清理定时任务失败"},
    "UpdateWarningLogCronError": {"code": 20814, "msg": "更新告警日志自动定时任务失败"},
    "AddTerminalCrontabError":{"code": 20815, "msg": "添加终端定时任务失败"},

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
    "AuthSizeExpired": {"code": 20919, "msg": "桌面授权数已达到最大，请联系管理员"},
    "ResourceAllocateError": {"code": 20920, "msg": "资源分配失败，请稍后重试"},
    "NodeStorageNotExist": {"code": 20921, "msg": "节点'{node}'存储路径'{path}'不存在"},
    "AuthExpired": {"code": 20922, "msg": "授权已过期"},
    "ShareDiskUpdateFail": {"code": 20930, "msg": "共享数据盘更新失败"},
    "TerminalTorrentDownloading": {"code": 20931, "msg": "有终端正在进行桌面下发任务，请先到终端管理页面取消下发后再进行删除"},

    "DhcpConfigUpdateError": {"code": 20940, "msg": "DHCP配置文件更新异常"},
    "TerminalUploadDiffNotExist": {"code": 20941, "msg": "终端上传差分盘不存在"},
    "TerminalUploadUpdateFail": {"code": 20942, "msg": "终端上传差分盘更新失败"},

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
    "IPUsedByOtherHost": {"code": 30028, "msg": "其他主机'{mac}'已使用IP地址'{ip}'"},
    "EnableHAError": {"code": 30029, "msg": "启用HA失败"},
    "DisableHAError": {"code": 30030, "msg": "禁用HA失败"},
    "ConfigBackupHAError": {"code": 30031, "msg": "备控HA配置失败"},
    "StartBackupHAError": {"code": 30032, "msg": "备控HA启动失败"},
    "SwitchHaMasterError": {"code": 30033, "msg": "HA主备切换失败"},
    "MountPointNotExist": {"code": 30034, "msg": "挂载点获取失败"},
    "AbnormalNetworkEnvironment": {"code": 30035, "msg": "网络环境异常，时间服务器同步失败"},


    # 40001 ~ 40999 MONITOR层错误码
    "GetCpuInfoFailure": {"code": 40001, "msg": "获取CPU信息失败"},
    "GetCpuVtInfoFailure": {"code": 40002, "msg": "获取CPU虚拟化信息失败"},
    "GetMemoryInfoFailure": {"code": 40101, "msg": "获取内存信息失败"},
    "GetDiskInfoFailure": {"code": 40201, "msg": "获取存储信息失败"},
    "GetDiskIoInfoFailure": {"code": 40202, "msg": "获取磁盘IO信息失败"},
    "GetNetworkInfoFailure": {"code": 40301, "msg": "获取网络信息失败"},
    "GetNetworkIoInfoFailure": {"code": 40302, "msg": "获取网络IO信息失败"},
    "IpInfoParamError": {"code": 40303, "msg": "IP信息参数异常"},
    "NotPhysicalNICError": {"code": 40304, "msg": "网卡不是物理网卡"},
    "MainNICIpDelError": {"code": 40305, "msg": "物理网卡的IP不能删除"},
    "IpConfFileNoFound": {"code": 40306, "msg": "IP配置文件不存在"},
    "AddIpConfFileFailure": {"code": 40307, "msg": "新增IP配置文件失败"},
    "UpdateIpConfFileFailure": {"code": 40308, "msg": "更新IP配置文件失败"},
    "DeleteIpConfFileFailure": {"code": 40309, "msg": "删除IP配置文件失败"},
    "ExchangeIpConfFileFailure": {"code": 40310, "msg": "互换IP配置文件失败"},
    "IpConfFileExistsError": {"code": 40311, "msg": "IP配置文件存在"},
    "VerifyPasswordError": {"code": 40312, "msg": "用户名或密码错误"},
    "GetSystemRunningTimeError": {"code": 40313, "msg": "获取系统运行时间失败"},

    "GetHardwareInfoFailure": {"code": 40401, "msg": "获取机器硬件信息失败"},
    "GetServiceInfoFailure": {"code": 40501, "msg": "获取系统服务信息失败"},
    "GetVmInfoFailure": {"code": 40502, "msg": "获取虚拟机信息失败"},
    "NotFoundCrontabRecord": {"code": 40601, "msg": "没有找到相应的Crontab记录"},
    "FoundMultipleCrontabRecord": {"code": 40602, "msg": "找到多条同名的Crontab记录"},
    "CrontabTaskAlreadyExists": {"code": 40603, "msg": "定时任务'{name}'已存在"},


    # 50001 ~ 50999 TERMINAL层错误码
    "TerminalCommunicationError": {"code": 50001, "msg": "终端通信错误"},
    "OnlineDoNotDeleteError": {"code": 50002, "msg": "终端在线不允许删除"},
    "RedisServerError": {"code": 50003, "msg": "Redis服务异常"},
    "RequestParamError": {"code": 50004, "msg": "请求参数异常"},
    "TerminalConfigNotFound": {"code": 50005, "msg": "终端配置信息不存在"},

    # 60001 ~ VOI TERMINAL 错误码
    "TerminalTokenError": {"code": 60000, "msg": "终端请求TOKEN错误"},
    "TerminalLoginFail": {"code": 60001, "msg": "终端登录失败"},
    "TerminalNotLogin": {"code": 60002, "msg": "终端没有登录"},
    "TerminalTypeError": {"code": 60003, "msg": "终端类型错误"},
    "TerminalIdError": {"code": 60004, "msg": "终端序号错误"},
    "TerminalMacError": {"code": 60005, "msg": "终端MAC错误"},
    "TerminalMaskError": {"code": 60006, "msg": "终端子网掩码错误"},
    "TerminalGatewayError": {"code": 60007, "msg": "终端网关错误"},
    "TerminalDns1Error": {"code": 60008, "msg": "终端域名解析地址错误"},
    "TerminalNameError": {"code": 60009, "msg": "终端名称错误"},
    "TerminalPlatformError": {"code": 60010, "msg": "终端CPU架构名称错误"},
    "TerminalSoftVersionError": {"code": 60011, "msg": "终端软件版本错误"},
    "TerminalModeTypeError": {"code": 60012, "msg": "终端默认桌面模式类型错误"},
    "TerminalModeAutoDesktopError": {"code": 60013, "msg": "终端模式自动登录设置错误"},
    "TerminalServerIpError": {"code": 60014, "msg": "终端连接服务器IP错误"},
    "TerminalConfVersionError": {"code": 60015, "msg": "终端配置版本号错误"},
    "TerminalRepeatLogin": {"code": 60016, "msg": "终端重复登录错误"},
    "TerminalNotConnectError": {"code": 60017, "msg": "终端未链接"},
    "TerminalOrderIdLittleStartId": {"code": 60018, "msg": "终端确认排序号小于起始编号"},
    "TerminalOrderMacError": {"code": 60019, "msg": "终端确认排序的MAC地址不在本次排序回话中"},
    "TerminalAlreadyOrdered": {"code": 60020, "msg": "终端已经排完序号"},
    "TorrentFileNotExist": {"code": 60021, "msg": "终端未链接"},
    "UserOrPasswordError": {"code": 60022, "msg": "用户名或密码错误"},
    "BtResponseMsgError": {"code": 60023, "msg": "报文错误"},
    "TerminalDesktopNotExist": {"code": 60024, "msg": "桌面信息不存在"},
    "TerminalRecordNotExist": {"code": 60025, "msg": ""},
    "TerminalDesktopIpOrderError": {"code": 60026, "msg": ""},
    "TerminalAddBtTaskError": {"code": 60027, "msg": ""},
    "TerminalTorrentUploadFail": {"code": 60028, "msg": "终端种子文件上传失败"},
    "TerminalBtTaskNotExist": {"code": 60029, "msg": "终端BT任务不存在"},
    "UploadDeviceNotExist": {"code": 60030, "msg": "终端上传的磁盘不存在"},
    "TerminalUpgradepagNotExist": {"code": 60031, "msg": "终端升级包不存在"},
    "TorrentCreateFail": {"code": 60032, "msg": "终端种子文件生成失败"},
    "TerminalBtUploadTaskNotExist" : {"code": 60033, "msg": "终端上传任务不存在"},

    "MessageError": {"code": 88888, "msg": "报文错误，请修正重试"},
    "ComputeServiceUnavaiable": {"code": 80000, "msg": "节点 {ipaddr} compute服务连接失败"},
    "ComputeServiceTimeout": {"code": 80001, "msg": "节点 {ipaddr} compute服务连接超时"},
    "UpgradeServiceTimeout": {"code": 80002, "msg": "节点 {ipaddr} upgrade服务连接超时"},
    "MonitorServiceUnavaiable": {"code": 88889, "msg": "节点 {ipaddr} monitor服务连接失败"},
    "TerminalServiceUnavaiable": {"code": 88890, "msg": "terminal管理服务连接失败"},
    "UpgradeServiceUnavailable": {"code": 88891, "msg": "upgrade服务连接失败"},

    "LicenseReadError": {"code": 99994, "msg": "试用授权文件读取异常"},
    "UkeyOpenFailError": {"code": 99995, "msg": "UKEY打开失败"},
    "UkeyNotFunctionError": {"code": 99996, "msg": "UKEY服务接口不存在"},
    "UkeyNotFoundError": {"code": 99997, "msg": "UKEY检测失败"},
    "AuthActiveFailError": {"code": 99998, "msg": "授权激活失败"},
    "SystemError": {"code": 99999, "msg": "系统异常，请稍后重试"},
    "OtherError": {"code": -1, "msg": "未知异常"},

    # 70000 ~  错误码
    "UpgradeRequestParamError": {"code": 70000, "msg": "请求参数异常"},
    "UpgradeReturnError": {"code": 70001, "msg": "返回值异常"},
    "ImageTaskRunning": {"code": 70002, "msg": "目前基础镜像或模板差异盘正处于同传任务中，暂不允许系统升级，请稍候"},
    "TerminalTaskRunning": {"code": 70003, "msg": "目前终端升级包处于同传任务中，暂不允许系统升级，请稍候"},
    "NoPackageToUpload": {"code": 70004, "msg": "请上传升级包"},
    "PackageTypeError": {"code": 70005, "msg": "不支持该类型的升级包"},
    "UpgradePackageSaveError": {"code": 70006, "msg": "升级包上传失败"},
    "UpgradePackageFormatError": {"code": 70007, "msg": "升级包格式错误"},
    "PackageNotMatchSystem": {"code": 70008, "msg": "升级包与当前版本不匹配"},
    "UploadPackageSyncError": {"code": 70009, "msg": "升级包分发失败"},
    "UpgradePackageMd5Failed": {"code": 70010, "msg": "升级包md5校验失败"},
    "StopServiceError": {"code": 70011, "msg": "停止服务{service}失败"},
    "StopSlavesServiceError": {"code": 70011, "msg": "停止计算节点服务失败"},
    "UpgradeBackupFailed": {"code": 70012, "msg": "服务备份失败"},
    "CopyFileFailed": {"code": 70013, "msg": "升级文件拷贝失败"},
    "RunUpgradeScriptFailed": {"code": 70014, "msg": "升级脚本运行失败"},
    "StartServiceError": {"code": 70015, "msg": "服务{service}启动失败"},
    "UpgradeSlavesError": {"code": 70016, "msg": "计算节点升级失败"},
    "RollbackServiceError": {"code": 70017, "msg": "回滚服务失败"},
    "RollbackUpgradeError": {"code": 70018, "msg": "回滚升级失败"},
    "RunRollbackScriptFailed": {"code": 70019, "msg": "回滚脚本运行失败"},
    "UpgradeSelfTimeout": {"code": 70020, "msg": "升级服务自升级超时"},

    # terminal 返回错误码
    "TerminalDesktopNotNeedUpdate": {"code": 100001, "msg": "VOI终端桌面不需要下载更新"},
}


def get_error_result(error="Success", data=None, msg="cn", **kwargs):
    error_code = deepcopy(ERROR_CODE)
    error_msg = error_code.get(error, error_code.get("OtherError"))
    message = error_msg['msg'].format(**kwargs)
    if data is not None and isinstance(data, (dict, list, str)):
        error_msg.update({"data": data})
    if msg == "cn":
        error_msg['msg'] = message
    elif msg == "en":
        error_msg["msg"] = error
    else:
        error_msg['msg'] = message
        error_msg['en_msg'] = error
    return error_msg


def get_error_name(err_code):
    for k, v in ERROR_CODE.items():
        if v.get("code", -1) == err_code:
            return k
    return "OtherError"
