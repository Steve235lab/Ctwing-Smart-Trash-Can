# -*- coding: utf-8 -*-
"""
get_device_statics.py

Created on Sat Feb  5 16:46:28 2022

@author: Steve D. J.

Copyright (c) 2022 Steve D. J.. All Rights Reserved.
"""


#import sys
#sys.path.append('..')
import apis.aep_device_status
import apis.aep_device_command
import base64
import time
import numpy as np
import pandas as pd
import json


def crc16(x, invert):
    a = 0xFFFF
    b = 0xA001
    for byte in x:
        a ^= ord(byte)
        for i in range(8):
            last = a % 2
            a >>= 1
            if last == 1:
                a ^= b
    s = hex(a).upper()
    
    return s[4:6]+s[2:4] if invert == True else s[2:4]+s[4:6]


def sent_rsp_msg(msg):
    msg_b64 = str(base64.b64encode(msg.encode('utf-8')), 'utf-8')
    
    content = {"dataType": 1,"yload": msg_b64}	
        
    body = {"content": content,
            "deviceId": "",
            "operator": "get_device_statics.py by Steve D. J.",
            "productId": ,
            "ttl": 7200,
            "level": 1
            }
    
    body = json.dumps(body)
    result = apis.aep_device_command.CreateCommand('', '', '', body)
    print('result='+str(result))


def update_info():
    global msgType, open_time, open_seconds, present_type, type_ct_list, uFull, faultreport_time, faultType, restarttime, uptime, weights, volumes, oneday_time, offline_flag, info_cache, Latitude, Longitude
    
    # 接收信息并提取有效内容
    try:
        raw_info = apis.aep_device_status.QueryDeviceStatusList('', '', '{"productId":"","deviceId":""}')
    except:
        offline_flag = 1
        return -1
    offline_flag = 0
    raw_info_str = str(raw_info)
    val_start_point = raw_info_str.find('value') + 8
    val_end_point = raw_info_str.find('timestamp') - 3
    value = raw_info_str[val_start_point : val_end_point]
    # base64解码
    value_decode = base64.b64decode(value)
    value_decode_str = str(value_decode)
    #print(value_decode_str)

    # 判断接收的信息是否是新信息
    if value_decode_str == info_cache:
        return 1
    else:
        info_cache = value_decode_str
        f=open('info_cache.txt', 'w')
        f.write(info_cache)
        f.close()
                        
        # 提取消息类型信息
        type_start_point = value_decode_str.find('msgType') + 8
        type_end_point = value_decode_str.find('LjtId') - 1
        msgType = value_decode_str[type_start_point : type_end_point]
        #print("msgType", msgType)
                
        # 开盖上报数据提取
        if msgType == 'opentime':
            # 读取开盖时间
            open_time_sp = value_decode_str.find(',time') + 6
            open_time_ep = value_decode_str.find('seconds') - 1
            open_time = value_decode_str[open_time_sp : open_time_ep]
            # 读取开盖持续时间
            open_seconds_sp = value_decode_str.find('seconds') + 8
            open_seconds_ep = value_decode_str.find('type') - 1 
            open_seconds_str = value_decode_str[open_seconds_sp : open_seconds_ep]
            open_seconds = int(open_seconds_str)
            # 读取投放垃圾类型
            type_sp = value_decode_str.find('type') + 5
            type_ep = value_decode_str.find('crc') - 1
            type_str = value_decode_str[type_sp:type_ep]
            present_type = int(type_str)
            type_ct_list[present_type-1] = type_ct_list[present_type-1] + 1
            # 提取uCode
            uCode_start_point = value_decode_str.find('uCode') + 6
            uCode_end_point = value_decode_str.find(',time')
            uCode = value_decode_str[uCode_start_point : uCode_end_point]
            
        # 心跳、桶满数据、经纬度信息提取
        if msgType == 'heartbeat':
            # 读取桶满状态
            uFull_sp =  value_decode_str.find('uFull') + 6
            uFull_str = value_decode_str[uFull_sp : uFull_sp+1]
            uFull = int(uFull_str)
            # 读取经纬度信息
            Latitude_sp = value_decode_str.find('nLatitude') + 10
            Latitude_ep = value_decode_str.find('nLongitude') - 1
            Latitude = value_decode_str[Latitude_sp: Latitude_ep]
            Longitude_sp = value_decode_str.find('nLongitude') + 11
            Longitude_ep = value_decode_str.find('ver') - 1
            Longitude = value_decode_str[Longitude_sp : Longitude_ep]
            # 提取uCode
            uCode_start_point = value_decode_str.find('uCode') + 6
            uCode_end_point = value_decode_str.find(',uFull')
            uCode = value_decode_str[uCode_start_point : uCode_end_point]
    
        # 故障上报数据提取
        if msgType == 'faultreport':
            # 读取故障上报时间
            faultreport_time_sp = value_decode_str.find(',time') + 6
            faultreport_time_ep = value_decode_str.find('type') - 1
            faultreport_time = value_decode_str[faultreport_time_sp : faultreport_time_ep]
            # 读取故障类型
            faultType_sp = value_decode_str.find('type') + 5
            faultType_ep = value_decode_str.find('crc') - 1
            faultType = value_decode_str[faultType_sp : faultType_ep]
            # 提取uCode
            uCode_start_point = value_decode_str.find('uCode') + 6
            uCode_end_point = value_decode_str.find(',time')
            uCode = value_decode_str[uCode_start_point : uCode_end_point]
    
        # 重启上报数据提取
        if msgType == 'restarttime':
            # 读取重启上报时间
            restarttime_sp = value_decode_str.find(',time') + 6
            restarttime_ep = value_decode_str.find('ver') - 1
            restarttime = value_decode_str[restarttime_sp : restarttime_ep]
            # 提取uCode
            uCode_start_point = value_decode_str.find('uCode') + 6
            uCode_end_point = value_decode_str.find(',time')
            uCode = value_decode_str[uCode_start_point : uCode_end_point]
            
        # 换桶上报数据提取
        if msgType == 'uptime':
            # 读取换桶时间
            uptime_sp = value_decode_str.find(',time') + 6
            uptime_ep = value_decode_str.find('weights') - 1
            uptime = value_decode_str[uptime_sp : uptime_ep]
            # 读取重量
            weights_sp = value_decode_str.find('weights') + 8
            weights_ep = value_decode_str.find('volumes') - 1
            weights_str = value_decode_str[weights_sp : weights_ep]
            weights = int(weights_str)
            # 读取体积
            volumes_sp = value_decode_str.find('volumes') + 8
            volumes_ep = value_decode_str.find('ver') - 1
            volumes_str = value_decode_str[volumes_sp : volumes_ep]
            volumes = int(volumes_str)
            # 提取uCode
            uCode_start_point = value_decode_str.find('uCode') + 6
            uCode_end_point = value_decode_str.find(',time')
            uCode = value_decode_str[uCode_start_point : uCode_end_point]

        # 按日上报数据提取
        if msgType == 'oneday':
            # 读取每日上报时间
            uptime_sp = value_decode_str.find(',time') + 6
            uptime_ep = value_decode_str.find('weights') - 1
            oneday_time = value_decode_str[uptime_sp : uptime_ep]
            # 读取重量
            weights_sp = value_decode_str.find('weights') + 8
            weights_ep = value_decode_str.find('volumes') - 1
            weights_str = value_decode_str[weights_sp : weights_ep]
            weights = int(weights_str)
            # 读取体积
            volumes_sp = value_decode_str.find('volumes') + 8
            volumes_ep = value_decode_str.find('ver') - 1
            volumes_str = value_decode_str[volumes_sp : volumes_ep]
            volumes = int(volumes_str)
            # 提取uCode
            uCode_start_point = value_decode_str.find('uCode') + 6
            uCode_end_point = value_decode_str.find(',time')
            uCode = value_decode_str[uCode_start_point : uCode_end_point]
        
        msgType_rsp = msgType + 'rsp'
        msg = '<msgType=' + msgType_rsp + ',LjtId=LB2110N001,sCode=OK,uCode=' + uCode + ','
        crc = crc16(msg, False)
        msg = msg + 'crc=' + crc + ',>\r\n'
        sent_rsp_msg(msg)
        
        return 0


if __name__ == '__main__':
    
    global msgType, open_time, open_seconds, present_type, type_ct_list, uFull, faultreport_time, faultType, restarttime, uptime, weights, volumes, oneday_time, offline_flag, info_cache, Latitude, Longitude
    offline_flag = 0
    # 定义基本数据
    msgType = ''
    open_time = ''
    open_seconds = 0
    present_type = 1                # type=1干垃圾，type=2湿垃圾，type=3可回收垃圾，type=4有害垃圾
    type_ct_list = [0, 0, 0, 0]
    uFull = 0                       # uFull: 0, 不满；1，全满；2半满
    faultreport_time = ''
    faultType = 'healthy'           # Open开盖故障，close关盖故障，up上升故障，down下降故障
    restarttime = ''
    uptime = ''
    weights = 0
    volumes = 0
    oneday_time = ''
    Latitude = ''
    Longitude = ''
    
    f = open('info_cache.txt', 'r')
    info_cache = f.read()
    f.close()
    
    while(True):
        time.sleep(0.1)
        
        if update_info() == 0:
            # 数据打包
            data = pd.read_excel('data.xlsx', index_col = None, header = 0)
            # 校验最新日期与数据文件中最后的日期，如果不同则添加新日期
            date_old = data.loc[:, '日期']
            date_list = []
            for i in date_old:
                temp = str(i)
                if temp != '':
                    date_list.append(temp)
            date_last = date_list[-1]
            date_last = date_last[0:10]
            latest_time = ''
            for i in [open_time, faultreport_time, restarttime, oneday_time]:
                if i != '':
                    latest_time = i
            if latest_time != '':
                date_latest = latest_time[0:10]
            if date_latest != date_last:
                data = data.append([{'日期':date_latest}], ignore_index=True) 
            # 最后一次开盖时间
            data.iloc[-1, 1] = open_time
            # 日开盖次数
            if msgType == 'opentime':
                if np.isnan(data.iloc[-1, 2]):
                    data.iloc[-1, 2] = 1
                else:
                    data.iloc[-1, 2] = int(data.iloc[-1, 2]) + 1
            # 开盖持续时间（是当日开盖持续时间的和）
            if np.isnan(data.iloc[-1, 3]):
                data.iloc[-1, 3] = open_seconds
            else:
                data.iloc[-1, 3] = int(data.iloc[-1, 3]) + open_seconds
            # 当前垃圾类型
            data.iloc[-1, 4] = present_type
            # 各类型垃圾投放次数统计(假设单次开盖延时5s)
            if msgType == 'opentime':
                for i in range(5, 9):
                    if np.isnan(data.iloc[-1, i]):
                        data.iloc[-1, i] = 0
                if present_type == 1:
                    data.iloc[-1, 5] = data.iloc[-1, 5] + int(open_seconds / 5)
                if present_type == 2:
                    data.iloc[-1, 6] = data.iloc[-1, 6] + int(open_seconds / 5)
                if present_type == 3:
                    data.iloc[-1, 7] = data.iloc[-1, 7] + int(open_seconds / 5)
                if present_type == 4:
                    data.iloc[-1, 8] = data.iloc[-1, 8] + int(open_seconds / 5)
            # 桶满状态
            data.iloc[-1, 9] = uFull
            # 故障类型
            data.iloc[-1, 10] = faultType
            # 故障上报时间
            data.iloc[-1, 11] = faultreport_time
            # 重启上报时间
            data.iloc[-1, 12] = restarttime
            # 换桶时间
            data.iloc[-1, 13] = uptime
            # 垃圾重量
            data.iloc[-1, 14] = weights
            # 垃圾体积
            data.iloc[-1, 15] = volumes
            # 每日上报时间
            data.iloc[-1, 16] = oneday_time
            # 经纬度
            data.iloc[-1, 17] = Longitude
            data.iloc[-1, 18] = Latitude
            
            #写入data.xlsx
            writer = pd.ExcelWriter('data.xlsx')
            data.to_excel(writer, sheet_name = 'Sheet1', index = False, header = ['日期', '最后一次开盖时间', '日开盖次数', '开盖持续时间', '当前垃圾类型', '干垃圾投放次数', '湿垃圾投放次数', '可回收垃圾投放次数', '有害垃圾投放次数', '桶满状态', '故障类型', '故障上报时间', '重启上报时间', '换桶时间', '垃圾重量', '垃圾体积', '每日上报时间', '经度', '纬度'])
            writer.save()
            
        elif(update_info() == -1): 
           print("检测到计算机已离线，请连接到网络后再试")
    
