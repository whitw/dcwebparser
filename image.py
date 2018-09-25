import os
from sys import argv
from PIL import Image, ImageFilter
from urllib.request import urlopen, urlretrieve
import requests
from urllib.error import HTTPError
from hdr import header_iPhone, header_image
file = 'img_index.txt'


def get_simple_name_num():
    ret = '0'
    file = 'img_index.txt'
    if(os.path.exists(file) is not True):
        with open(file, 'wt') as f:
            f.write('0')
    pos = 0
    with open(file, 'rt') as f:
        try:
            pos = f.read()
        except Exception:
            pos = 'image'
    ret = pos
    with open(file, 'wt') as f:
        pos = int(pos)
        pos = pos + 1
        pos = str(pos)
        f.write(pos)
    return ret


def get_file_name(rq, simple_name=False):
    ret = None
    ftype = rq.headers['Content-Type']
    if(simple_name is False):
        ret = rq.headers['Content-Disposition'].split('=')[1]
    else:
        ret = get_simple_name_num()
    if(ftype == 'application/octet-stream'):
        pass
    elif(ftype == 'image/gif'):
        ret = ret + '.gif'
    elif(ftype == 'image/jpg'):
        ret = ret + '.jpg'
    if(ret.find('.') == -1):
        ret = ret + '.jpg'
    return ret


def request_image_simple(referer, src, simple_name=False):
    header = header_image
    header['Referer'] = referer
    if(os.path.exists(file) is not True):
        with open(file, 'wt') as f:
            f.write('0')
    pos = 0
    with open(file, 'rt') as f:
        try:
            pos = f.read()
        except Exception:
            pos = 'image'
    if(src is None):
        return None

    rq = requests.get(src, headers=header)
    name = get_file_name(rq, simple_name=simple_name)

    if not os.path.exists('image'):
        os.mkdir('image')

    name = 'image//' + name
    with open(name, 'wb') as f:
        f.write(rq.content)

    return name


def sfwimage(img, to=None):
    if(img is None):
        return None
    if(to is None):
        to = img
    try:
        im = Image.open(img)
    except OSError as e:
        return None
    im = Image.eval(im, lambda x: x-50).convert('L')
    im = im.filter(ImageFilter.FIND_EDGES)
    # im = Image.eval(im, lambda x: 256-x)
    while(im.size[0] > 300 or im.size[1] > 300):
        smallsize = (int(im.size[0] * 0.5), int(im.size[1] * 0.5))
        im = im.resize(smallsize, Image.ANTIALIAS)
    im.save(to)
    return to


if(__name__ == '__main__'):
    ffrom = 'default.jpg'
    if(len(argv) > 1):
        ffrom = argv[1]
    print('converted "%s" into "safe.jpg"' % ffrom)
    ffrom = 'image//' + ffrom
    sfwimage(ffrom, 'image//safe.jpg')
