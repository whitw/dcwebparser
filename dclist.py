import os
import sys
import urllib.request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from hdr import header_chrome


def read(
    list_page='http://gall.dcinside.com/'
    + 'list.php?id=programming&=page=1'
):
    try:
        req = urllib.request.Request(list_page, headers=header_chrome)
        data = urllib.request.urlopen(req).read()
    except HTTPError:
        print("HTTPError:Unable to read page")
        return None
    soup = BeautifulSoup(data, "html.parser")

    try:
        link = soup.find("table").tbody.find_all("tr")
    except AttributeError:
        raise AttributeError("Can't access that gallery!")
    result = []

    for li in link:
        msg = {"no": None, "title": None, "comment": None,
               "nick": None, "date": None, "view": None,
               "vote_up": None, "id": None}
        try:
            no = li.find("td", {"class": "t_notice"}).get_text()
            if(no is not None and no.isnumeric() is True):
                msg['no'] = no
            else:
                continue
            a = li.find_all('a')
            msg['title'] = a[0].get_text().strip()
            if(len(a) > 1):
                msg['comment'] = a[1].em.get_text()[1:-1]
            else:
                msg['comment'] = '0'
            msg['nick'] = li.find("td", {"class": "t_writer user_layer"})
            msg['nick'] = msg['nick'].get('user_name')
            msg['date'] = li.find("td", {"class": "t_date"}).get('title')
            hits = li.find_all('td', {'class': 't_hits'})
            msg['view'] = hits[0].get_text()
            msg['vote_up'] = hits[1].get_text()
            msg['id'] = li.find("span", {"class": "user_nick_nm"}).get('title')
        except AttributeError as e:
            continue
        else:
            result.append(msg)
    return result


def search(
    gallery='programming',
    page='1',
    search_type=0,
    keyword='',
    view_recommend=False
):
    try:
        search_type = int(search_type)
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
    listurl = dclist + gallery + '&page=' + page
    listurl = listurl + '&s_keyword=' + keyword
    listurl = listurl + '&s_type=' + list_search_type[search_type]
    if(view_recommend is True):
        listurl += '&exception_mode=recommend'
        ret = None
    try:
        ret = read(listurl)
    except AttributeError:
        ret = None
    return ret


def get(gallery='programming', page="1", view_recommend=False):
    dclist = 'http://gall.dcinside.com/board/lists/?id='
    listurl = dclist + gallery + '&page=' + str(page)
    if(view_recommend is True):
        listurl += '&exception_mode=recommend'
    try:
        ret = read(listurl)
    except AttributeError:
        ret = None
    return ret


def show(result_list):
    try:
        for msg in result_list:
            print("({}){}[{}]({}) by {} on {}(추천|{})".format(
               msg['no'],
               msg['title'],
               msg['comment'],
               msg['view'],
               msg['nick'],
               msg['date'],
               msg['vote_up'])
               )
    except TypeError:
        pass
    return result_list
