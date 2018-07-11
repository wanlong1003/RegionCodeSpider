# !/usr/bin/env  python3
# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import time


class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            raise Exception('url is None')
        print(url)
        request = urllib.request.Request(url, None, {'Cookie': 'AD_RS_COOKIE=20083363',
                                                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                                                     AppleWeb\Kit/537.36 (KHTML, like Gecko)\
                                                      Chrome/58.0.3029.110 Safari/537.36'})
        try:
            with urllib.request.urlopen(request) as response:
                print(response.getcode())
                if response.getcode() != 200:
                    time.sleep(5)
                    return self.download(url)
                else:
                    return response.read()
        except urllib.error.HTTPError as e:
            print(e)
            time.sleep(5)
            return self.download(url)
