import cv2 as cv
import os
import sys
import time
import shutil
import math
import matplotlib.pyplot as plt


def crop_image(num_path, crop_num_path, bmp_name, w_num, h_num, isSecond):
    cell_size = 328
    cell_gap_w = 490
    cell_gap_h = 375
    bmp_path = os.path.join(num_path, bmp_name)
    print 'Crop ' + bmp_path + ' ...'
    src_image = cv.imread(bmp_path)
    height = src_image.shape[0]
    width = src_image.shape[1]
    print src_image.shape
    gray_image = cv.cvtColor(src_image, cv.COLOR_BGR2GRAY)
    print gray_image.shape

    sum_x = gray_image.sum(axis=1)
    sum_y = gray_image.sum(axis=0)

    mean_x = sum_x.mean() * 0.8
    mean_y = sum_y.mean() * 0.8
    # plt.plot(sum_y)
    # plt.show()
    result_x = []
    result_y = []
    for i in xrange(sum_x.shape[0] - 1):
        if sum_x[i] < mean_x < sum_x[i + 1]:
            result_x.append(i)
        if sum_x[i] > mean_x > sum_x[i + 1]:
            result_x.append(i)
    for i in xrange(sum_y.shape[0] - 1):
        if sum_y[i] < mean_y < sum_y[i + 1]:
            result_y.append(i)
        if sum_y[i] > mean_y > sum_y[i + 1]:
            result_y.append(i)

    coord_x = []
    coord_y = []
    index = 0
    while index < len(result_y) - 1:
        first = result_y[index]
        for j in xrange(index + 1, len(result_y)):
            second = result_y[j]
            if second - first - cell_size > 30:
                break
            if math.fabs(second - first - cell_size) < 31:
                coord_x.append(first)
                # coord_x_start = first
                index = j
                continue
        index += 1

    index = 0
    # this can improve, it perform
    while index < len(result_x) - 1:
        first = result_x[index]
        for j in xrange(index + 1, len(result_x)):
            second = result_x[j]
            if second - first - cell_size > 30:
                break
            if math.fabs(second - first - cell_size) < 31:
                coord_y.append(first)
                # coord_y_start = first
                index = j
                continue
        index += 1
    # coord_y may be less than truth
    coord_y_big = []
    while isSecond and len(coord_y) < 7:
        print coord_y
        coord_y.append(coord_y[len(coord_y) - 1] + cell_gap_h)
    while (not isSecond) and len(coord_y) < 8:
        print coord_y
        coord_y.append(coord_y[len(coord_y) - 1] + cell_gap_h)
    print 'generate ' + str(len(coord_x)) + 'x' + str(len(coord_y)) + ' small bmps'
    # print coord_x
    # print coord_y
    for i in xrange(len(coord_x)):
        for j in xrange(len(coord_y)):
            crop_img = src_image[coord_y[j]:(coord_y[j] + cell_size), coord_x[i]:(coord_x[i] + cell_size), :]
            cv.imwrite(crop_num_path + "/" + str(w_num + i) + "x" + str(h_num + j) + ".bmp", crop_img)
            print crop_num_path + "/" + str(w_num + i) + "x" + str(h_num + j) + ".bmp"
    return (len(coord_x)) * (len(coord_y))


def copy_xml(num_path, crop_num_path):
    files = os.listdir(num_path)
    for f in files:
        if f.endswith('xml'):
            src = os.path.join(num_path, f)
            dst = os.path.join(crop_num_path, f)
            shutil.copyfile(src, dst)


def crop_images(num_path, crop_num_path):
    total = 0
    bmp_list = [['11.bmp', '12.bmp', '13.bmp', '14.bmp', '15.bmp'],
                ['21.bmp', '22.bmp', '23.bmp', '24.bmp', '25.bmp']]
    width_num = [1, 4, 11, 18, 25]
    height_num = [1, 9]
    for w in xrange(5):
        for h in xrange(2):
            total += crop_image(num_path, crop_num_path, bmp_list[h][w], width_num[w], height_num[h], h == 1)
    return total


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


def crop_images_dir(root_dir):
    total = 0
    region_data_path = os.path.join(root_dir, 'region_data')
    # region_data_path = os.path.join(root_dir, 'region_test')
    crop_data_path = os.path.join(root_dir, 'crop_data')
    # crop_data_path = os.path.join(root_dir, 'crop_test')

    date_dirs = os.listdir(region_data_path)
    for date_dir in date_dirs:
        date_path = os.path.join(region_data_path, date_dir)
        crop_date_path = os.path.join(crop_data_path, date_dir)
        num_dirs = os.listdir(date_path)
        for num_dir in num_dirs:
            num_path = os.path.join(date_path, num_dir)
            crop_num_path = os.path.join(crop_date_path, num_dir)
            mk_dir(crop_num_path)
            total = total + crop_images(num_path, crop_num_path)
            copy_xml(num_path, crop_num_path)
    return total


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python bmp data dir'
        exit(1)
    data_dir = sys.argv[1]
    start = time.time()
    total_num = crop_images_dir(data_dir)
    end = time.time()
    print 'time: ' + str(end - start) + 's'
    print 'numbers: ' + str(total_num)
    print 'fps: ' + str(total_num / (end - start))
