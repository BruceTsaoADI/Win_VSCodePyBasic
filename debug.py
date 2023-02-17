import matplotlib.pyplot as plt
import matplotlib.image as img
import os
import numpy as np
import cv2


width = 812
height = 1080
subpixel = 1
num = width * height * subpixel

filepath = r'/debug/test.png'
image = img.imread(filepath)
image = np.arange(0, 1, 1/num).reshape(width, height, subpixel)
# image = np.arange(0, 1, 1/num).reshape(width, height)

# image = image * 65535
# image = image.astype('uint8')

tmpw = []
for w in range(width):
    tmph = []
    for h in range(height):
        tmps = []
        for subp in range(subpixel):
            tmps.append(127)
        tmph.append(tmps)
    tmpw.append(tmph)

# tmpw = []
# for w in range(width):
#     tmph = []
#     for h in range(height):
#         tmps = []
#         tmph.append(255)
#     tmpw.append(tmph)


image = np.array(tmpw)
image = image.astype('uint8')

print('shape', image.shape)
print('dtype', image.dtype)
print(image[0][0])
plt.imshow(image)
plt.show()

# img = cv2.imread('test.png', 1)
# print(img.shape)
# print(img.dtype)
# print(img)

cv2.imshow('image', image)
cv2.waitKey(1000)
cv2.destroyAllWindows()