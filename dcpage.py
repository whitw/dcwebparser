import os
import sys
import urllib.request
import requests
from urllib.error import HTTPError
from error import print_error_msg, NoGalleryError
from bs4 import BeautifulSoup
from bs4 import NavigableString, Comment
from hdr import header_iPhone
from image import request_image_simple, sfwimage, smallimage


class dcpage:
    def __init__(
        self, gallery, no, page='1',
        data_from_dclist={
            'title': None,
            'nick': None,
            'date': None,
            'view': 0,
            "vote_up": 0
        }
    ):
        # gall info
        self.__gallery = gallery
        self.__no = no
        self.__page = page  # order in dclist
        # image settings
        self.__referer = None
        self.image = []  # image files as absolute path name
        # soup data
        self.__have_captcha = None
        self.__html_data = None
        self.__soup_data = None
        self.__comment_tag = None
        # transmittable data
        self.title = data_from_dclist['title']
        self.nick = data_from_dclist['nick']
        self.date = data_from_dclist['date']
        self.view = data_from_dclist['view']
        self.vote_up = data_from_dclist['vote_up']
        self.num_comment = data_from_dclist['comment']
        # digested data
        self.body = None
        self.vote_up_member = 0
        self.vote_down = 0
        self.comment = []

    def get(self, gallery, no, page='1',
            safe=True, simple_name=True, small_img=True
            ):
        self.__gallery = gallery
        self.__no = no
        self.__page = page
        self.safe = safe
        self.simple_name = simple_name
        self.small_img = small_img
        self.read_page()

    def get_gallery(self):
        return self.__gallery
    
    def get_no(self):
        return self.__no
    
    def get_page(self):
        return self.__page
        
    def getsoup(self):
        def changeTypo(data):
            return data.replace('</sapn>', '</span>')
        dcpage = 'http://m.dcinside.com/view.php?id='
        pageurl = dcpage + self.__gallery
        pageurl = pageurl + '&no=' + str(self.__no)
        pageurl = pageurl + '&page=' + str(self.__page)
        data = None
        if(self.__soup_data is None):
            try:
                data = requests.get(pageurl, headers=header_iPhone)
                data = data.text
                data = changeTypo(data)
                self.__html_data = data
                self.__soup_data = BeautifulSoup(data, "html.parser")
                data = self.__soup_data
            except HTTPError:
                return None
        else:
            data = self.__soup_data
        self.__referer = pageurl
        return data

    def read_page(self):
        if(self.body is not None):
            return
        soup = self.getsoup()
        link = soup.find_all("section", {"class": "grid"})[2]
        if(link is None):
            return None
        else:
            body = link.find("div", {"class": "gall-thum-btm"})
            vote_box = body.find("div", {"class": "reco-circle"})
            if(self.title is None):
                head = link.find("div", {"class": "gallview-tit-box"})
                title = head.find("span", {"class": "tit"}).get_text().strip()
                self.title = title.strip()

                head2 = head.find('div', {"class": "btm"})
                head2 = head2.find('ul', {"class": "ginfo2"})
                nick = head2.find_all("li")[0]
                self.nick = nick.get_text().strip()
                date = head2.find_all("li")[1]
                self.date = date.get_text().strip()

                b_head = body.find("ul", {"class": "ginfo2"})
                view = b_head.find_all("li")[0].get_text()
                view = view.split(' ')[1]
                self.view = view

                vote_up = vote_box.find("span", {"id": "recomm_btn"})
                self.vote_up = vote_up.get_text()

            vote_up_member = vote_box.find("span", {"id": "recomm_btn_member"})
            self.vote_up_member = vote_up_member.get_text()

            vote_down = vote_box.find("span", {"id": "nonrecomm_btn"})
            self.vote_down = vote_down.get_text()

            try:
                comment = soup.find_all("li", {"class": "comment"})
            except AttributeError:
                comment = []

            self.__have_captcha = link.find(
                "div", {"class": "captcha-code-box"}
            )
#           if(self.have_captcha is not None):
#               pass
            self.comment = parse_comments(comment)
            main_text = body.find("div", {"class": "thum-txt"})
            self.body = self.read_body(main_text)

    def read_body(self, body):
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
                        self.__referer,
                        c.get('src'),
                        self.simple_name
                    )
                    if(self.safe is True):
                        sfwimage(image)
                    if(self.small_img is True):
                        smallimage(image)
                except HTTPError as e:
                    image = None
                    res += '(:읽는데 에러가 발생했습니다.)'
        return res

    def get_image(self, src=None):
        if(src is None):
            result = get_image_src()
        else:
            if(isinstance(src, list)):
                result = src
            else:
                result = [].append(src)
        for img_src in result:
            image = request_image_simple(
                self.__referer,
                img_src
            )

    def get_image_src(self):
        result = []
        soup = self.getsoup()
        link = soup.find_all("section", {"class": "grid"})[2]
        if(link is None):
            return []
        body = link.find("div", {"class": "gall-thum-btm"})
        img = body.find_all("image")
        for i in img:
            result.append(img.get('src'))

    def result_str(self):
        self.read_page()
        str = ''
        if(self.title is not None):
            str += "{} by {}\n{}\n▲{}({})  ▼{}\n".format(
                self.title,
                self.nick,
                self.body,
                self.vote_up,
                self.vote_up_member,
                self.vote_down
            )
            if(len(self.comment) > 0):
                str += '------------------------------\n'
                for i in self.comment:
                    str += '{}: {}\n'.format(i['name'], i['body'])
                str += '------------------------------\n'
        else:
            str = 'Unable to read page! May be deleted'
        return str

    def parse_comments(self, comment):
        result = []
        for c in comment:
            one_comment = {'name': '', 'body': ''}
            if(c['class'][0] == 'comment-add'):
                one_comment['body'] += ' └▶'
            try:
                one_comment['name'] = c.a.contents[0]
            except AttributeError as e:
                deleted = c.find('div', {'class': 'delted'})
                if(deleted is not None):
                    one_comment['name'] = ''
                    one_comment['body'] = deleted.get_text().strip()
                    result.append(one_comment)
                    continue
                else:
                    raise e
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

    def show(self):
        print(self.result_str())

    def do_captcha(self):
        pass

    def vote_up(self):
        pass

    def vote_down(self):
        pass
