import cv2 as cv
import numpy as np
import time

start = time.time()
overlap_w = 1277
overlap_h = 0
dir_path = '2/'

image_11 = cv.imread(dir_path + '11.bmp')
image_12 = cv.imread(dir_path + '12.bmp')
image_13 = cv.imread(dir_path + '13.bmp')
image_14 = cv.imread(dir_path + '14.bmp')
image_15 = cv.imread(dir_path + '15.bmp')

print image_11.shape
image_21 = cv.imread(dir_path + '21.bmp')
image_22 = cv.imread(dir_path + '22.bmp')
image_23 = cv.imread(dir_path + '23.bmp')
image_24 = cv.imread(dir_path + '24.bmp')
image_25 = cv.imread(dir_path + '25.bmp')

height = image_11.shape[0]
h = height - overlap_h
width = image_11.shape[1]
w = width - overlap_w
image_full_1 = np.zeros((height, width * 5 - overlap_w * 4, 3))
image_full_2 = np.zeros((height, width * 5 - overlap_w * 4, 3))
print image_full_1.shape
image_full_1[:, 0:w, :] = image_11[:, 0:w, :]
image_full_1[:, w:2 * w, :] = image_12[:, 0:w, :]
image_full_1[:, 2 * w:3 * w, :] = image_13[:, 0:w, :]
image_full_1[:, 3 * w:4 * w, :] = image_14[:, 0:w, :]
image_full_1[:, 4 * w:, :] = image_15[:, :, :]

image_full_2[:, 0:w, :] = image_21[:, 0:w, :]
image_full_2[:, w:2 * w, :] = image_22[:, 0:w, :]
image_full_2[:, 2 * w:3 * w, :] = image_23[:, 0:w, :]
image_full_2[:, 3 * w:4 * w, :] = image_24[:, 0:w, :]
image_full_2[:, 4 * w:, :] = image_25[:, :, :]

# image_full[0:h, 0:w, :] = image_11[0:h, 0:w, :]
# image_full[0:h, w:2 * w, :] = image_12[0:h, 0:w, :]
# image_full[0:h, 2 * w:3 * w, :] = image_13[0:h, 0:w, :]
# image_full[0:h, 3 * w:4 * w, :] = image_14[0:h, 0:w, :]
# image_full[0:h, 4 * w:, :] = image_15[0:h, :, :]

# image_full[h:, 0:w, :] = image_21[:, 0:w, :]
# image_full[h:, w:2 * w, :] = image_22[:, 0:w, :]
# image_full[h:, 2 * w:3 * w, :] = image_23[:, 0:w, :]
# image_full[h:, 3 * w:4 * w, :] = image_24[:, 0:w, :]
# image_full[h:, 4 * w:, :] = image_25[:, :, :]

cv.imwrite("full_1.bmp", image_full_1)
cv.imwrite("full_2.bmp", image_full_2)
end = time.time()
print 'time: ' + str(end - start) + 's'
