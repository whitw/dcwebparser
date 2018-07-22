import os
import sys
import urllib.request
from bs4 import BeautifulSoup
from hdr import header


def get(gallery="programming", no="812899", page="5"):
    dcpage = 'http://m.dcinside.com/view.php?id='
    pageurl = dcpage + gallery + '&no=' + str(no) + '&page=' + str(page)
    req = urllib.request.Request(pageurl, headers=header)
    data = urllib.request.urlopen(req).read()
    with open("result_page.txt", "wt") as file:
        file.write(pageurl + '\n')
        file.write(data.decode('utf8'))
    soup = BeautifulSoup(data, "html.parser")
    link = soup.find("div", {"class": "gall_content"})
    result = {"title": None, "nick": None,
              "date": None, "view": None, "comment": None, "body": None}
    if(link is None):
        return None
    else:
        title = link.find("span", {"class": "tit_view"}).get_text()
        head = link.find("span", {"class": "info_edit"})
        body = link.find("div", {"class": "view_main"})
        result['title'] = title.strip()
        result['nick'] = head.get_text().strip()
        result['body'] = body.get_text().strip()

        return result


def show(result):
    if(result is not None and result['title'] is not None):
        print("%s by %s\n%s" % (result['title'],
                                result['nick'],
                                result['body']))
    else:
        print('Unable to read page! May be deleted')
