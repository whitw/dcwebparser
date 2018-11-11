import os
import sys
from html_tool import reqsoup, redirection
import urllib.request
from urllib.error import HTTPError
from error import print_error_msg
from bs4 import BeautifulSoup
from hdr import header_chrome


class dclist:
    SEARCH_BY_ALL = 0
    SEARCH_BY_TITLE = 1
    SEARCH_BY_TEXT = 2
    SEARCH_BY_NICK = 3
    SEARCH_BY_TITLE_TEXT = 4

    def __init__(self,
                 gallery, index,
                 view_recommend=False,
                 search_by=None, search_keyword=None
                 ):
        # base information
        self.__gallery = gallery
        self.__index = index
        self.__view_recommend = view_recommend
        # __index th list of gallery
        self.__search_by = search_by
        self.__search_keyword = search_keyword
        self.__last = None
        # last index that user viewed, use page() to get __resultpage[__last]
        # and use next() to show next page.
        # if it is last page in list, next() calls nextlist()

        # parsed soup
        self.__soup = None

        # parsed data
        self.__resultpage = []   # accept only dcpages

    def page(self, index=None):
        if(index is not None):
            self.__last = index
        if(self.__last is None):
            self.__last = 0
        self.get()
        return __resultpage[self.__last]

    def pages(self):
        self.__last = None
        self.get()
        return __resultpage

    def nextlist(self):
        self.__index++
        self.__last = None
        self.get()

    def get(self):
        dclist = 'http://gall.dcinside.com/'
        data = self.__gallery + '&page=' + str(self.__page)
        listurl = dclist + 'board/lists/?id=' + data
        if(self.__view_recommend is True):
            listurl += '&exception_mode=recommend'
        listurl = redirection(listurl)
        try:
            self.__read_url(listurl)
        except AttributeError as e:
            print_error_msg(e)
            return None
        return len(self.__resultpage) > 0

    def __read_url(self, url):
        soup = reqsoup(url, header_chrome)
        if(soup is None):
            return None
        try:
            trs = soup.find("table", {"class": "gall_list"})
            trs = trs.tbody.find_all("tr")
        except AttributeError:
            raise NoGalleryError("Can't access that gallery!")
        for tr in trs:
            msg = {
                "no": None,        # 필수
                "title": None,     # 중복
                "comment": None,   # dcpage에선 필요도 낮음
                "have_img": False  # dcpage에선 필요도 낮음
                "nick": None,      # 중복
                "date": None,      # 중복
                "view": None,      # 중복
                "vote_up": None,   # 중복
            }
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
            except KeyError as e:  # 운영자
                continue
            else:
                self.__resultpage.append(
                    dcpage(
                        self.__gallery,
                        self.__last,
                        self.__index,
                        data_from_dclist=msg
                    )
                )

    def show(self, to=sys.stdout):
        result_list = self.__resultpage
        try:
            i = 0
            for msg in result_list:
                result = "{}]{}:{}[{}]({}) by {} on {}(추천|{})".format(
                   i,
                   msg.get_no()
                   msg.title,
                   msg.num_comment,
                   msg.view,
                   msg.nick,
                   msg.date,
                   msg.vote_up
                )
                list.append(result)
                i = i + 1
        except TypeError:
            pass

        if(len(result_list) == 0):
            print('No result available!', file=to)
        if(file is None):
            for result in result_list:
                print(result, file=to)
        return result_list


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
        ret = self.__read_url(listurl)
    except AttributeError:
        try:  # check if it is minor gallery
            listurl = mdclist + data
            if(view_recommend is True):
                listurl += '&exception_mode=recommend'
            ret = self.__read_url(listurl)
        except AttributeError as e:
            print_error_msg(e)
            return None
    return ret
