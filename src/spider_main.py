# !/usr /bin/env  python3
# -*- coding: utf-8    -*-
from mysql_handler import MysqlHandler
from html_downloader import HtmlDownloader
from html_parser import HtmlParser
import traceback
import os


class CodeSpider(object):
    def __init__(self):
        self.mysql_handler = MysqlHandler()
        self.html_downloader = HtmlDownloader()
        self.html_parser = HtmlParser()
        self.root_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html'
        self.split_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/'
        self.province_url_list = []
        self.city_url_list = []
        self.county_url_list = []
        self.town_url_list = []
        self.url_list_502 = []

    def craw(self):
        try:
            downloading_url = self.root_url
            html_content = self.html_downloader.download(downloading_url)
            self.province_url_list = self.html_parser.province_parser(html_content, self.split_url)
            for province_name, province_url, province_code in self.province_url_list:
                self.mysql_handler.insert("",province_name,"")
                downloading_url = province_url
                html_content = self.html_downloader.download(downloading_url)
                self.city_url_list = self.html_parser.city_parser(html_content, self.split_url)
                for city_name, city_url, city_code in self.city_url_list:
                    self.mysql_handler.insert(city_code,city_name,"")
                    if city_url is None:
                        continue
                    downloading_url = city_url
                    html_content = self.html_downloader.download(downloading_url)
                    self.county_url_list = self.html_parser.county_parser(html_content, self.split_url + province_code + "/")
                    for county_name, county_url, county_code in self.county_url_list:
                        self.mysql_handler.insert(county_code, county_name,"")
                        if county_url is None:
                            continue
                        downloading_url = county_url
                        html_content = self.html_downloader.download(downloading_url)
                        self.town_url_list = self.html_parser.town_parser(html_content, os.path.dirname(downloading_url) + '/')
                        for town_name,town_url, town_code in self.town_url_list:
                            print(town_name, town_url,town_code)
                            self.mysql_handler.insert(town_code, town_name, "")
                            if town_url is None:
                                continue
                            downloading_url = town_url
                            html_content = self.html_downloader.download(downloading_url)
                            self.village_url_list = self.html_parser.village_parser(html_content, os.path.dirname(downloading_url) + '/')
                            for village_name, village_code, village_type in self.village_url_list:
                                print(village_name, village_code, village_type)
                                self.mysql_handler.insert(village_code, village_name, village_type)
            self.mysql_handler.close()
        except Exception as e:
            print('[ERROR] Craw Field!Url:', downloading_url, 'Info:', e)
            traceback.print_exc()

if __name__ == '__main__':
    obj_spider = CodeSpider()
    obj_spider.craw()
