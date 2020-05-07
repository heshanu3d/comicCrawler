import unittest
import re
from animezilla import *

from animezilla import book_done
from net_util import *
import collections
import socket
import socks
import requests

#added sth for repo update

class MyTestCase(unittest.TestCase):
    def test_page_download_thread(self):
        threads = []
        web_url = 'https://18h.animezilla.com/manga/3783'
        dir_path = 'unit-test'
        totalPage = 209
        PAGE_DOWNLOAD_THREAD_NUM = 3
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
            print('mkdir %s\n' % dir_path)
        if (totalPage > 1):
            for i in range(1, totalPage + 1):
                img_filename = '%s\\%d.jpg' % (dir_path, i)
                if not os.path.exists(img_filename):
                    thread_loop(threads, page_download, (web_url, dir_path, i,), PAGE_DOWNLOAD_THREAD_NUM)
                    print('start downloading %s ...\n' % img_filename)
                else:
                    print('%s exists\n' % img_filename)
    def test_page_download(self):
        web_url = 'https://18h.animezilla.com/manga/1768'
        dir_path = 'unit-test'
        i = 2
        page_download(web_url, dir_path, i)
    def test_book_manage(self):
        dir_path = os.path.abspath(os.path.join(os.getcwd(), "../comicCrawler_out"))
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
            print('mkdir %s\n' % dir_path)
        web_url = 'https://18h.animezilla.com/manga/1768'
        book_done_list = []
        book_manage(web_url,book_done_list,dir_path)
    def test_book_manage_process(self):
        dir_path = os.path.abspath(os.path.join(os.getcwd(), "../comicCrawler_out"))
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
            print('mkdir %s\n' % dir_path)
        book_list = ['https://18h.animezilla.com/manga/3783', \
                     'https://18h.animezilla.com/manga/3775', \
                     'https://18h.animezilla.com/manga/3777', \
                     'https://18h.animezilla.com/manga/3773', \
                     'https://18h.animezilla.com/manga/3766', \
                     'https://18h.animezilla.com/manga/3757']
        book_done_list = []
        BOOK_MANAGE_THREAD_NUM = 3
        proceeds = []
        totalBook = len(book_list)
        if totalBook > 0:
            for i in range(totalBook):
                process_loop(proceeds, book_manage, (book_list[i],book_done_list,dir_path,), BOOK_MANAGE_THREAD_NUM)
    def test_book_done(self):
        dir_path = os.path.abspath(os.path.join(os.getcwd(), "../comicCrawler_out"))
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
            print('mkdir %s\n' % dir_path)
        book_done_list = []
        book_done(book_done_list, dir_path)
        # for d in book_done_list:
        #     print('%s' % d)
    def test_init_cat_dic(self):
        url = 'https://18h.animezilla.com/'
        # 获取category_list
        category_dict = collections.defaultdict(list)
        category_dict[url] = 'F'
        category_list = []
        init_cat_dic(category_dict, category_list)
    def test_dir_name(self):
        s = '[中文H漫][うえかん] 好きのサインは\/喜歡的微兆是? [200P]'
        # os.mkdir(s)
        print(s)
        s = re.sub(r'[/\\:*?"<>|]', ' ', s)
        print(s)
        # os.mkdir(s)
    def test_search_book_link(self):
        category_list = \
            ['https://18h.animezilla.com/', \
             'https://18h.animezilla.com/doujinshi', \
             'https://18h.animezilla.com/doujinshi/original', \
             'https://18h.animezilla.com/doujinshi/page/2', \
             'https://18h.animezilla.com/doujinshi/page/3', \
             'https://18h.animezilla.com/doujinshi/page/4', \
             'https://18h.animezilla.com/doujinshi/page/5', \
             'https://18h.animezilla.com/doujinshi/page/6', \
             'https://18h.animezilla.com/doujinshi/page/7', \
             'https://18h.animezilla.com/doujinshi/parody', \
             'https://18h.animezilla.com/doujinshi/parody/page/2', \
             'https://18h.animezilla.com/doujinshi/parody/page/3', \
             'https://18h.animezilla.com/doujinshi/parody/page/4', \
             'https://18h.animezilla.com/doujinshi/parody/page/5', \
             'https://18h.animezilla.com/doujinshi/parody/page/6', \
             'https://18h.animezilla.com/doujinshi/parody/page/7', \
             'https://18h.animezilla.com/manga', \
             'https://18h.animezilla.com/manga/page/10', \
             'https://18h.animezilla.com/manga/page/11', \
             'https://18h.animezilla.com/manga/page/12', \
             'https://18h.animezilla.com/manga/page/13', \
             'https://18h.animezilla.com/manga/page/14', \
             'https://18h.animezilla.com/manga/page/15', \
             'https://18h.animezilla.com/manga/page/16', \
             'https://18h.animezilla.com/manga/page/17', \
             'https://18h.animezilla.com/manga/page/18', \
             'https://18h.animezilla.com/manga/page/2', \
             'https://18h.animezilla.com/manga/page/3', \
             'https://18h.animezilla.com/manga/page/4', \
             'https://18h.animezilla.com/manga/page/5', \
             'https://18h.animezilla.com/manga/page/6', \
             'https://18h.animezilla.com/manga/page/7', \
             'https://18h.animezilla.com/manga/page/8', \
             'https://18h.animezilla.com/manga/page/9']
        book_list = []
        for cateIndex in range(len(category_list)):
            search_book_link(category_list[cateIndex], book_list)
        print('book_list length:', len(book_list))
    def test_book_done_err(self):
        dir_path = '1977-[中文同人H漫][酒呑童子] 18号が催眠でNTRれる本 (七龍珠Z)'
        dir_path = '1057-[中文同人H漫][6ro-] 七瀬さんに横恋慕 (金田一少年之事件簿)'
        dir_path = '1613-[中文同人H漫][YU-RI] 黒蝶乱舞 (死神Bleach)'
        book_totalpage_pre = dir_path.rfind('[')
        book_totalpage_aff = dir_path.rfind(']')
        if book_totalpage_pre == -1 or book_totalpage_aff == -1 or not dir_path[book_totalpage_pre + 1:book_totalpage_aff - 1].isdigit():
            print(1)
        else:
            print(0)
    def test_totalpage_notequal_err(self):
        s = '[中文H漫][うえかん] 好きのサインは\/喜歡的微兆是? [200P]'
        print(s)
        totalpage = 123
        s = re.sub(r'(\[(\d+)P\])$', '[%dP]'%totalpage, s)
        print(s)
    def test_pysocks(self):
        proxy = {
            'http': 'http://127.0.0.1:1080',
            'https': 'https://127.0.0.1:1080'
        }
        try:
            print(requests.get('https://18h.animezilla.com/manga/1768', proxies=proxy).text)
            # print(requests.get('https://18h.animezilla.com/manga/1768').text)
        except requests.exceptions.ProxyError:
            print('requests.exceptions.ProxyError')
        except requests.exceptions.ConnectionError:
            print('requests.exceptions.ConnectionError')
    def test_try_except(self):
        proxy = {
            'http': 'http://127.0.0.1:1081',
            'https': 'https://127.0.0.1:1081'
        }
        try:
            print(requests.get('https://18h.animezilla.com/manga/1768', proxies=proxy).text)
            # print(requests.get('https://18h.animezilla.com/manga/1768').text)
        except requests.exceptions.ProxyError:
            print('requests.exceptions.ProxyError')
        except requests.exceptions.ConnectionError:
            print('requests.exceptions.ConnectionError')
    def test_request_get_decode(self):
        proxy = {
            'http': 'http://127.0.0.1:1081',
            'https': 'https://127.0.0.1:1081'
        }
        web_url = 'https://18h.animezilla.com/manga/3689/2'
        web_data = requests_get(web_url, proxies=proxy)
        print(web_data)
        if web_data:
            html = etree.HTML(web_data)
            img_url = html.xpath("//div[@id='page-current']//img/@src")
            print(img_url)


if __name__ == '__main__':
    unittest.main()
