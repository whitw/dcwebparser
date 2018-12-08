import urllib.request
import requests
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from error import print_error_msg
from hdr import header_chrome


def redirection(pageurl, header=header_chrome):
    result = pageurl
    soup = reqsoup(pageurl, header)
    if(soup is None):
        return pageurl
    scripts = soup.find_all('script')
    for sc in scripts:
        sc = sc.get_text()
        if(sc.find('location.replace') != -1):
            first = sc.find('location.replace(')
            sc = sc[first + 18:]  # '
            end = sc.find(')')
            sc = sc[:end - 1]  # '
            result = sc
            result = redirection(result, header)
            break
        else:
            continue
    return result


def reqsoup(page, header):
    try:
        session = requests.Session()
        data = session.get(page, headers=header)
    except HTTPError as e:
        return None
    soup = BeautifulSoup(data.text, "lxml")
    return soup
