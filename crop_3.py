# -*-coding:utf-8-*-
import cv2 as cv
import os
import sys
import time
import shutil
import math
import logging
import logging.handlers
import matplotlib.pyplot as pltforever


def crop_image(num_path, crop_num_path, bmp_name, w_num, h_num, isFour, header):
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
    # while isSecond and len(coord_y) < 7:
    #     print coord_y
    #     coord_y.append(coord_y[len(coord_y) - 1] + cell_gap_h)
    # while (not isSecond) and len(coord_y) < 8:
    #     print coord_y
    #     coord_y.append(coord_y[len(coord_y) - 1] + cell_gap_h)
    # print 'generate ' + str(len(coord_x)) + 'x' + str(len(coord_y)) + ' small bmps'
    print coord_x
    print coord_y
    if isFour:
        if len(coord_x) != 4:
            logger.error(bmp_path + ' coord_x should be 4 but got ' + str(len(coord_x)))
    elif len(coord_x) != 7:
        logger.error(bmp_path + ' coord_x should be 7 but got ' + str(len(coord_x)))

    if len(coord_y) != 5:
        logger.error(bmp_path + ' coord_y should be 5 but got ' + str(len(coord_y)))
    for i in xrange(len(coord_x)):
        for j in xrange(len(coord_y)):
            crop_img = src_image[coord_y[j]:(coord_y[j] + cell_size), coord_x[i]:(coord_x[i] + cell_size), :]
            cv.imwrite(crop_num_path + "/" + header + '_' + str(w_num + i) + "x" + str(h_num + j) + ".bmp", crop_img)
            print crop_num_path + "/" + str(w_num + i) + "x" + str(h_num + j) + ".bmp"
    return (len(coord_x)) * (len(coord_y))


def crop_images(num_path, crop_num_path, header):
    total = 0
    bmp_list = [['11_看图王.bmp', '12_看图王.bmp', '13_看图王.bmp', '14_看图王.bmp', '15_看图王.bmp'],
                ['21_看图王.bmp', '22_看图王.bmp', '23_看图王.bmp', '24_看图王.bmp', '25_看图王.bmp'],
                ['31_看图王.bmp', '32_看图王.bmp', '33_看图王.bmp', '34_看图王.bmp', '35_看图王.bmp']]
    width_num = [1, 5, 12, 19, 26]
    height_num = [1, 6, 11]
    for w in xrange(5):
        for h in xrange(3):
            total += crop_image(num_path, crop_num_path, bmp_list[h][w], width_num[w], height_num[h], w == 0, header)
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
    region_data_path = os.path.join(root_dir, 'region_data_2')
    # region_data_path = os.path.join(root_dir, 'region_test')
    crop_data_path = os.path.join(root_dir, 'crop_data_2')
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
            total = total + crop_images(num_path, crop_num_path, num_dir)
    return total


def init_logger():
    logger = logging.getLogger("loggingmodule.NomalLogger")
    handler = logging.FileHandler("crop_bmp.log")
    formatter = logging.Formatter("[%(levelname)s][%(funcName)s][%(asctime)s]%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python bmp data dir'
        exit(1)
    data_dir = sys.argv[1]
    logger = init_logger()
    start = time.time()
    total_num = crop_images_dir(data_dir)
    end = time.time()
    print 'time: ' + str(end - start) + 's'
    print 'numbers: ' + str(total_num)
    print 'fps: ' + str(total_num / (end - start))
