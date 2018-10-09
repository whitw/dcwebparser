import os
import sys
from html_tool import reqsoup
import urllib.request
from urllib.error import HTTPError
from error import print_error_msg
from bs4 import BeautifulSoup
from hdr import header_chrome


def read(
    list_page='http://gall.dcinside.com/'
    + 'list.php?id=programming&=page=1'
):
    soup = reqsoup(list_page, header_chrome)
    if(soup is None):
        return None
    try:
        trs = soup.find("table", {"class": "gall_list"}).tbody.find_all("tr")
    except AttributeError:
        raise AttributeError("Can't access that gallery!")
    result = []

    for tr in trs:
        msg = {"have_img": False, "no": None, "title": None, "comment": None,
               "nick": None, "date": None, "view": None,
               "vote_up": None, "id": None}
        try:
            ub_word = tr.find("td", {"class": "gall_tit"})
            notice = ub_word.em['class'][1]
            msg['title'] = ub_word.a.get_text()
            comment = ub_word.find("a", {"class": "reply_numbox"})
            if(comment is not None):
                msg['comment'] = comment.get_text()[1:-1]
            else:
                msg['comment'] = '0'
            if(notice == 'icon_notice'):
                continue
            elif(notice == 'icon_img'):
                msg['have_img'] = True
            else:
                msg['have_img'] = False
        except Exception as e:
            print_error_msg(e)
        try:
            msg['no'] = tr.find("td", {"class": "gall_num"}).get_text()
            nick = tr.find("td", {"class": "gall_writer"})
            msg['nick'] = nick['data-nick']
            msg['date'] = tr.find("td", {"class": "gall_date"}).get_text()
            msg['view'] = tr.find("td", {"class": "gall_count"}).get_text()
            vote_up = tr.find("td", {"class": "gall_recommend"})
            msg['vote_up'] = vote_up.get_text()
        except AttributeError as e:
            continue
        else:
            result.append(msg)
    return result


def search(
    gallery,
    keyword,
    page='1',
    search_type=0,
    view_recommend=False
):
    def transform_string(string):
        result = ''
        string = string.encode('utf8')
        for i in range(len(string)):
            result = result + '%' + str(hex(string[i])).lstrip('0x').upper()
        return result
    try:
        search_type = int(search_type)
    except ValueError:
        search_type = 0
    except TypeError:
        search_type = 0

    try:
        page = str(page)
    except TypeError:
        page = 1

    list_search_type = ['search_all', 'search_subject', 'search_memo',
                        'search_name', 'search_subject_memo']
    dclist = 'http://gall.dcinside.com/board/lists/?id='
    mdclist = 'http://gall.dcinside.com/mgallery/board/lists/?id='
    data = gallery + '&page=' + page
    data = data + '&s_keyword=' + transform_string(keyword)
    data = data + '&s_type=' + list_search_type[search_type]
    listurl = dclist + data
    ret = None
    if(view_recommend is True):
        listurl += '&exception_mode=recommend'
    try:
        ret = read(listurl)
    except AttributeError:
        try:  # check if it is minor gallery
            listurl = mdclist + data
            if(view_recommend is True):
                listurl += '&exception_mode=recommend'
            ret = read(listurl)
        except AttributeError as e:
            print_error_msg(e)
            return None
    return ret


def get(gallery, page="1", view_recommend=False):
    dclist = 'http://gall.dcinside.com/'
    data = gallery + '&page=' + str(page)
    listurl = dclist + 'board/lists/?id=' + data
    if(view_recommend is True):
        listurl += '&exception_mode=recommend'
    try:
        ret = read(listurl)
    except AttributeError:
        try:  # check if it is minor gallery
            listurl = dclist + 'mgallery/board/lists/?id=' + data
            if(view_recommend is True):
                listurl += '&exception_mode=recommend'
            ret = read(listurl)
        except AttributeError as e:
            print_error_msg(e)
            return None
    return ret


def string_list(result_list):
    list = []
    try:
        i = 0
        for msg in result_list:
            result = "{}]{}:{}[{}]({}) by {} on {}(추천|{})".format(
               i,
               msg['no'],
               msg['title'],
               msg['comment'],
               msg['view'],
               msg['nick'],
               msg['date'],
               msg['vote_up']
            )
            list.append(result)
            i = i + 1
    except TypeError:
        pass
    return list


def show(result_list):
    result_list = string_list(result_list)
    if(len(result_list) == 0):
        print('No result available!')
    for result in result_list:
        print(result)
    return result_list


def write(filename, result_list):
    result_list = string_list(result_list)
    with open('filename', 'at') as f:
        for result in result_list:
            f.write(result)
    return result_list
