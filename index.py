import sys
import dclist
import dcpage


if(__name__ == "__main__"):
    if(len(sys.argv) == 2):
        gallery = sys.argv[1]
        for i in range(1, 5):
            dclist.printlist(dclist.getlist(sys.argv[1], str(i)))
    if(len(sys.argv) > 2):
        gallery = sys.argv[1]
        no = sys.argv[2]
        print("gallery = {0},no = {1}".format(gallery, no))
        dcpage.printpage(dcpage.getpage(gallery, no, page='1'))
    else:
        gallery = 'programming'
        no = '1'
