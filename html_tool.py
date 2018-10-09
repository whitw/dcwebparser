import urllib.request
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from error import print_error_msg
from hdr import header_chrome


def redirection(pageurl, header=header_chrome):
    result = pageurl
    soup = reqsoup(pageurl, header)
    scripts = soup.find_all('script')
    for sc in scripts:
        sc = sc.get_text()
        if(sc.find('location.replace') != -1):
            first = sc.find('location.replace(')
            sc = sc[first + 18:]  # '
            end = sc.find(')')
            sc = sc[:end - 1]  # '
            result = redirection(sc, header)
            break
        else:
            continue
    return result


def reqsoup(page, header):
    try:
        req = urllib.request.Request(page, headers=header)
        data = urllib.request.urlopen(req).read()
    except HTTPError as e:
        print_error_msg(e)
        return None
    soup = BeautifulSoup(data, "html.parser")
    return soup
