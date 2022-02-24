#!/usr/bin/python
# encoding=utf-8

import sys
if sys.version_info[0] == 2:
    # Python2
    import core.AepSdkRequestSend as AepSdkRequestSend
else:
    # Python3
    from apis.core import AepSdkRequestSend



#参数body: 类型json, 参数不可以为空
#  描述:body,具体参考平台api说明
def QueryDeviceStatus(appKey, appSecret, body):
    path = '/aep_device_status/deviceStatus'
    head = {}
    param = {}
    version = '20181031202028'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, body, version, application, None, key, 'POST')
    if response is not None:
        return response.read()
    return None

#参数body: 类型json, 参数不可以为空
#  描述:body,具体参考平台api说明
def QueryDeviceStatusList(appKey, appSecret, body):
    path = '/aep_device_status/deviceStatusList'
    head = {}
    param = {}
    version = '20181031202403'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, body, version, application, None, key, 'POST')
    if response is not None:
        return response.read()
    return None

#参数body: 类型json, 参数不可以为空
#  描述:body,具体参考平台api说明
def getDeviceStatusHisInTotal(appKey, appSecret, body):
    path = '/aep_device_status/api/v1/getDeviceStatusHisInTotal'
    head = {}
    param = {}
    version = '20190928013529'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, body, version, application, None, key, 'POST')
    if response is not None:
        return response.read()
    return None

#参数body: 类型json, 参数不可以为空
#  描述:body,具体参考平台api说明
def getDeviceStatusHisInPage(appKey, appSecret, body):
    path = '/aep_device_status/getDeviceStatusHisInPage'
    head = {}
    param = {}
    version = '20190928013337'
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, body, version, application, None, key, 'POST')
    if response is not None:
        return response.read()
    return None

