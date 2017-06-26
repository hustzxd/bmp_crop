import sys
import os


def readMap():
    wrong_map = {}
    with open('wrong_map.txt', 'r') as f:
        for line in f:
            # print line
            wrong_index, index = map(int, line.split(' '))
            # print wrong_index, index
            wrong_map[wrong_index] = index
    return wrong_map


def getlist(data_dir):
    wrong_map = readMap()
    train_dir = os.path.join(data_dir, 'train')
    train_file = open('train.txt', 'w')
    num_dirs = os.listdir(train_dir)
    for num in num_dirs:
        val = wrong_map[int(num)]
        if val == -1:
            continue
        num_dir = os.path.join(train_dir, num)
        bmps = os.listdir(num_dir)
        for bmp in bmps:
            train_file.write(os.path.join(num_dir, bmp) + ' ' + str(val) + '\n')
    train_file.close()

    val_dir = os.path.join(data_dir, 'val')
    val_file = open('val.txt', 'w')
    num_dirs = os.listdir(val_dir)
    for num in num_dirs:
        val = wrong_map[int(num)]
        if val == -1:
            continue
        num_dir = os.path.join(val_dir, num)
        bmps = os.listdir(num_dir)
        for bmp in bmps:
            val_file.write(os.path.join(num_dir, bmp) + ' ' + str(val) + '\n')
    val_file.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python bmp data dir'
        exit(1)
    data_dir = sys.argv[1]
    getlist(data_dir)
