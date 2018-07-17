import os
import sys
import urllib.request
import dcparser
from bs4 import BeautifulSoup

hdr = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X)'
    + 'AppleWebKit/601.1.46 (KHTML, like Gecko)'
    + '/Version/9.0 Mobile/13F69 Safari/601.1',
    'Accept': 'text/html,application/xhtml+xml,'
    + 'application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

if(__name__ == "__main__"):
    if(len(sys.argv) > 2):
        gallery = sys.argv[1]
        no = sys.argv[2]
        print("gallery = {0},no = {1}".format(gallery, no))
    else:
        gallery = 'jumper'
        no = '1'


def getlist(gallery="jumper", page="1"):
    dclist = 'http://m.dcinside.com/list.php?id='
    listurl = dclist + gallery + '&page=' + page
    req = urllib.request.Request(listurl, headers=hdr)
    data = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(data, "html.parser")
    link = soup.find("div", {"id": "search_layer"})
    link = link.find_all("a")
    result = []
    with open('resul2.txt', 'wt') as file:
        file.write(data.decode('utf8'))
    for li in link:
        msg = {"no": None, "title": None, "comment": None,
               "nick": None, "date": None, "view": None,
               "vote_up": None, "id": None}
        string = li.get('href')  # get link to page
        if(string is not None):
            no = string[string.find('no=')+3:string.find('&p')]
            if(no.isnumeric() is False):
                break
        msg['no'] = no
        msg['title'] = li.find("span", {"class": "txt"}).get_text().strip()
        msg['comment'] = li.find("em", {"class": "txt_num"}).get_text()[1:-1]
        if(msg['comment'] == ''):
            msg['comment'] = '0'
        msg['nick'] = li.find("span", {"class": "name"}).get_text()

        print("(%s)%s[%s] by %s" % (msg['no'],
                                    msg['title'], msg['comment'], msg['nick']))

        result.append(msg)
    return result


def getpage(gallery="jumper", no="1290489", page="1"):
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

        print("%s by %s\n%s" % (title, result['nick'], result['body']))

        return result


result = None
# result = getpage(gallery, no, '1')
if(result is None or result['title'] is None):
    pass
else:
    # print('title= {0}'.format(result['title']))
    # print('head.get_text = {0}'.format(result['nick'].get_text()))
    # ('body = \n{0}'.format(result['body'].get_text().strip()))
    pass
result = getlist(gallery, '1')
for data in result:
    getpage(gallery, data['no'], '1')
    print('\n\n')
