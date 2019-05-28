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

db = psycopg2.connect(host="192.168.10.200", user="postgres", password="postgres", database="region_db")
request = urllib.request.Request("http://dmfw.mca.gov.cn:9091/subject/china.json")
with urllib.request.urlopen(request) as response:
    if response.getcode() != 200:
        print(response.read())
    else:
        result = json.loads(response.read())
        features1 = result['features']
        for data in features1:          
            try:
                code1 = data['properties']['CODE']
                name1 = data['properties']['NAME']
                coordinates1 = json.dumps(data['geometry']['coordinates'])
                print(code1, name1)                
                with db.cursor() as cursor:
                    cursor.execute('INSERT INTO region_coordinates (code,name,coordinates) VALUES (%s,%s,%s)', [code1,name1,coordinates1])
                db.commit()
                request = urllib.request.Request("http://dmfw.mca.gov.cn:9091/subject/"+code1+".json")
                with urllib.request.urlopen(request) as response:
                    if response.getcode() != 200:
                        print(response.read())
                    else:
                        result = json.loads(response.read())
                        features2 = result['features']
                        for data in features2:
                            try:
                                code2 = data['properties']['code']
                                name2 = data['properties']['name']
                                coordinates2 = json.dumps(data['geometry']['coordinates'])
                                print(code2, name2)
                                with db.cursor() as cursor:
                                    cursor.execute('INSERT INTO region_coordinates (code,name,coordinates) VALUES (%s,%s,%s)', [code2,name2,coordinates2])
                                db.commit()
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
                            except Exception as e:
                                print(e)
                            time.sleep(1)
            except Exception as e:
                print(e)
            time.sleep(3)