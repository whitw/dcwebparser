from html_tool import reqsoup, redirection
import urllib.request
from urllib.error import HTTPError
from error import print_error_msg, NoGalleryError
from bs4 import BeautifulSoup
from hdr import header_chrome
from dcpage import dcpage
from collections import namedtuple

dpformat = namedtuple('dpformat',
                      'no title nick date view vote_up comment have_img')


class dclist:
    def __init__(self, gallery, index, view_recommend=False,
                 search_by=None, search_keyword=None, simple_image_name=True):
        self.__gallery = gallery
        self.__index = index
        self.simple_image_name = simple_image_name
        self.__view_recommend = view_recommend
        self.__search_by = search_by
        self.__search_keyword = search_keyword
        self.__expired = True
        self.resultpage = []

    def __getitem__(self, k):
        if self.__expired:
            self.get()
        if isinstance(k, slice):
            return [self.to_dcpage(a.no) for a in self.resultpage[k]]
        try:
            ret = self.to_dcpage(self.resultpage[k].no)
        except IndexError:
            return
        return ret

    def __len__(self):
        if not self.__expired:
            return len(self.resultpage)
        else:
            return 0

    def __repr__(self):
        if self.__expired:
            self.get()
        ret = 'dclist>>\n'
        i = self.resultpage[0]
        ret = ret + i.no + ': ' + i.title + '\n~\n'
        i = self.resultpage[-1]
        ret = ret + i.no + ': ' + i.title
        return ret

    def __str__(self):
        if self.__expired:
            self.get()
        if len(self.resultpage) == 0:
            return 'no result available!'
        else:
            s = ''
            try:
                i = 0
                for msg in self.resultpage:
                    result = ('{}]{}:{}[{}]({}) by {} on {}(추천|{})\n').format(
                        i, msg.no, msg.title, msg.comment, msg.view,
                        msg.nick, msg.date, msg.vote_up)
                    s += result
                    i = i + 1

            except TypeError:
                pass

            return s[:-2]

    def nextlist(self):
        try:
            self.__index = str(int(self.__index) + 1)
        except Exception:
            return

        self.get()

    def get(self):
        dclist = 'http://gall.dcinside.com/'
        data = self.__gallery + '&page=' + str(self.__index)
        listurl = dclist + 'board/lists/?id=' + data
        if self.__view_recommend is True:
            listurl += '&exception_mode=recommend'
        try:
            self.__read_url(listurl)
        except AttributeError as e:
            print_error_msg(e)
            return
        except NoGalleryError as e:
            raise e

        self.__expired = False
        return len(self.resultpage) > 0

    def __read_url(self, url, header=header_chrome):
        url = redirection(url)
        soup = reqsoup(url, header)
        if soup is None:
            raise NoGalleryError("Can't access that gallery!")
        self.resultpage = []
        try:
            trs = soup.find('table', {'class': 'gall_list'})
            trs = trs.tbody.find_all('tr')
        except AttributeError:
            raise NoGalleryError("Can't access that gallery!")

        for tr in trs:
            msg = {'title': None,
                   'nick': None,
                   'date': None,
                   'view': None,
                   'vote_up': None,
                   'comment': None,
                   'have_img': False
                   }
            try:
                ub_word = tr.find('td', {'class': 'gall_tit'})
                notice = ub_word.em['class'][1]
                msg['title'] = ub_word.a.get_text()
                comment = ub_word.find('a', {'class': 'reply_numbox'})
                if comment is not None:
                    msg['comment'] = comment.get_text()[1:-1]
                else:
                    msg['comment'] = '0'
                if notice == 'icon_notice':
                    continue
                else:
                    if notice == 'icon_img':
                        msg['have_img'] = True
                    else:
                        msg['have_img'] = False
            except Exception as e:
                print_error_msg(e)

            try:
                no = tr.find('td', {'class': 'gall_num'}).get_text()
                nick = tr.find('td', {'class': 'gall_writer'})
                msg['nick'] = nick['data-nick']
                msg['date'] = tr.find('td', {'class': 'gall_date'}).get_text()
                msg['view'] = tr.find('td', {'class': 'gall_count'}).get_text()
                vote_up = tr.find('td', {'class': 'gall_recommend'})
                msg['vote_up'] = vote_up.get_text()
            except AttributeError as e:
                continue
            except KeyError as e:
                continue

            self.resultpage.append(dpformat(
                no, msg['title'], msg['nick'], msg['date'],
                msg['view'], msg['vote_up'], msg['comment'], msg['have_img']))

    def show(self):
        print(self)

    def search(self):
        self.resultpage = []

        def transform_string(string):
            result = ''
            string = string.encode('utf8')
            for i in range(len(string)):
                result += '%' + str(hex(string[i])).lstrip('0x').upper()

            return result

        try:
            search_by = list_search_type[self.__search_by]
        except Exception as e:
            print_error_msg(e)

        search_keyword = self.__search_keyword
        data = gallery + '&page=' + page
        data = data + '&s_keyword=' + search_keyword
        data = data + '&s_type=' + search_by
        listurl = dclist + data
        self.__read_url(listurl)

    def to_dcpage(self, no):
        try:
            return dcpage(self.__gallery, no,
                          self.__index, self.simple_image_name)
        except Exception:
            return
