import os
import collections.abc
from sys import argv
from PIL import Image, ImageFilter
from urllib.request import urlopen, urlretrieve
import requests
from urllib.error import HTTPError
from hdr import header_iPhone, header_image
file = 'img_index.txt'


class imagemachine:
    def __init__(self, f=None):
        if(f is None):
            self.filter = []
        else:
            if(isinstance(f, collections.abc.Sequence)):
                # f stands for function or list of functions
                self.filter = list(f)
            else:
                self.filter = [f]

    def convert(self, image, to=None):
        im = image
        result = []
        try:
            for f in self.filter:
                result.append(f(im, to))
        except TypeError:
            raise TypeError("filter functions need two arguments: \
            image(dir of image), to=None(dir of converted image)")
        except Exception:
            raise
        return all(result)

    def toggle(self, f, to):
        if(to is True):
            self.add(f)
        else:
            self.delete(f)

    def add(self, f):
        if f not in self.filter:
            self.filter.append(f)

    def delete(self, f):
        if f in self.filter:
            self.filter.remove(f)

    def __call__(self, image, to=None):
        if(isinstance(image, str)):
            return self.convert(image, to)
        if(isinstance(image, collections.abc.Sequence)):
            res = [self.convert(im) for im in image]
            return all(res)
        return False


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
        if(ret.find('.') != -1):
            return ret
    else:
        ret = get_simple_name_num()
    # at here: only file name had been created, no extension here.
    if(ftype == 'application/octet-stream'):
        fname = rq.headers['Content-Disposition'].split('=')[1]
        ftype = fname.split('.')[1]
        ret = ret + '.' + ftype
    elif(ftype[0:6] == 'image/'):
        ret = ret + '.' + ftype[6:]
    else:
        ret = ret + '.jpeg'
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


def safefilter(img, to=None):
    if(img.split('.')[-1].lower() == 'gif'):
        return None
    if(img is None):
        return None
    if(to is None):
        to = img
    try:
        im = Image.open(img)
    except OSError as e:
        raise e
    im = Image.eval(im, lambda x: x-50).convert('L')
    im = im.filter(ImageFilter.FIND_EDGES)
    # im = Image.eval(im, lambda x: 256-x) # white image
    try:
        if(img.split('.')[-1].lower() != 'gif'):
            im.save(to)
    except OSError as e:
        im.convert('RGB').save(to)
    return to


def smallfilter(img, to=None):
    if(img.split('.')[-1].lower() == 'gif'):
        return None
    if(img is None):
        return None
    if(to is None):
        to = img
    try:
        im = Image.open(img)
    except OSError as e:
        raise e
    while(im.size[0] > 300 or im.size[1] > 300):
        smallsize = (int(im.size[0] * 0.5), int(im.size[1] * 0.5))
        im = im.resize(smallsize, Image.ANTIALIAS)
    try:
        im.save(to)
    except OSError as e:
        im.convert('RGB').save(to)
    return to


if(__name__ == '__main__'):
    ffrom = 'default.jpg'
    if(len(argv) > 1):
        ffrom = argv[1]
    print('converted "%s" into "safe.jpg"' % ffrom)
    ffrom = 'image//' + ffrom
    sfwimage(ffrom, 'image//safe.jpg')
