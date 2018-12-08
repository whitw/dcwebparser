from dclist import dclist as dl
from dcpage import dcpage as dp
import os
import sys
from error import print_error_msg, NoGalleryError
from command import command, command_book
from image import imagemachine, safefilter, smallfilter

book = command_book()
imagemode = imagemachine([safefilter, smallfilter])
tinyimg = True
safeimg = True
shortname = True
gallery = ''
view_recommend = False
last_list = None


def f_view_recommend(argvs):
    global view_recommend
    view_recommend = not view_recommend
    print('view_recommend mode is now', 'On' if view_recommend else 'Off')


def f_exit(argvs):
    sys.exit(0)


def f_clear(argvs):
    os.system('clear')


def f_gallery(argvs):
    global gallery
    argv = argvs.split(' ')
    try:
        dl(argv[0], 1).get()
    except NoGalleryError:
        print("There is no gallery named " + argv[0] + "!")
    else:
        gallery = argv[0]
        print("You can now access on gallery " + gallery)


def f_small_img(argvs):
    global tinyimg
    tinyimg = not tinyimg
    imagemode.toggle(smallfilter, tinyimg)
    print('tiny image mode is now', 'On' if tinyimg else 'Off')


def f_short_name(argvs):
    global shortname
    shortname = not shortname
    print('short named image mode is now', 'On' if shortname else 'Off')


def f_safe(argvs):
    global safeimg
    safeimg = not safeimg
    imagemode.toggle(safefilter, safeimg)
    print('safe image mode is now', 'On' if safeimg else 'Off')


def f_list(argvs):
    global last_list
    argv = argvs.split(' ')
    if(argv[0] == ''):
        argv[0] = 1
    try:
        no = int(argv[0])
    except ValueError:
        raise ValueError('Please enter valid number.')
    last_list = dl(gallery, no, view_recommend, simple_image_name=shortname)
    last_list.show()


def f_get(argvs):
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
        last_list = dl(gallery, no, view_recommend,
                       simple_image_name=shortname)
    page = last_list[page]
    if(page is not None):
        page.show()
        imagemode(page.get_image())


def f_get_all(argvs):
    global last_list
    argv = argvs.split(' ')
    if(argv[0] == ''):
        argv[0] = 1
    try:
        no = int(argv[0])
    except ValueError:
        raise ValueError('Please enter valid number.')
    if(last_list is None):
        last_list = dl(gallery, no, view_recommend,
                       simple_image_name=shortname)
    for page in last_list:
        page.show()
        imagemode(page.get_image())


def f_page(argvs):
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
    page = dp(gallery, no, simple_image_name=shortname)
    page.show()
    imagemode(page.get_image())


def f_search(argvs):
    argv = argvs.split(' ')
    search_type = 0
    page = 1
    if(argv[0] == ''):
        raise TypeError('Please Enter the keyword!')
    else:
        keyword = argv[0]
    if(len(argv) > 1):
        search_type = argv[1]
    if(len(argv) > 2):
        page = argv[2]
    pass


def f_get_all_images(argvs):
    global last_list
    argv = argvs.split(' ')
    if(last_list is None):
        last_list = dl(gallery, no, view_recommend)
    for page in last_list:
        imagemode(page.get_image())
        page.download_image()


book.append(command(
    'view_recommend',
    'usage: view_recommend\ntoggle showing recommended pages only',
    f_view_recommend
))
book.append(command('exit', 'usage: exit\nend program', f_exit))
book.append(command('safe', 'usage: safe\ntoggle safe image mode', f_safe))
book.append(command(
    'short',
    'usage: short\ntoggle short named image mode',
    f_short_name
))
book.append(command(
    'tinyimg',
    'usage: tinyimg\ntoggle whether to download images as small size',
    f_small_img
))
book.append(command('clear', 'usage: clear\nclear the screen', f_clear))
book.append(command(
    'gallery',
    'usage: gallery [gallery]\nset gallery',
    f_gallery
))
book.append(command(
    'list',
    '''usage: list (number of list page)
get list of n-th page''',
    f_list
))
book.append(command(
    'page',
    '''usage: page [number of page]
get page on the gallery by index number''',
    f_page
))
book.append(command(
    'get',
    '''usage: get (i-th) (number of list page)
get n-th page on the gallery page list''',
    f_get
))
book.append(command(
    'get_all',
    '''usage: get_all (number of list page)
get every pages on the list''',
    f_get_all
))
book.append(command(
    'search',
    '''usage: search [keyword] (search_type) (page)
search_type = 0:all, 1:by title, 2:by text,
3:by name, 4:by title and text
search some keyword in gallery.
use (search_type) to set how to search the keyword.
use (page) to view next list of result''',
    f_search
))
book.append(command(
    'get_all_image',
    '''usage: get_all_image (number of list page)
    get all images in the list''',
    f_get_all_images
))


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
