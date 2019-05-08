from dclist import dclist as dl
from dcpage import dcpage as dp
import os
import sys
from error import print_error_msg, NoGalleryError
from command import command, command_book
from image import imagemachine, safefilter, smallfilter

book = command_book()
imagemode = imagemachine([safefilter, smallfilter])
tiny_img = False
safe_img = False
shortname = True
gall = ''
view_recommend = False
last_list = None
index_in_list = 0


def commanddeco(func):
    book.append(command(
        func.__name__,
        func.__doc__,
        func
    ))
    return func


@commanddeco
def view_recommend(argvs):
    '''usage: view_recommend
toggle showing recommended pages only'''
    global view_recommend
    view_recommend = not view_recommend
    print('view_recommend mode is now', 'On' if view_recommend else 'Off')


@commanddeco
def exit(argvs):
    '''usage: exit
end program'''
    sys.exit(0)


@commanddeco
def clear(argvs):
    '''usage: clear
clear the screen'''
    os.system('clear')


@commanddeco
def gallery(argvs):
    '''usage: gallery [gallery]
set gallery to [gallery]'''
    global gall
    argv = argvs.split(' ')
    try:
        dl(argv[0], 1).get()
    except NoGalleryError:
        print("There is no gallery named " + argv[0] + "!")
    else:
        gall = argv[0]
        print("You can now access on gallery " + gall)


@commanddeco
def tinyimg(argvs):
    '''usage: tinyimg
toggle whether to download images as small size'''
    global tiny_img
    tiny_img = not tiny_img
    imagemode.toggle(smallfilter, tiny_img)
    print('tiny image mode is now', 'On' if tiny_img else 'Off')


@commanddeco
def short(argvs):
    '''usage: short
toggle short named image mode'''
    global shortname
    shortname = not shortname
    print('short named image mode is now', 'On' if shortname else 'Off')


@commanddeco
def safeimg(argvs):
    '''usage: safe
toggle safe image mode'''
    global safe_img
    safe_img = not safe_img
    imagemode.toggle(safefilter, safe_img)
    print('safe image mode is now', 'On' if safe_img else 'Off')


@commanddeco
def list(argvs):
    '''usage: list (number of list page)
get list of n-th page'''
    global last_list
    argv = argvs.split(' ')
    if(argv[0] == ''):
        argv[0] = 1
    try:
        no = int(argv[0])
    except ValueError:
        raise ValueError('Please enter valid number.')
    last_list = dl(gall, no, view_recommend, simple_image_name=shortname)
    last_list.show()


@commanddeco
def get(argvs):
    '''usage: get (i-th) (number of list page)
get n-th page on the gallery page list'''
    global last_list
    argv = argvs.split(' ')
    if(argv[0] == ''):
        argv[0] = 0
    try:
        page = int(argv[0])
    except ValueError:
        raise ValueError('Please enter valid number.')
    try:
        no = int(argv[1])
    except IndexError:
        no = 1
    except ValueError:
        raise ValueError('Please enter valid number.')
    if(last_list is None):
        last_list = dl(gall, no, view_recommend,
                       simple_image_name=shortname)
    page = last_list[page]
    if(page is not None):
        page.show()
        imagemode(page.get_image())


@commanddeco
def get_all(argvs):
    '''usage: get_all (number of list page)
get every pages on the list'''
    global last_list
    argv = argvs.split(' ')
    if(argv[0] == ''):
        argv[0] = 1
    try:
        no = int(argv[0])
    except ValueError:
        raise ValueError('Please enter valid number.')
    if(last_list is None):
        last_list = dl(gall, no, view_recommend,
                       simple_image_name=shortname)
    for page in last_list:
        page.show()
        imagemode(page.get_image())


@commanddeco
def page(argvs):
    '''usage: page [number of page]
get page on the gallery by index number'''
    global last_list
    argv = argvs.split(' ')
    if(argv[0] == ''):
        argv[0] = 1
    try:
        no = int(argv[0])
    except IndexError:
        raise ValueError('Please Enter the number of page!')
    except ValueError:
        raise ValueError('Please enter valid number.')
    last_list = None
    page = dp(gall, no, simple_image_name=shortname)
    page.show()
    imagemode(page.get_image())


@commanddeco
def search(argvs):
    '''usage: search ['keyword'] (page) (search_type)
keyword must be in two apostrophe.
search_type =
0:all, 1:by title, 2:by text,
3:by name, 4:by title and text
search some keyword in gallery.
use (page) to view page-th list of result
use (search_type) to set how to search the keyword.'''
    global last_list
    argv = argvs.split("'")
    if (argv[0] == '') is False:
        raise TypeError("keywords must be within two apostrophe!('')")
    keyword = argv[1]

    argvs = argv[2].lstrip()
    argv = argvs.split(' ')

    if(len(argv) > 0):
        page = argv[0]
    else:
        page = '1'

    if(len(argv) > 1):
        search_type = argv[1]
    else:
        search_type = 'all'

    '''
    잠깐 여기서 정리좀 할게요
    만약에 문장이 여러 단어인 경우에는???
    search 한단어
    search 여러 단어
    search '여러 단어 1'
    search '여러 단어 1 2'
    search 여러 단어 1
    search 여러 단어 1 2
    search 여러 단어 1 얼씨구
    다음 일곱가지가 나온다.
    무조건 문장은 ''로 싸게 하자. 그러면 argvs를 자르는 것도 ''를 기준으로 하면 되는 거 아닌가.
    그러면 다음 몇가지로 압축이 된다.
    search '문장'
    search '문장' 1
    search '문장' 1 2
    아님 search 문장' 1 2형태로 시켜버릴까.... 흠 아냐 이건 모양이 구려.
    이러면 쉽지. split만 잘 해주면 되겠네.
    먼저 '를 기준으로 split을 해주면
    [0] = ""고
    [1] = "문장"이고
    [2] = " 1 2"니까
    [2].strip().split(' ')해주면 되겠네.
    '''
    last_list = dl(gall, page, view_recommend,
                   search_by=search_type, search_keyword=keyword,
                   simple_image_name=shortname)
    last_list.search()
    last_list.show()


@commanddeco
def get_all_images(argvs):
    '''usage: get_all_image (number of list page)
get all images in the list'''
    global last_list
    argv = argvs.split(' ')
    if(last_list is None):
        last_list = dl(gall, no, view_recommend)
    for page in last_list:
        imagemode(page.get_image())
        page.download_image()


def exec(string):
    cmd = string.split(' ')[0]
    argv = string[len(cmd) + 1:]
    return book.command[cmd].exec(argv)
    # for case that it need to return some value...
    # I actually think that it is highly possible to become a None


if(__name__ == "__main__"):
    while(True):
        try:
            string = input('>>>')
        except KeyboardInterrupt:
            print("Ending Program...")
            break
        except UnicodeDecodeError:
            print("Can't decode unicode. Please retry again...")
            continue
        try:
            ret = exec(string)
            if(ret is not None):
                print(ret)
        except KeyError:
            print("There is no command like that! try 'help' to get help.")
        except ValueError as e:
            print_error_msg(e)
        except TypeError as e:
            print_error_msg(e)
        except NoGalleryError as e:
            print_error_msg(e)
        except ConnectionResetError:
            print("Connection Reset Occured. Please retry again...")
        except Exception as e:
            raise e
