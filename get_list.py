import sys
import time
import os
import xml.dom.minidom as xml

result = {}
for i in xrange(30):
    result[i] = 0


def readXML(num_path, xml_path, wrong_map, f):
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
        if wrong_map[wrong_index] != -1:
            print xml_path, x+'x'+y, wrong_map[wrong_index]
            f.write(num_path + '/' + x + 'x' + y + '.bmp' + ' ' + str(wrong_map[wrong_index]) + '\n')
    for x in xrange(32):
        for y in xrange(15):
            if str(x+1)+'x'+str(y+1) not in wrong_list:
                print xml_path + str(x+1)+'x'+str(y+1), 0
                f.write(num_path + '/' + str(x+1) + 'x' + str(y+1) + '.bmp' + ' ' + str(0) + '\n')


def readMap():
    wrong_map = {}
    with open('wrong_map.txt', 'r') as f:
        for line in f:
            # print line
            wrong_index, index = map(int, line.split(' '))
            # print wrong_index, index
            wrong_map[wrong_index] = index
    return wrong_map


def readXMLs(root_dir, isTrain):
    total = 0
    wrong_map = readMap()
    if isTrain:
        train_data_path = os.path.join(root_dir, 'train')
        train_val_file = open('train.txt', 'w')
    else:
        train_data_path = os.path.join(root_dir, 'val')
        train_val_file = open('val.txt', 'w')
    date_dirs = os.listdir(train_data_path)
    for date_dir in date_dirs:
        date_path = os.path.join(train_data_path, date_dir)
        num_dirs = os.listdir(date_path)
        for num_dir in num_dirs:
            num_path = os.path.join(date_path, num_dir)
            files = os.listdir(num_path)
            for f in files:
                if f.endswith('xml'):
                    xml_path = os.path.join(num_path, f)
                    print xml_path
                    readXML(num_path, xml_path, wrong_map, train_val_file)
                    break
    train_val_file.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python bmp data dir'
        exit(1)
    data_dir = sys.argv[1]
    start = time.time()
    readXMLs(data_dir, True)
    readXMLs(data_dir, False)
    print str(result)
