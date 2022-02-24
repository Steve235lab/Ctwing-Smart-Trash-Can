#!/usr/bin/python
# encoding=utf-8

import sys
if sys.version_info[0] == 2:
    # Python2
    import core.AepSdkRequestSend as AepSdkRequestSend
else:
    # Python3
    from apis.core import AepSdkRequestSend



#参数MasterKey: 类型String, 参数不可以为空
#  描述:MasterKey在该设备所属产品的概况中可以查看
#参数body: 类型json, 参数不可以为空
#  描述:body,具体参考平台api说明
def CreateCommand(appKey, appSecret, MasterKey, body):
    path = '/aep_device_command/command'
    head = {}
    param = {}
    version = '20190712225145'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, body, version, application, MasterKey, key, 'POST')
    if response is not None:
        return response.read()
    return None

#参数MasterKey: 类型String, 参数不可以为空
#  描述:MasterKey在该设备所属产品的概况中可以查看
#参数productId: 类型long, 参数不可以为空
#  描述:产品ID，必填
#参数deviceId: 类型String, 参数不可以为空
#  描述:设备ID，必填
#参数startTime: 类型String, 参数可以为空
#  描述:日期格式，年月日时分秒，例如：20200801120130
#参数endTime: 类型String, 参数可以为空
#  描述:日期格式，年月日时分秒，例如：20200801120130
#参数pageNow: 类型long, 参数可以为空
#  描述:当前页数
#参数pageSize: 类型long, 参数可以为空
#  描述:每页记录数，最大40
def QueryCommandList(appKey, appSecret, MasterKey, productId, deviceId, startTime, endTime, pageNow, pageSize):
    path = '/aep_device_command/commands'
    head = {}
    param = {'productId':productId, 'deviceId':deviceId, 'startTime':startTime, 'endTime':endTime, 'pageNow':pageNow, 'pageSize':pageSize}
    version = '20200814163736'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, None, version, application, MasterKey, key, 'GET')
    if response is not None:
        return response.read()
    return None

#参数MasterKey: 类型String, 参数不可以为空
#  描述:MasterKey在该设备所属产品的概况中可以查看
#参数commandId: 类型String, 参数不可以为空
#  描述:创建指令成功响应中返回的id，
#参数productId: 类型long, 参数不可以为空
#  描述:
#参数deviceId: 类型String, 参数不可以为空
#  描述:设备ID
def QueryCommand(appKey, appSecret, MasterKey, commandId, productId, deviceId):
    path = '/aep_device_command/command'
    head = {}
    param = {'commandId':commandId, 'productId':productId, 'deviceId':deviceId}
    version = '20190712225241'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, None, version, application, MasterKey, key, 'GET')
    if response is not None:
        return response.read()
    return None

#参数MasterKey: 类型String, 参数不可以为空
#  描述:
#参数body: 类型json, 参数不可以为空
#  描述:body,具体参考平台api说明
def CancelCommand(appKey, appSecret, MasterKey, body):
    path = '/aep_device_command/cancelCommand'
    head = {}
    param = {}
    version = '20190615023142'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, body, version, application, MasterKey, key, 'PUT')
    if response is not None:
        return response.read()
    return None

