import os
import sys
import urllib.request
from bs4 import BeautifulSoup
from hdr import header


def getpage(gallery="programming", no="812899", page="5"):
    dcpage = 'http://m.dcinside.com/view.php?id='
    pageurl = dcpage + gallery + '&no=' + no + '&page=' + page
    req = urllib.request.Request(pageurl, headers=hdr)
    data = urllib.request.urlopen(req).read()
    # with open("result.txt", "wt") as file:
    #    file.write(data.decode('utf8'))
    soup = BeautifulSoup(data, "html.parser")

    link = soup.find("div", {"class": "gall_content"})
    result = {"title": None, "nick": None,
              "date": None, "view": None, "comment": None, "body": None}
    if(link is None):
        return result
    else:
        title = link.find("span", {"class": "tit_view"}).get_text()
        head = link.find("span", {"class": "info_edit"})
        body = link.find("div", {"class": "view_main"})
        result['title'] = title.strip()
        result['nick'] = head.get_text().strip()
        result['body'] = body.get_text().strip()

        return result


def printpage(result_page):
    print("%s by %s\n%s" % (title, result['nick'], result['body']))
