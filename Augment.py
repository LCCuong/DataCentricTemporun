import os
import cv2
import numpy as np
import random
from time import time

random.seed(time())

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def add_noise(img, min_rec=30, max_rec=50):
    img_new = img.copy()
    num_rec = random.randint(min_rec, max_rec)
    for i in range(num_rec):
        x, y = random.randint(0, 28), random.randint(0, 28)
        color = random_color()
        cv2.rectangle(img_new, (x, y), (x, y), color, -1)
    return img_new


def random_blur(img):
    kernel = (random.randrange(1, 4, 2), random.randrange(1, 4, 2))

    return cv2.blur(img, kernel)


def random_rotate(img, min_angle=-30, max_angle=30):
    angle = random.randint(min_angle, max_angle)
    height, width = img.shape[:2]
    center = (width / 2, height / 2)
    rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=angle, scale=1)
    rotated_image = cv2.warpAffine(src=img, M=rotate_matrix, dsize=(width, height))
    return rotated_image


def random_transparent(img):
    bg = np.full((28, 28, 3), random_color(), np.uint8)
    res = cv2.addWeighted(img, 0.4, bg, 0.6, 0)
    return res


def aug_one_img(img, num=0):
    rate = {'add_noise': 0, 'random_blur': 0, 'random_rotate': 0, 'random_transparent': 100}

    img_aug = img.copy()

    aug_rate = random.randint(0, 100)
    if aug_rate < rate['add_noise']:
        img_aug = add_noise(img_aug)

    aug_rate = random.randint(0, 100)
    if aug_rate < rate['random_blur']:
        img_aug = random_blur(img_aug)

    aug_rate = random.randint(0, 100)
    if aug_rate < rate['random_rotate']:
        if num == 7:
            img_aug = random_rotate(img_aug, -5, 5)
        else:
            img_aug = random_rotate(img_aug)

    aug_rate = random.randint(0, 100)
    if aug_rate < rate['random_transparent']:
        img_aug = random_transparent(img_aug)

    return img_aug


def aug_process(source, file, destination, num):
    img = cv2.imread(source + '/' + file)
    num_of_aug = 1

    for i in range(num_of_aug):
        img_aug = aug_one_img(img, num)
        cv2.imwrite(destination + '/' + file[:-4] + str(time()) + '_' + str(i) + file[-4:], img_aug)


source = '28x28/data_ngoai'
destination = 'AUG/data_ngoai/2'

for i in range(10):
    try:
        os.mkdir(destination + '/' + str(i))
    except:
        pass

for i in range(10):
    files = os.listdir(source + '/' + str(i))
    for file in files:
        aug_process(source + '/' + str(i), file, destination + '/' + str(i), i)

