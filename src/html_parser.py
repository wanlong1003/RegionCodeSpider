# !/usr/bin/env  python3
# -*- coding: utf-8 -*- 
from bs4 import BeautifulSoup
import re


class HtmlParser(object):
    def province_parser(self, html_content, url):
        if html_content is None:
            raise Exception('Html is None')
        html_content = html_content.decode('gb2312', 'ignore').encode('utf-8')
        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
        url_tds = soup.find_all('a', href=re.compile(r'\d+.html'))
        urls = [(td.get_text(), url + td['href'], td['href'].replace('.html', '')) for td in url_tds]
        return urls

    def city_parser(self, html_content, url):
        if html_content is None:
            raise Exception('Html is None')
        html_content = html_content.decode('gb2312', 'ignore').encode('utf-8')
        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
        url_trs = soup.find_all('tr', 'citytr')
        urls = [(tr.contents[1].get_text() if tr.contents[1].a is None else tr.contents[1].a.get_text(),
                  None if tr.contents[0].a is None else url + tr.contents[0].a['href'],
                 tr.contents[0].get_text() if tr.contents[0].a is None else tr.contents[0].a.get_text())
                for tr in url_trs]
        return urls

    def county_parser(self, html_content, url):
        if html_content is None:
            raise Exception('Html is None')
        html_content = html_content.decode('gb2312', 'ignore').encode('utf-8')
        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
        url_trs = soup.find_all('tr', 'countytr')
        urls = [(tr.contents[1].get_text() if tr.contents[1].a is None else tr.contents[1].a.get_text(),
                  None if tr.contents[0].a is None else url + tr.contents[0].a['href'],
                 tr.contents[0].get_text() if tr.contents[0].a is None else tr.contents[0].a.get_text())
                for tr in url_trs]
        return urls

    def town_parser(self, html_content, url):
        if html_content is None:
            raise Exception('Html is None')
        html_content = html_content.decode('gb2312', 'ignore').encode('utf-8')
        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
        url_trs = soup.find_all('tr', 'towntr')
        urls = [(tr.contents[1].get_text() if tr.contents[1].a is None else tr.contents[1].a.get_text(),
                  None if tr.contents[0].a is None else url + tr.contents[0].a['href'],
                 tr.contents[0].get_text() if tr.contents[0].a is None else tr.contents[0].a.get_text())
                for tr in url_trs]
        return urls

    def village_parser(self, html_content, url):
        if html_content is None:
            raise Exception('Html is None')
        html_content = html_content.decode('gb2312', 'ignore').encode('utf-8')
        soup = BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
        url_trs = soup.find_all('tr', 'villagetr')
        #2017年 360124200210 220 新和村委会 数据中包含俩个'\n'，需要单独处理
        url_trs.remove('\n')
        url_trs.remove('\n')
        urls = [(tr.contents[2].get_text(),
                 tr.contents[0].get_text(),
                 tr.contents[1].get_text())
                for tr in url_trs]
        return urls
