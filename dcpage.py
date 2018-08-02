import os
import sys
import urllib.request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from hdr import header_iPhone
from image import request_image_simple


def get(gallery="programming", no="812899", page="5"):
    dcpage = 'http://m.dcinside.com/view.php?id='
    pageurl = dcpage + gallery + '&no=' + str(no) + '&page=' + str(page)
    try:
        req = urllib.request.Request(pageurl, headers=header_iPhone)
        data = urllib.request.urlopen(req).read()
    except HTTPError:
        return None
    soup = BeautifulSoup(data, "html.parser")
    check_mgallery = None
    if(check_mgallery is not None):
        pass
    link = soup.find("div", {"class": "gall_content"})
    result = {"title": None, "nick": None,
              "date": None, "view": None, "comment": [], "body": None}
    if(link is None):
        return None
    else:
        title = link.find("span", {"class": "tit_view"}).get_text()
        head = link.find("span", {"class": "info_edit"})
        body = link.find("div", {"class": "view_main"})
        try:
            comment = soup.find("div", {"class": "wrap_list"})
            comment = comment.find_all("span", {"class": "inner_best"})
        except AttributeError:
            comment = []

        for c in comment:
            one_comment = {'name': None, 'body': None}
            one_comment['name'] = c.span.get_text()[1:-1]
            one_comment['body'] = c.find("span", {"class": "txt"})
            img = one_comment['body'].find("img")
            if(img is not None):
                one_comment['body'] = "(디시콘)"
                one_comment['body'] += img.get('title')
            else:
                one_comment['body'] = one_comment['body'].get_text().strip()
            result['comment'].append(one_comment)

        result['title'] = title.strip()
        result['nick'] = head.get_text().strip()
        result['body'] = read_body(body)

        return result


def read_body(body):
    res = ''
    for child in body.descendants:
        if(child.name == 'img'):
            res += '(이미지)'
            request_image_simple(child.attrs['src'])
        elif(child.name == 'br'):
            res += '\n'
        elif(child.name == 'p'):
            try:
                res += child.get_text().strip()
            except Exception as e:
                print_err_msg(e)
        elif(child.name == 'div' and
             child.has_attr('class') is True and
             child.attrs['class'] == 'yt_movie'):
            res += '(유튜브)'
            # currently it can't read youtube:need to be fixed
        else:
            pass
    print('*')
    return res


def show(result):
    if(result is not None and result['title'] is not None):
        print("%s by %s\n%s" % (result['title'],
                                result['nick'],
                                result['body']))
        if(len(result['comment']) > 0):
            print('------------------------------')
            for i in result['comment']:
                print('%s: %s' % (i['name'], i['body']))
            print('------------------------------')

    else:
        print('Unable to read page! May be deleted')
