# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import psycopg2


class PostgresHandler(object):
    def __init__(self):
        self.db = psycopg2.connect(host="192.168.10.200", user="postgres", password="postgres", database="region_db")

    def insert(self,province, code, name, type):
        try:
            with self.db.cursor() as cursor:
                cursor.execute('INSERT INTO region'+province+' (code,name,type) VALUES (%s,%s,%s)', [code,name,type])
            self.db.commit()
        except Exception as e:
            raise Exception('Postgres ERROR:', e)

    def create(self, province):
        try:
            with self.db.cursor() as cursor:
                cursor.execute('create table region'+province+' as select * from region where 1=0')
        except Exception as e:
            raise Exception('Postgres ERROR:', e)

    def close(self):
        self.db.close()
