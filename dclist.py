import os
import sys
import urllib.request
from bs4 import BeautifulSoup
from hdr import header


def readlist(list_page='http://m.dcinside.com/'
             + 'list.php?id=programming&=page=1'):
    req = urllib.request.Request(list_page, headers=header)
    data = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(data, "html.parser")
    link = soup.find("div", {"id": "search_layer"})
    link = link.find_all("a")
    result = []
    for li in link:
        msg = {"no": None, "title": None, "comment": None,
               "nick": None, "date": None, "view": None,
               "vote_up": None, "id": None}
        string = li.get('href')  # get link to page
        if(string is not None):
            no = string[string.find('no=')+3:string.find('&p')]
            if(no.isnumeric() is False):
                break
        msg['no'] = no
        msg['title'] = li.find("span", {"class": "txt"}).get_text().strip()
        msg['comment'] = li.find("em", {"class": "txt_num"}).get_text()[1:-1]
        if(msg['comment'] == ''):
            msg['comment'] = '0'
        msg['nick'] = li.find("span", {"class": "name"}).get_text()
        class_info = li.find("span", {"class": "info"})
        msg['date'] = class_info.find_all("span")[2].get_text()
        msg['view'] = class_info.find_all("span")[4].find('span').get_text()
        msg['vote_up'] = class_info.find_all("span")[7].find('span').get_text()
        msg['id'] = li.find("span", {"class": "block_info"}).get_text()
        result.append(msg)
    return result


def searchlist(gallery='programming', search_type=0,
               keyword='', view_recommend=False):
    if(isnumeric(search_type) is False):
        return None
    list_search_type = ['search_all', 'search_subject', 'search_memo',
                        'search_name', 'search_subject_memo']
    dclist = 'http://m.dcinside.com/list.php?id='
    listurl = dclist + gallery + '&page=' + page
    + '&s_type=' + list_search_type[int(search_type)] + '&s_keyword=' + keyword
    if(view_recommend):
        listurl += '&exception_mode=recommend'
    return readlist(listurl)


def getlist(gallery='programming', page="1"):
    dclist = 'http://m.dcinside.com/list.php?id='
    listurl = dclist + gallery + '&page=' + str(page)
    return readlist(listurl)


def printlist(result_list):
    for msg in result_list:
        print("(%s)%s[%s](%s) by %s on %s(추천|%s)" % (
            msg['no'],
            msg['title'],
            msg['comment'],
            msg['view'],
            msg['nick'],
            msg['date'],
            msg['vote_up']))
    return result_list
