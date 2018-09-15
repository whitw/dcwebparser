import os
import sys
import urllib.request
from urllib.error import HTTPError
from error import print_error_msg
from bs4 import BeautifulSoup
from bs4 import NavigableString
from hdr import header_iPhone
from image import request_image_simple, sfwimage


class dcpage:
    def __init__(self, gallery, no, page='1', safe=True):
        self.gallery = gallery
        self.no = no
        self.page = page
        self.safe = safe
        self.result = {
            "title": None,
            "nick": None,
            "date": None,
            "view": None, "comment": [], "body": None}
        self.read_page()

    def set_gallery(self, gallery):
        self.gallery = gallery

    def get(self, gallery, no, page='1', safe=True):
        self.gallery = gallery
        self.no = no
        self.page = page
        self.safe = safe
        self.read_page()

    def gethtml(self):
        dcpage = 'http://m.dcinside.com/view.php?id='
        pageurl = dcpage + self.gallery
        pageurl = pageurl + '&no=' + str(self.no) + '&page=' + str(self.page)
        req = None
        data = None
        try:
            req = urllib.request.Request(pageurl, headers=header_iPhone)
            data = urllib.request.urlopen(req).read()
        except HTTPError:
            return None
        return data

    def debug(self):
        data = self.gethtml()
        with open('result.txt', 'wt') as f:
            f.write(data.decode('utf8'))

    def read_page(self):
        data = self.gethtml()
        if(data is None):
            return None
        soup = BeautifulSoup(data, "html.parser")
        link = soup.find("div", {"class": "gall_content"})
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
            self.result['comment'] = parse_comments(comment)
            self.result['title'] = title.strip()
            self.result['nick'] = head.get_text().strip()
            self.result['body'] = read_body(body, self.safe)

    def result_str(self):
        str = ''
        if(self.result['title'] is not None):
            str += "{} by {}\n{}\n".format(
                self.result['title'],
                self.result['nick'],
                self.result['body']
            )
            if(len(self.result['comment']) > 0):
                str += '------------------------------\n'
                for i in self.result['comment']:
                    str += '{}: {}\n'.format(i['name'], i['body'])
                str += '------------------------------\n'
        else:
            str = 'Unable to read page! May be deleted'
        return str

    def show(self):
        print(self.result_str())

    def print(self):
        print(self.gallery)
        print(self.no)
        print(self.page)
        print(self.safe)
        print(self.result)


def read_body(body, safe):
    res = ''
    for c in body.descendants:
        if(c == '\n'):
            continue
        if(isinstance(c, NavigableString) and c.parent.name != 'script'):
            res += c
        if(c.name == 'br' or c.name == 'p'):
            res += '\n'
        elif(c.name == 'img'):
            res += '(이미지)'
            try:
                image = request_image_simple(c.get('src'))
                if(safe is True):
                    sfwimage(image)
            except HTTPError as e:
                res += '(:읽는데 에러가 발생했습니다.)'
    return res


def parse_comments(comment):
    result = []
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
        result.append(one_comment)
    return result
