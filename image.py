import os
from urllib.request import urlretrieve
file = 'img_index.txt'


def request_image_simple(src):
    if(os.path.exists(file) is not True):
        with open(file, 'wt') as f:
            f.write('0')
    pos = 0
    with open(file, 'rt') as f:
        try:
            pos = f.read()
        except Exception:
            pos = 'image'
    urlretrieve(src, 'image//' + pos + '.jpg')
    with open(file, 'wt') as f:
        pos = int(pos)
        pos = pos + 1
        pos = str(pos)
        f.write(pos)


if(__name__ == '__main__'):
    request_image_simple(
        'http://dcimg7.dcinside.co.kr/viewimageM.php?'
        + 'id=jumper&no=24b0d769e1d32ca73fef80fa11d028314d28878'
        + 'c8e439571894d71b565e5c7cb89eaaf550bd31b6d115'
        + 'ba7f0007c7ede3eafba192667db7099f0d5cca6'
        + '44c4e168978e6379a9bb&f_no=7ce88374bc816cf'
        + '63ee898bf06d698c2681f6a298a39b3edbf7'
        + '4d862b5adca7657fd2f5a60da4edd8b4571451fa'
        )
