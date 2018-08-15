import os
from PIL import Image, ImageFilter
from urllib.request import urlretrieve
file = 'img_index.txt'


def request_image_simple(src):
    if(src is None):
        return None
    if(os.path.exists(file) is not True):
        with open(file, 'wt') as f:
            f.write('0')
    pos = 0
    with open(file, 'rt') as f:
        try:
            pos = f.read()
        except Exception:
            pos = 'image'
    imgpos = 'image//' + pos + '.jpg'
    urlretrieve(src, imgpos)
    with open(file, 'wt') as f:
        pos = int(pos)
        pos = pos + 1
        pos = str(pos)
        f.write(pos)
    return imgpos


def sfwimage(img):
    im = Image.open(img)
    im = Image.eval(im, lambda x: x-32).convert('L')
    im = im.filter(ImageFilter.FIND_EDGES)
    smallsize = (int(im.size[0] * 0.25), int(im.size[1] * 0.25))
    im = im.resize(smallsize, Image.ANTIALIAS)
    im.save(img)
    return img


if(__name__ == '__main__'):
    sfwimage('image//29.jpg')
