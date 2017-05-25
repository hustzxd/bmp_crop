import math
import sys
import cv2 as cv
import os
import time


def crop_image(bmp_name, dst_path):
    print 'Crop the ' + bmp_name + '...'
    src_image = cv.imread(bmp_name)
    gray_image = cv.cvtColor(src_image, cv.COLOR_BGR2GRAY)
    print gray_image.shape

    sum_x = gray_image.sum(axis=1)
    sum_y = gray_image.sum(axis=0)

    mean_x = sum_x.mean()

    mean_y = sum_y.mean()
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
        for j in xrange(index + 1, len(result_y) - 1):
            second = result_y[j]
            if second - first - 300 > 30:
                break
            if math.fabs(second - first - 300) < 30:
                coord_x.append(first)
                index = j
                continue
        index += 1
    index = 0
    while index < len(result_x) - 1:
        first = result_x[index]
        for j in xrange(index + 1, len(result_x) - 1):
            second = result_x[j]
            if second - first - 300 > 30:
                break
            if math.fabs(second - first - 300) < 30:
                coord_y.append(first)
                index = j
                continue
        index += 1
    print 'generate ' + str(len(coord_x)) + 'x' + str(len(coord_y)) + ' small bmps'

    for i in xrange(len(coord_x)):
        for j in xrange(len(coord_y)):
            crop_img = src_image[coord_y[j]:(coord_y[j] + 300), coord_x[i]:(coord_x[i] + 300), :]
            cv.imwrite(dst_path + "-" + str(i + 1) + "x" + str(j + 1) + ".bmp", crop_img)
    return (len(coord_x) + 1) * (len(coord_y) + 1)


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


def crop_images(root_dir):
    list_dirs = os.walk(root_dir + '/region_data')
    nums = 0
    for root, dirs, files in list_dirs:
        for f in files:
            region_bmp = os.path.join(root, f)
            if region_bmp.endswith('.bmp'):
                index = region_bmp.rfind('/')
                crop_dir = region_bmp[0: index].replace('region_data', 'crop_data')
                mk_dir(crop_dir)
                crop_bmp = region_bmp.replace('region_data', 'crop_data')[0:-4]
                num = crop_image(region_bmp, crop_bmp)
                nums += num
    return nums


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python bmp data dir'
        exit(1)
    data_dir = sys.argv[1]
    start = time.time()
    nums = crop_images(data_dir)
    end = time.time()
    print 'time: ' + str(end - start) + 's'
    print 'numbers: ' + str(nums)
    print 'fps: ' + str(nums / (end - start))
