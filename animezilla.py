# coding:utf-8

import io
import os
from fake_useragent import UserAgent
from lxml import etree

from PIL import Image
import re

# python2
# from Queue import Empty, Full
# python3
from queue import Empty, Full
from multiprocessing import Queue

from concurrent_util import thread_loop
from concurrent_util import process_loop
from net_util import requests_get
# #######################		下载线程		#################
# 输入：
# 		#url:https://18h.animezilla.com/manga/3689
# 		#page:1-lastPage
# 		#dir_path:3689-xxxxxx [215P]
# 输出:
# 		#3689-xxxxxx [215P]/1.jpg
# 		#3689-xxxxxx [215P]/2.jpg
# 		#...
# 		#3689-xxxxxx [215P]/lastPage.jpg


def page_download(url, dir_path, page):
    # web_url = 'https://18h.animezilla.com/manga/3689/2'
    # img_url = 'https://m.iprox.xyz/s/20190114/004668f1.jpg'
    web_url = url

    if page != 1:
        web_url = '%s/%d' % (url, page)

    # 判断文件存在
    img_filename = '%s\\%d.jpg' % (dir_path, page)
    if not os.path.exists(img_filename):

        # 获取并解析页面
        web_data = requests_get(web_url)
        if not web_data:
            return
        html = etree.HTML(web_data)
        img_url = html.xpath("//div[@id='page-current']//img/@src")
        if img_url:
            img_url = img_url[0]
        else:
            # 最后一页regex变了
            img_url = html.xpath("//div[@class='entry-content']//img/@src")[0]
        # 模拟浏览器
        ua = UserAgent()
        headers = {'User-Agent': ua.random, 'Referer': web_url}
        response = requests_get(img_url, headers=headers)
        if not response:
            return
        # 图片保存
        #img_file = Image.open(io.BytesIO(response.content))
        try:
            img_file = Image.open(io.BytesIO(response))
            img_file.save(img_filename)
            print('%s done!\n' % img_filename)
        except IOError:
            print('image file %s is truncated\n' % img_filename)


# #######################		任务调度线程		#################
# 输入：
# 		#
# 		#
# 		#
# 输出:
# 		#
# 		#
# 		#
# 		#


def book_manage(url, book_done_list, dir):
    PAGE_DOWNLOAD_THREAD_NUM = 3
    web_url = url

    # 书ID!!!
    book_id_rindex = web_url.rfind('/')
    book_id = web_url[book_id_rindex + 1:]
    print('BookManage:resolve book:%s\n' % book_id)
    # 判断是否已经下载完毕
    if book_id in book_done_list:
        print('book %s has been downloaded done before!\n' % book_id)
        return

    # 获取页面资源
    web_url = '%s/2' % url
    web_data = requests_get(web_url, decode='utf-8')
    if not web_data:
        return
    html = etree.HTML(web_data)
    web_url = url

    # 书名!!!
    # python2
    # book_name = html.xpath("//h1[@class='entry-title']//a/text()")[0].encode('gbk','ignore')
    # python3
    book_name = html.xpath("//h1[@class='entry-title']//a/text()")[0]
    print(book_name)
    book_name_index = book_name.rfind('/')
    book_name = book_name[book_name_index + 1:]
    # print('book_name:%s\n'%book_name)

    # totalPage
    title = html.xpath("//h1[@class='entry-title']/text()")[0]
    # print('%s\n' % title)
    rIndex = title.rfind('/')
    totalPage = title[rIndex + 1:]
    # python2
    # totalPage = string.atoi(totalPage)
    # python3
    totalPage = int(totalPage)

    # 创建文件夹!!!
    # 判断书名是否有[pages]否则自己加上，少部分图书采集不到总页数信息
    book_totalpage_pre = book_name.rfind('[')
    book_totalpage_aff = book_name.rfind(']')
    if book_totalpage_pre == -1 or book_totalpage_aff == -1 or not book_name[book_totalpage_pre + 1:book_totalpage_aff - 1].isdigit():
        book_name = '%s[%dP]' % (book_name, totalPage)
    # 去掉文件夹名中的非法字符，参考test_dir_name
    book_name = re.sub(r'[/\\:*?"<>|]', ' ', book_name)
    # 更改文件夹名里的总页数和实际总页数不一致情况，参考test_totalpage_notequal_err
    book_name = re.sub(r'(\[(\d+)P\])$', '[%dP]'%totalPage, book_name)
    dir_path = '%s\%s-%s' % (dir, book_id, book_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        print('mkdir %s\n' % dir_path)

    print('%s has %d pages!\n' % (dir_path, totalPage))
    print('Download begin...\n')

    threads = []
    if totalPage > 1:
        for i in range(1, totalPage + 1):
            img_filename = '%s\\%d.jpg' % (dir_path, i)
            if not os.path.exists(img_filename):
                thread_loop(threads, page_download, (web_url, dir_path, i,), PAGE_DOWNLOAD_THREAD_NUM)
                print('start downloading %s ...\n' % img_filename)
            # else:
            #     print('%s exists\n' % img_filename)


def search_book_link(url, book_list):
    regex_search_book = ['(18h.animezilla.com/manga/\d+)', ]
    web_url = url
    # 书ID!!!
    book_id_rindex = web_url.rfind('/')
    book_id = web_url[book_id_rindex + 1:]
    # print('book_id :%s\n'%book_id)

    # 获取页面资源
    web_data = requests_get(web_url)
    if not web_data:
        return
    html = etree.HTML(web_data)

    # 书链接名!!!
    book_links = html.xpath("//a/@href")
    book_link_num = 0
    for bl in book_links:
        for r in regex_search_book:
            if r and re.findall(r, bl):
                bl_index = bl.find('18h.animezilla.com')
                bl = 'https://%s' % bl[bl_index:]
                if not bl in book_list:
                    book_list.append(bl)
                    book_link_num += 1
    # sort使用查看 https://blog.csdn.net/meiqi0538/article/details/88584497
    book_list.sort(reverse=False)
    for bl in book_list:
        print('%s' % bl)

    print('%s add %d book links\n' % (web_url, book_link_num))
    print('---------------------------------------------')


# #######################		搜索线程		#################
# 输入：
# 		#
# 		#
# 		#
# 输出:
# 		#
# 		#
# 		#
# 		#
# 规则
# 持久层
def search_category(url, category_dict):
    regex_search_category = ['(18h.animezilla.com/topic$)',
                             '(18h.animezilla.com/doujinshi$)',
                             '(18h.animezilla.com/doujinshi/page/\d+$)',
                             '(18h.animezilla.com/manga$)',
                             '(18h.animezilla.com/manga/page/\d+$)',
                             '(18h.animezilla.com/doujinshi/original$)',
                             '(18h.animezilla.com/doujinshi/original/page/\d+$)',
                             '(18h.animezilla.com/doujinshi/parody$)',
                             '(18h.animezilla.com/doujinshi/parody/page/\d+$)']

    web_url = url

    # 获取页面资源
    web_data = requests_get(web_url)
    if not web_data:
        return
    html = etree.HTML(web_data)

    # 书链接名!!!
    links = html.xpath("//a/@href")
    link_num = 0
    for l in links:
        for r in regex_search_category:
            if r and re.findall(r, l):
                l_index = l.find('18h.animezilla.com')
                l = 'https://%s' % l[l_index:]
                if not category_dict[l]:
                    category_dict[l] = 'F'
                    link_num = 1 + link_num
                    print('link:%s' % l)

    print('%s add %d category links\n' % (web_url, link_num))
    print('---------------------------------------------')


def init_cat_dic(category_dict, category_list):
    sflag = True
    while (sflag):
        sflag = False
        for k, v in category_dict.items():
            if v == 'F':
                sflag = True
                category_dict[k] = 'T'
                search_category(k, category_dict)
                break
    for k in sorted(category_dict):
        category_dict[k] = 'F'
        category_list.append(k)
        print(k)


def book_done(book_done_list, dir_path):
    files_dirs = os.listdir(dir_path)
    for d in files_dirs:
        book_id_index = d.find('-')
        if book_id_index != -1:
            jpgs = os.listdir('%s\%s' % (dir_path,d))
            jpg_num = 0
            for jpg in jpgs:
                if jpg.find('.jpg') != -1:
                    jpg_num += 1
            book_page_pre = d.rfind('[')
            book_page_aff = d.rfind(']')
            if book_page_pre != -1 and book_page_aff != -1:
                book_page = d[book_page_pre + 1:book_page_aff - 1]
                print('book %s has downloaded %s(%s total) pages:' % (d[:book_id_index], jpg_num, book_page))
                if int(book_page) == jpg_num:
                    book_done_list.append(d[:book_id_index])
    book_done_num = 0
    for d in book_done_list:
        book_done_num+=1
    print('book_done_num:',book_done_num)

if __name__ == '__main__':
    dir_path = os.path.abspath(os.path.join(os.getcwd(), "..\comicCrawler_out"))
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        print('mkdir %s\n' % dir_path)

    book_done_list = []
    book_done(book_done_list, dir_path)

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

    proceeds = []
    for cateIndex in range(len(category_list)):
        book_list = []
        search_book_link(category_list[cateIndex], book_list)
        BOOK_MANAGE_THREAD_NUM = 10
        totalBook = len(book_list)
        if totalBook > 0:
            for i in range(totalBook):
                # 判断是否已经下载完毕
                book_id = book_list[i][book_list[i].rfind('/') + 1:]
                if not book_id in book_done_list:
                    process_loop(proceeds, book_manage, (book_list[i], book_done_list,dir_path,), BOOK_MANAGE_THREAD_NUM)
                else:
                    print('book %s has been downloaded done before!\n' % book_id)
