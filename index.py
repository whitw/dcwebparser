import dclist as dl
import dcpage as dp


if(__name__ == "__main__"):
    stat = {
        'last': None,
        'gallery': None,
        'no': 1,
        'keyword': None,
        'search_type': 0,
        'view_recommend': False
    }
    while(True):
        try:
            string = input('>>>').split(' ')
        except KeyboardInterrupt:
            print("Ending Program...")
            break
        except UnicodeDecodeError:
            print("Can't decode unicode. Please retry again...")
            continue

# one_word commands

        if(string[0] == 'help'):
            print('list [gallery] (page)')
            print('page [gallery] [page_number]')
            print('search [gallery] [keyword] (search_type) (page)')
            print('search_type = 0:all, 1:by title, 2:by text, ' +
                  '3:by name, 4:by title and text')
            print('next or n')
            print('before or back or p or b')
            continue
        elif(string[0] == 'view_recommend'):
            stat['view_recommend'] = not stat['view_recommend']
            print(
                'view_recommend mode is now {0}'.format(stat['view_recommend'])
            )
            continue
        elif(string[0] == 'exit'):
            break

# over_one_word commands

        if(len(string) > 1):
            stat['gallery'] = string[1]
        else:
            print("use 'command [gallery] (if search:keyword) (no)'")
            continue

        if(len(string) > 2 and string[2].isnumeric() is True):
            stat['no'] = string[2]
        else:
            stat['no'] = 1

        if(string[0] == 'list'):
            stat['last'] = 'list'
            dl.show(dl.get(
                stat['gallery'],
                stat['no'],
                stat['view_recommend']
            ))

        elif(string[0] == 'page' or string[0] == 'view'):
            stat['last'] = 'page'
            dp.show(dp.get(stat['gallery'], stat['no']))

        elif(string[0] == 'get'):
            if(len(string) > 3 and string[3].isnumeric() is True):
                page = int(string[3])
                dl_dictionary = dl.get(
                    stat['gallery'],
                    stat['no'],
                    stat['view_recommend']
                )
                dp_id = dl_dictionary[page]['no']
                stat['no'] = dp_id
                stat['last'] = page
                dp.show(dp.get(stat['gallery'], stat['no']))

        elif(string[0] == 'search'):
            if(len(string) > 2):
                stat['last'] = 'search'
                stat['keyword'] = string[2]
            else:
                print("Too little parameter!")
                print('search [gallery] [keyword] (search_type) (page)')
                print(
                    'search_type = 0:all, 1:by title, 2:by text, ' +
                    '3:by name, 4:by title and text'
                )

            try:
                stat['search_type'] = int(string[3])
            except TypeError:
                continue
            except IndexError:
                stat['search_type'] = 0

            try:
                stat['no'] = int(string[4])
            except TypeError:
                continue
            except IndexError:
                stat['no'] = '1'

            dl.show(dl.search(
                gallery=stat['gallery'],
                page=stat['no'],
                search_type=stat['search_type'],
                keyword=stat['keyword'],
                view_recommend=stat['view_recommend']
                ))
