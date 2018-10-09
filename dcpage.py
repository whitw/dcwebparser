import os
import sys
import urllib.request
import requests
from urllib.error import HTTPError
from error import print_error_msg
from bs4 import BeautifulSoup
from bs4 import NavigableString, Comment
from hdr import header_iPhone
from image import request_image_simple, sfwimage


class dcpage:
    def __init__(self, gallery, no, page='1', safe=True, simple_name=True):
        self.gallery = gallery
        self.no = no
        self.page = page
        self.safe = safe
        self.referer = None
        self.simple_name = simple_name
        self.have_captcha = None
        self.data = None
        self.result = {
            "title": None,
            "nick": None,
            "date": None,
            "view": None,
            "vote_up": 0,
            "vote_up_member": 0,
            "vote_down": 0,
            "comment": [],
            "body": None}
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
        def changeTypo(data):
            return data.replace('sapn', 'span')
        dcpage = 'http://m.dcinside.com/view.php?id='
        pageurl = dcpage + self.gallery
        pageurl = pageurl + '&no=' + str(self.no) + '&page=' + str(self.page)
        req = None
        data = None
        if(self.data is None):
            try:
                # req = urllib.request.Request(pageurl, headers=header_iPhone)
                # data = urllib.request.urlopen(req).read()
                data = requests.get(pageurl, headers=header_iPhone)
                data = data.text
                data = changeTypo(data)
                self.data = data
            except HTTPError:
                return None
        else:
            data = self.data
        self.referer = pageurl
        return data

    def debug(self):
        data = self.gethtml()
        with open('raw.txt', 'wt') as f:
            f.write(data)
        soup = BeautifulSoup(data, "html.parser")
        with open('result.txt', 'wt') as f:
            f.write(soup.prettify())

    def read_page(self):
        data = self.gethtml()
        if(data is None):
            return None
        soup = BeautifulSoup(data, "html.parser")
        link = soup.find_all("section", {"class": "grid"})[2]
        if(link is None):
            return None
        else:
            head = link.find("div", {"class": "gallview-tit-box"})
            title = head.find("span", {"class": "tit"}).get_text().strip()
            if(title.find('[일반]') != -1):
                title = title[len('[일반]'):]
            self.result['title'] = title.strip()

            head2 = head.find('div', {"class": "btm"})
            head2 = head2.find('ul', {"class": "ginfo2"})
            nick = head2.find_all("li")[0]
            self.result['nick'] = nick.get_text().strip()
            time = head2.find_all("li")[1]
            self.result['time'] = time.get_text().strip()

            body = link.find("div", {"class": "gall-thum-btm"})
            b_head = body.find("ul", {"class": "ginfo2"})
            view = b_head.find_all("li")[0].get_text()
            view = view.split(' ')[1]
            self.result['view'] = view

            vote_box = body.find("div", {"class": "reco-circle"})
            vote_up = vote_box.find("span", {"id": "recomm_btn"})
            self.result['vote_up'] = vote_up.get_text()

            vote_up_member = vote_box.find("span", {"id": "recomm_btn_member"})
            self.result['vote_up_member'] = vote_up_member.get_text()

            vote_down = vote_box.find("span", {"id": "nonrecomm_btn"})
            self.result['vote_down'] = vote_down.get_text()

            try:
                # comment = soup.find("div", {"class": "all-comment"})
                # comment = comment.find_all("li")
                comment = soup.find_all("li", {"class": "comment"})
            except AttributeError:
                comment = []

            self.have_captcha = link.find("div", {"class": "captcha-code-box"})
#           if(self.have_captcha is not None):
#               pass
            self.result['comment'] = parse_comments(comment)
            main_text = body.find("div", {"class": "thum-txt"})
            self.result['body'] = self.read_body(
                main_text,
                self.safe,
                self.simple_name
            )

    def read_body(self, body, safe, simple_name=True):
        res = ''
        for c in body.descendants:
            if(c == '\n'):
                continue
            if(isinstance(c, NavigableString) and c.parent.name != 'script'):
                if(isinstance(c, Comment)):
                    pass
                else:
                    res += c
            if(c.name == 'br' or c.name == 'p'):
                res += '\n'
            elif(c.name == 'img'):
                res += '(이미지)'
                try:
                    image = request_image_simple(
                        self.referer,
                        c.get('src'),
                        simple_name=simple_name
                    )
                    if(safe is True):
                        sfwimage(image)
                except HTTPError as e:
                    image = None
                    res += '(:읽는데 에러가 발생했습니다.)'
        return res

    def result_str(self):
        str = ''
        if(self.result['title'] is not None):
            str += "{} by {}\n{}\n▲{}({})  ▼{}\n".format(
                self.result['title'],
                self.result['nick'],
                self.result['body'],
                self.result['vote_up'],
                self.result['vote_up_member'],
                self.result['vote_down']
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

    def do_captcha(self):
        pass

    def vote_up(self):
        pass

    def vote_down(self):
        pass


def parse_comments(comment):
    result = []
    for c in comment:
        one_comment = {'name': '', 'body': ''}
        if(c['class'][0] == 'comment-add'):
            one_comment['body'] += ' └▶'
        one_comment['name'] = c.a.contents[0]
        if(not isinstance(one_comment['name'], NavigableString)):
            one_comment['name'] = one_comment['name'].get_text().strip()
        body = c.find("p", {"class": "txt"})
        if(body is None):
            one_comment['body'] = ''
            result.append(one_comment)
            continue
        img = body.find("img")
        if(img is not None):
            one_comment['body'] += "(디시콘)"
            one_comment['body'] += img.get('title')
        else:
            one_comment['body'] += body.get_text().strip()
        result.append(one_comment)
    return result


def get_src(script, name):
    text = name + "="
    begin = script.find(text) + len(text)
    end = script[begin:].find('"') + begin
    result = script[begin: end]
    return result
