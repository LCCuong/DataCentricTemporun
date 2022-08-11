import cv2
import numpy as np
import random
from time import time

random.seed(time())


def random_color(background=False):
    min_val = 0
    max_val = 256
    if background:
        min_val = 0
        max_val = 256
    return (random.randint(min_val, max_val), random.randint(min_val, max_val), random.randint(min_val, max_val))


def add_noise(img, min_rec=50, max_rec=100):
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


def aug_one_img(img):
    rate = {'add_noise': 10, 'random_blur': 30, 'random_rotate': 50}

    img_aug = img.copy()

    aug_rate = random.randint(0, 100)
    if aug_rate < rate['add_noise']:
        img_aug = add_noise(img_aug)

    aug_rate = random.randint(0, 100)
    if aug_rate < rate['random_blur']:
        img_aug = random_blur(img_aug)

    aug_rate = random.randint(0, 100)
    if aug_rate < rate['random_rotate']:
        img_aug = random_rotate(img_aug)

    return img_aug


def draw_circle(event, x, y, flags, param):
    if flags == cv2.EVENT_FLAG_LBUTTON and event == cv2.EVENT_MOUSEMOVE:
        for i, img in enumerate(imgs):
            cv2.circle(img, (x, y), 25, brush_colors[i], -1)
            # cv2.circle(img, (x, y), 20, brush_colors[i], -1)
            # cv2.circle(img, (x, y + 80), 20, brush_colors[i], -1)
    elif flags == cv2.EVENT_FLAG_RBUTTON and event == cv2.EVENT_MOUSEMOVE:
        for i, img in enumerate(imgs):
            cv2.circle(img, (x, y), 20, brush_colors[i], -1)
            cv2.circle(img, (x + 80, y), 20, brush_colors[i], -1)


def create_images():
    for i, img in enumerate(imgs):
        img_new = cv2.resize(img, (28, 28))
        img_new = aug_one_img(img_new)

        cv2.imwrite('new_hand_data/9/' + str(time()) + '_' + str(i) + '.jpg', img_new)


def dist(color1, color2, threshold=50):
    for i in range(3):
        if abs(color1[i] - color2[i]) < threshold:
            return False
    return True


def reset():
    for i in range(number_of_images):
        brush_colors[i] = random_color()
        background_colors[i] = random_color(True)

        while not dist(brush_colors[i], background_colors[i]):
            brush_colors[i] = random_color()
            background_colors[i] = random_color(True)

        imgs[i] = np.full((28 * image_size, 28 * image_size, 3), background_colors[i], np.uint8)


number_of_images = 100
image_size = 20
imgs = []
brush_colors = []
background_colors = []

for i in range(number_of_images):
    brush_color = random_color()
    background_color = random_color(True)

    while not dist(brush_color, background_color):
        brush_color = random_color()
        background_color = random_color(True)

    brush_colors.append(brush_color)
    background_colors.append(background_color)

    imgs.append(np.full((28 * image_size, 28 * image_size, 3), background_color, np.uint8))


cv2.namedWindow('Image')
cv2.setMouseCallback('Image', draw_circle)

id = 0
while True:
    cv2.imshow('Image', imgs[0])
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
    if k == ord('s'):
        create_images()
        print(id)
        id += 1
        reset()