from tqdm import tqdm
import os
import random
import shutil


def _copyfileobj_patched(fsrc, fdst, length=64*1024*1024):
    """Patches shutil method to hugely improve copy speed"""
    while 1:
        buf = fsrc.read(length)
        if not buf:
            break
        fdst.write(buf)


shutil.copyfileobj = _copyfileobj_patched


# paths = ['AUG/mnist/train', 'AUG/mnist/val', 'hand_data', 'new_hand_data']
paths = ['AUG/data_ngoai/1', '28x28/data_ngoai', '28x28/new_data', 'new_hand_data']
destination_path = 'submission/10_8_4'
move_path = 'best_data/8_6'
imgs = []

random.seed(0)

# print('Moving folder...')
# for folder in os.listdir(move_path):
#     shutil.copytree(move_path + '/' + folder, destination_path + '/' + folder)

try:
     os.mkdir(destination_path + '/val')
except:
    pass

try:
     os.mkdir(destination_path + '/train')
except:
    pass

class_count = [0 for i in range(10)]

for path in tqdm(paths):
    for i in tqdm(range(10)):
        files = os.listdir(path + '/' + str(i))
        class_count[i] += len(files)
        for file in tqdm(files):
            imgs.append((file, str(i), path))

for i in range(10):
    print(str(i) + ':', class_count[i])

print('Done init.')

val_rate = 0.5
val_size = int(len(imgs) * val_rate)

print('Processing val...')
for i in range(10):
    try:
        os.mkdir(destination_path + '/val/' + str(i))
    except:
        pass

for i in tqdm(range(val_size)):
    x = random.choice(imgs)
    imgs.remove(x)
    shutil.copy(x[2] + '/' + x[1] + '/' + x[0], destination_path + '/val/' + x[1] + '/' + x[0])

print('Val Class: ')
for i in range(10):
    print(str(i) + ':', len(os.listdir(destination_path + '/val/' + str(i))))

print('Processing train...')
for i in range(10):
    try:
        os.mkdir(destination_path + '/train/' + str(i))
    except:
        pass

for x in tqdm(imgs):
    shutil.copy(x[2] + '/' + x[1] + '/' + x[0], destination_path + '/train/' + x[1] + '/' + x[0])

print('Train Class: ')
for i in range(10):
    print(str(i) + ':', len(os.listdir(destination_path + '/train/' + str(i))))

print('Done.')