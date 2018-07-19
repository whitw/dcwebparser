import dclist
import dcpage


if(__name__ == "__main__"):
    if(len(sys.argv) > 2):
        gallery = sys.argv[1]
        no = sys.argv[2]
        print("gallery = {0},no = {1}".format(gallery, no))
    else:
        gallery = 'programming'
        no = '1'


result = None
# result = getpage(gallery, no, '1')
if(result is None or result['title'] is None):
    pass
else:
    # print('title= {0}'.format(result['title']))
    # print('head.get_text = {0}'.format(result['nick'].get_text()))
    # ('body = \n{0}'.format(result['body'].get_text().strip()))
    pass
result = getlist(gallery, '1')
# for data in result:
# getpage(gallery, data['no'], '1')
# print('\n\n')
