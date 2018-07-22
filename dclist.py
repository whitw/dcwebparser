import os
import sys
import urllib.request
from bs4 import BeautifulSoup
from hdr import header


def read(
    list_page='http://m.dcinside.com/'
    + 'list.php?id=programming&=page=1'
):
    try:
        req = urllib.request.Request(list_page, headers=header)
        data = urllib.request.urlopen(req).read()
        with open("result_list.txt", "wt") as file:
            file.write(data.decode('utf8'))
    except HTTPError:
        print("HTTPError:Unable to read page")
        return None
    soup = BeautifulSoup(data, "html.parser")

    try:
        link = soup.find("div", {"id": "search_layer"})
        link = link.find_all("a")
    except AttributeError:
        print("Can't access that gallery! Is it valid gallery?")
        return None
    result = []

    for li in link:
        msg = {"no": None, "title": None, "comment": None,
               "nick": None, "date": None, "view": None,
               "vote_up": None, "id": None}
        try:
            string = li.get('href')  # get link to page
            if(string is not None):
                no = string[string.find('no=')+3:string.find('&p')]
                if(no.isnumeric() is False):
                    break
            msg['no'] = no
            msg['title'] = li.find("span", {"class": "txt"}).get_text().strip()
            msg['comment'] = li.find("em", {"class": "txt_num"})
            msg['comment'] = msg['comment'].get_text()[1:-1]
            if(msg['comment'] == ''):
                msg['comment'] = '0'
            msg['nick'] = li.find("span", {"class": "name"}).get_text()
            class_info_span = li.find("span", {"class": "info"})
            class_info_span = class_info_span.find_all("span")
            msg['date'] = class_info_span[2].get_text()
            msg['view'] = class_info_span[4].find('span').get_text()
            msg['vote_up'] = class_info_span[7].find('span').get_text()
            msg['id'] = li.find("span", {"class": "block_info"}).get_text()
        except Exception:
            print('unable to read page!')
        else:
            result.append(msg)
    return result


def search(
    gallery='programming',
    search_type=0,
    page='1',
    keyword='',
    view_recommend=False
):
    try:
        search_type = int(search_type)
    except TypeError:
        search_type = 0
    list_search_type = ['search_all', 'search_subject', 'search_memo',
                        'search_name', 'search_subject_memo']
    dclist = 'http://m.dcinside.com/list.php?id='
    listurl = dclist + gallery + '&page=' + page
    + '&s_type=' + list_search_type[int(search_type)] + '&s_keyword=' + keyword
    if(view_recommend is True):
        listurl += '&exception_mode=recommend'
    return read(listurl)


def get(gallery='programming', page="1"):
    dclist = 'http://m.dcinside.com/list.php?id='
    listurl = dclist + gallery + '&page=' + str(page)
    return read(listurl)


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
