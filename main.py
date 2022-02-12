# make new image later
import numpy
from scipy.io import loadmat, savemat
import numpy as np
import matplotlib.pyplot as plt
from random import random
from PIL import Image

noisy_data = loadmat("noisy_richb.mat")['x']
# image = Image.open("38-383841_background-random-pic-hd.jpg")
# image = image.resize((192, 108))
# image = image.convert("L")
# image.show()
# image_array = np.asarray(image)
image_array = noisy_data
print(np.shape(noisy_data))

plt.imshow(image_array, cmap="gray")
plt.show()

def add_noise(image_array, chance, amplitude):
    image_shape = np.shape(image_array)
    output_image = np.zeros(image_shape)
    for row_index, row in enumerate(image_array):
        for col_index, pixel in enumerate(row):
            if random() <= chance:
                output_image[row_index, col_index] = image_array[row_index, col_index] + (2 * (random() - .5) * amplitude)
                if output_image[row_index, col_index] > 1: output_image[row_index, col_index] = 1
                if output_image[row_index, col_index] < 0: output_image[row_index, col_index] = 0
            else:
                output_image[row_index, col_index] = image_array[row_index, col_index]
    return output_image

def mean(image_array, radius, ignore):
    image_shape = np.shape(image_array)
    output_image = np.zeros(image_shape)
    for row_index, row in enumerate(image_array):
        for col_index, pixel in enumerate(row):
            if not (row_index < radius - 1 or row_index > image_shape[0] - radius or col_index < radius - 1 or col_index > image_shape[1] - radius):
                surrounding = image_array[row_index - radius + 1:row_index + radius, col_index - radius + 1:col_index + radius]
                surrounding = np.reshape(surrounding, (1, -1))[0]
                surrounding = np.sort(surrounding)
                surrounding = surrounding[ignore:-ignore]
                output_image[row_index, col_index] = np.mean(surrounding)
    return output_image


def median(image_array, radius):
    image_shape = np.shape(image_array)
    output_image = np.zeros(image_shape)
    for row_index, row in enumerate(image_array):
        for col_index, pixel in enumerate(row):
            if not (row_index < radius - 1 or row_index > image_shape[0] - radius or col_index < radius - 1 or col_index > image_shape[1] - radius):
                surrounding = image_array[row_index - radius + 1:row_index + radius, col_index - radius + 1:col_index + radius]
                output_image[row_index, col_index] = np.median(surrounding)
    return output_image

# image_array = add_noise(image_array, 1, 100)

plt.imshow(image_array, cmap="gray")
plt.show()

output_image = median(image_array, 3)

plt.imshow(output_image, cmap="gray")
plt.show()

output_dict = {}
output_dict['x'] = output_image

savemat("output.mat", output_dict)


# noisy_data = loadmat("noisy_richb.mat")
#
# x_array = np.zeros((1000, 1000, 3))
# x_array = np.zeros((1000, 1000, 3))
#
# for i in range(100):
#     x_array.append([0] * 100)
#
# for n in range(len(x_array)):
#     for m in range(len(x_array[0])):
#          x_array[n][m] = random()
#
#
# plt.imshow(noisy_data)
# plt.show()

# print(x_array)
