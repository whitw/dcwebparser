import dclist as dl
from dcpage import dcpage as dp
import os
import sys
from error import print_error_msg
from command import command, command_book


book = command_book()
stat = {
    'last': [],
    'last_page': None,
    'gallery': '',
    'no': 1,
    'keyword': None,
    'search_type': 0,
    'view_recommend': False,
    'safe': True,
    'short_name': True,
    'small_img': True
}


def f_view_recommend(argvs):
    stat['view_recommend'] = not stat['view_recommend']
    print(
        'view_recommend mode is now {0}'.format(stat['view_recommend'])
    )
    stat['last'] = []
    stat['last_page'] = None


def f_exit(argvs):
    sys.exit(0)


def f_clear(argvs):
    os.system('clear')


def f_gallery(argvs):
    gallery = argvs.split(' ')[0]
    if(gallery == ''):
        if(stat['gallery'] == ''):
            print('set gallery first!')
        else:
            print('you are now on gallery "%s"' % stat['gallery'])
        return
    if(dl.get(gallery, 1, False) is not None):
        stat['gallery'] = gallery
        print('you now access on gallery "%s"' % stat['gallery'])
    stat['last'] = []
    stat['last_page'] = None


def f_small_img(argvs):
    stat['small_img'] = not stat['small_img']
    print(
        'small image mode is now {0}'.format(stat['small_img'])
    )


def f_short_name(argvs):
    stat['short_name'] = not stat['short_name']
    print(
        'short_named image mode is now {0}'.format(stat['short_name'])
    )


def f_safe(argvs):
    stat['safe'] = not stat['safe']
    print(
        'safe image mode is now {0}'.format(stat['safe'])
    )


def f_list(argvs):
    argv = argvs.split(' ')
    if(argv[0] == ''):
        argv[0] = 1
    try:
        stat['no'] = int(argv[0])
    except ValueError:
        raise ValueError('Please enter valid number.')
    stat['last'] = dl.get(
            stat['gallery'],
            stat['no'],
            stat['view_recommend']
        )
    dl.show(stat['last'])
    stat['last_page'] = None


def f_get(argvs):
    argv = argvs.split(' ')
    if(argv[0] == ''):
        argv[0] = 0
    try:
        page = int(argv[0])
    except ValueError:
        raise ValueError('Please enter valid number.')
    try:
        stat['no'] = int(argv[1])
    except IndexError:
        stat['no'] = 1
    except ValueError:
        raise ValueError('Please enter valid number.')
    if(stat['last'] == []):
        dl_list = dl.get(
            stat['gallery'],
            stat['no'],
            stat['view_recommend']
        )
        if(dl_list is None):
            return
        else:
            stat['last'] = dl_list
    else:
        dl_list = stat['last']
    try:
        dp_id = dl_list[page]['no']
    except IndexError:
        return
    except TypeError:
        return
    stat['no'] = dp_id
    page = dp(
            stat['gallery'],
            no=stat['no'],
            safe=stat['safe'],
            simple_name=stat['short_name'],
            small_img=stat['small_img']
        )
    page.show()
    # page.debug()
    stat['last_page'] = page


def f_get_all(argvs):
    argv = argvs.split(' ')
    if(argv[0] == ''):
        argv[0] = 1
    try:
        stat['no'] = int(argv[0])
    except ValueError:
        raise ValueError('Please enter valid number.')
    if(stat['last'] == []):
        dl_list = dl.get(
            stat['gallery'],
            stat['no'],
            stat['view_recommend']
        )
    else:
        dl_list = stat['last']
    for dl_page in dl_list:
        dp(stat['gallery'],
            no=stat['no'],
            safe=stat['safe'],
            simple_name=stat['short_name'],
            small_img=stat['small_img']).show()
    stat['last_page'] = dl_list[-1]


def f_page(argvs):
    argv = argvs.split(' ')
    if(argv[0] == ''):
        argv[0] = 1
    try:
        stat['no'] = int(argv[0])
    except IndexError:
        raise IndexError('Please Enter the number of page!')
    except ValueError:
        raise ValueError('Please enter valid number.')
    page = dp(stat['gallery'],
              no=stat['no'],
              safe=stat['safe'],
              simple_name=stat['short_name'],
              small_img=stat['small_img'])
    page.show()
    stat['last_page'] = page


def f_search(argvs):
    argv = argvs.split(' ')
    search_type = 0
    page = 1
    if(argv[0] == ''):
        raise IndexError('Please Enter the keyword!')
    else:
        keyword = argv[0]
    if(len(argv) > 1):
        search_type = argv[1]
    if(len(argv) > 2):
        page = argv[2]
    stat['last'] = dl.search(
        stat['gallery'],
        keyword,
        page,
        search_type,
        stat['view_recommend']
    )
    dl.show(stat['last'])
    stat['last_page'] = None


def f_get_all_images(argvs):
    argv = argvs.split(' ')

    if(len(argv) > 1):
        try:
            page = int(argv[1])
        except ValueError:
            raise ValueError('Please enter valid number.')
    else:
        if(stat['last'] == []):
            dl_list = dl.get(
                stat['gallery'],
                stat['no'],
                stat['view_recommend']
            )
        else:
            dl_list = stat['last']
    for dl_page in dl_list:
        dp(stat['gallery'],
            no=stat['no'],
            safe=stat['safe'],
            simple_name=stat['short_name'],
            small_img=stat['small_img']).get_image()
    stat['last'] = dl_list
    stat['last_page'] = None


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
    book.command[cmd].exec(argv)


def new_command(newcmd):
    if(isinstance(newcmd, command)):
        book.append(command)
    else:
        raise AttributeError('Not a command class!')


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
            exec(string)
        except KeyError:
            print("There is no command like that! try 'help' to get help.")
        except IndexError as e:
            print_error_msg(e)
            continue
        except ValueError as e:
            print_error_msg(e)
            continue
        except TypeError as e:
            print_error_msg(e)
            continue
        except ConnectionResetError:
            print("Connection Reset Occured. Please retry again...")
        except Exception as e:
            raise e
        else:
            pass
