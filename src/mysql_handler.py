# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymysql.cursors


class MysqlHandler(object):
    def __init__(self):
        self.db = pymysql.connect(host="192.168.1.250", user="root", passwd="!QAZ@WSX3edc4rfv", db="qh", charset="utf8", cursorclass=pymysql.cursors.DictCursor)

    def insert(self,province, code, name, type):
        try:
            with self.db.cursor() as cursor:
                cursor.execute('INSERT INTO region'+province+' (code,name,type) VALUES (%s,%s,%s)', [code,name,type])
            self.db.commit()
        except Exception as e:
            raise Exception('MySQL ERROR:', e)

    def create(self, province):
        try:
            with self.db.cursor() as cursor:
                cursor.execute('create table region'+province+' as select * from region where 1=0')
        except Exception as e:
            raise Exception('MySQL ERROR:', e)

    def close(self):
        self.db.close()
