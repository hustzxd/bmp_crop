import sys
import os


def delete_bmp(dir0):
    files = os.listdir(dir0)
    count = 0
    for f in files:
        if count % 2 != 0:
            os.remove(os.path.join(dir0, f))
            count += 1
            count %= 2
        else:
            count += 1
            count %= 2


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python bmp data dir'
        exit(1)
    dir0 = sys.argv[1]
    delete_bmp(dir0)
