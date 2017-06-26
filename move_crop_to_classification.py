import sys
import time
import os
import xml.dom.minidom as xml
from shutil import copyfile

result = {}
for i in xrange(30):
    result[i] = 0


def mk_dir(path):
    path = path.strip()
    path = path.rstrip("\\")
    is_exists = os.path.exists(path)
    if not is_exists:
        print 'mkdir:' + path
        os.makedirs(path)
        return True
    else:
        return False


def readXML(num_path, xml_path, header, dst_dir):
    dom = xml.parse(xml_path)
    root = dom.documentElement
    wrong_position = root.getElementsByTagName('WrongPosition')
    wrong_list = []
    print len(wrong_position)

    # num_path = os.path.join(xml_path, '..')
    for item in wrong_position:
        # wrong_index = int(item.firstChild.data)
        x = item.getElementsByTagName('X')[0].firstChild.data
        y = item.getElementsByTagName('Y')[0].firstChild.data
        wrong_index = int(item.getElementsByTagName('WrongIndex')[0].firstChild.data)
        print x, y, wrong_index
        wrong_list.append(x + 'x' + y)
        mk_dir(os.path.join(dst_dir, str(wrong_index)))
        src = os.path.join(num_path, x + 'x' + y + '.bmp')
        dst = os.path.join(dst_dir, str(wrong_index), header + x + 'x' + y + '.bmp')
        copyfile(src, dst)

    for x in xrange(32):
        for y in xrange(15):
            file_name = str(x + 1) + 'x' + str(y + 1)
            if file_name not in wrong_list:
                print xml_path + str(x + 1) + 'x' + str(y + 1), 0
                src = os.path.join(num_path, file_name + '.bmp')
                mk_dir(os.path.join(dst_dir, '0'))
                dst = os.path.join(dst_dir, '0', header + file_name + '.bmp')
                copyfile(src, dst)


def move_file(root_dir, dst_dir):
    date_dirs = os.listdir(root_dir)
    for date_dir in date_dirs:
        date_path = os.path.join(root_dir, date_dir)
        num_dirs = os.listdir(date_path)
        for num_dir in num_dirs:
            num_path = os.path.join(date_path, num_dir)
            files = os.listdir(num_path)
            for f in files:
                if f.endswith('xml'):
                    xml_path = os.path.join(num_path, f)
                    print xml_path
                    readXML(num_path, xml_path, date_dir + '_' + num_dir + '_', dst_dir)
                    break


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python bmp data dir'
        exit(1)
    data_dir = sys.argv[1]
    start = time.time()
    move_file(data_dir, '/home/share/bmp_crop/data/classification')
    # readXMLs(data_dir, True)
    # readXMLs(data_dir, False)
    print str(result)
