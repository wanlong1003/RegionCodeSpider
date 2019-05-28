# !/usr /bin/env  python3
# -*- coding: utf-8    -*-
# 从 国家地名信息库 获取区划的边界坐标数据
# http://dmfw.mca.gov.cn/index.html

import psycopg2
import traceback
import os
import time
import json
import urllib.request
import urllib.error
import time

# 直辖市没有市级数据， 海口和三亚的需要单独处理
# 1101 北京   1201 天津   5001 重庆 3101 上海  4601 海口  4602 三亚
code2 = '4602'
db = psycopg2.connect(host="192.168.10.200", user="postgres", password="postgres", database="region_db")
request = urllib.request.Request("http://dmfw.mca.gov.cn:9091/subject/city/"+code2+".json")
with urllib.request.urlopen(request) as response:
    if response.getcode() != 200:
        print(response.read())
    else:
        result = json.loads(response.read())
        features3 = result['features']
        for data in features3:                                            
            try:
                code3 = data['properties']['XZQH']
                name3 = data['properties']['TSMC']
                coordinates3 = json.dumps(data['geometry']['coordinates'])
                print(code3, name3)
                with db.cursor() as cursor:
                    cursor.execute('INSERT INTO region_coordinates (code,name,coordinates) VALUES (%s,%s,%s)', [code3,name3,coordinates3])
                db.commit()
            except Exception as e:
                print(e)