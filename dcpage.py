from html_tool import reqsoup
from urllib.error import HTTPError
from error import print_error_msg
from bs4 import NavigableString, Comment
from hdr import header_iPhone
from image import request_image_simple


class dcpage:
    def __init__(
        self, gallery, no, page='1',
        simple_image_name=True,
    ):
        # gall info
        self.gallery = gallery
        self.no = no
        self.page = page  # order in dclist
        # image settings
        self.__referer = 'http://m.dcinside.com/view.php?'
        self.__referer += 'id=' + str(self.gallery)
        self.__referer += '&no=' + str(self.no)
        self.__referer += '&page=' + str(self.page)

        self.simple_img_name = simple_image_name
        self.image = []  # image files as absolute path name
        # expired data
        self.__expired = True
        self.__soup_data = None
        # transmittable data
        self.title_head = None  # 말머리 기능
        self.title = None
        self.nick = None
        self.date = None
        self.view = None
        self.vote_up = None
        self.num_comment = None
        # digested data
        self.__have_captcha = None
        self.body = None
        self.vote_up_member = 0
        self.vote_down = 0
        self.comment = []

    def __repr__(self):
        result = 'dcpage:' + str(self.gallery)
        result += ')' + str(self.no) + '-' + str(self.page)
        return result

    def __str__(self):
        self.__read_page()
        str = ''
        if(self.title is not None):
            str += "{}{} by {}\n{}\n▲{}({})  ▼{}\n".format(
                self.title_head if self.title_head else '',
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

    def set(self, gallery=None, no=None, page=None, simple_img_name=None):
        '''
        set([gallery],[no],[page])
        return None
        '''
        if(gallery is not None):
            self.gallery = gallery
            self.__expired = True
        if(no is not None):
            self.no = no
            self.__expired = True
        if(page is not None):
            self.page = page
            self.__expired = True
        if(simple_img_name is not None):
            self.simple_img_name = simple_img_name

    def getsoup(self):
        '''
        getsoup(None)
        set self.__soup_data=(new soup data), self.__expired=False
        return  self.__soup_data
        '''
        if(self.__expired is True):
            self.__soup_data = reqsoup(self.__referer, header_iPhone)
        if(self.__soup_data is not None):
            self.__expired = False
            return self.__soup_data
        return None

    def __read_page(self):
        '''
        __read_page(None)
        read most of attribute of dcpage
        call read_body, get_comment
        return None
        '''
        if(self.__expired is False):
            return
        soup = self.getsoup()
        if(soup is None):
            return None
        link = soup.find_all("section", {"class": "grid"})[2]
        if(link is None):
            return None
        else:
            body = link.find("div", {"class": "gall-thum-btm"})
            vote_box = body.find("div", {"class": "reco-circle"})
            head = link.find("div", {"class": "gallview-tit-box"})

            title = head.find("span", {"class": "tit"}).get_text().strip()
            if(title[0] == '['):
                title_head_end = title.find(']') + 1
                self.title_head = title[0:title_head_end]
                title = title[title_head_end:]
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

            self.get_comment()

            self.__have_captcha = link.find(
                "div", {"class": "captcha-code-box"}
            )
#           if(self.have_captcha is not None):
#               pass
            main_text = body.find("div", {"class": "thum-txt"})
            self.body = self.read_body(main_text)
            self.__expired = False

    def read_body(self, body):
        '''
        parse main body to string
        return string
        '''
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
                        self.simple_img_name
                    )
                    self.image.append(image)
                except HTTPError as e:
                    image = None
                    res += '(:읽는데 에러가 발생했습니다.)'
        return res

    def download_image(self):
        '''
        download_image(None)
        download all image in self.image using image class module.
        return None
        '''
        if(self.__expired is True):
            self.get_image_src()
        for src in self.image:
            request_image_simple(self.__referer, img, self.simple_img_name)

    def get_image(self):
        if(self.__expired is True):
            self.get_image_src()
        return self.image

    def get_image_src(self):
        '''
        get_image_src(None)
        set self.image with images in page.
        return self.image
        '''
        self.image = []
        soup = self.getsoup()
        link = soup.find_all("section", {"class": "grid"})[2]
        if(link is None):
            return []
        body = link.find("div", {"class": "gall-thum-btm"})
        img = body.find_all("image")
        self.image = [i.get('src') for i in img]

    def get_comment(self):
        soup = self.getsoup()
        comment = soup.find_all("li", {'class': ['comment', 'comment-add']})
        self.comment = []
        for c in comment:
            one_comment = {'name': '', 'body': ''}
            if('comment-add' in c.get('class')):
                one_comment['body'] += ' └▶'
            try:
                one_comment['name'] = c.a.contents[0]
            except AttributeError as e:
                deleted = c.find('div', {'class': 'delted'})
                if(deleted is not None):
                    one_comment['name'] = ''
                    one_comment['body'] = deleted.get_text().strip()
                    self.comment.append(one_comment)
                    continue
                else:
                    raise e
            if(not isinstance(one_comment['name'], NavigableString)):
                one_comment['name'] = one_comment['name'].get_text().strip()
            body = c.find("p", {"class": "txt"})
            if(body is None):
                one_comment['body'] = ''
                self.comment.append(one_comment)
                continue
            img = body.find("img")
            if(img is not None):
                one_comment['body'] += "(디시콘)"
                one_comment['body'] += img.get('title')
            else:
                one_comment['body'] += body.get_text().strip()
            self.comment.append(one_comment)
        return self.comment

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
        print(self)

    def do_captcha(self):
        pass

    def vote_up(self):
        pass

    def vote_down(self):
        pass
