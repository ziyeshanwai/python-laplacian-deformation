import cv2
import imgaug.augmenters as iaa
import os
from skimage import exposure
import numpy as np


def img_augs(img):
    pass


if __name__ == "__main__":
    image_path = '\\\\192.168.20.63\\ai\\face_data\\20190514\\image\\048170110027'
    img_aug_com = iaa.Affine(translate_percent={"x": (-0.0, 0.0), "y": (0, 0.3)},
                             rotate=(-5, 5), scale=(1.0, 1.3), mode='edge')
    i = 0
    img_file = os.path.join(image_path, "{}.jpg".format(i))
    img = cv2.imread(img_file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img.T
    img = cv2.flip(img, 1)  # 需要做一次对称
    img = cv2.resize(img, dsize=(258, 386))
    for i in range(0, 19):
        img_aug = img_aug_com.augment_image(img)
        # img_aug_com = iaa.Affine(translate_percent={"x": (-0.0, 0.0), "y": (0, 0.3)}, mode='edge')
        # img_aug = img_aug_com.augment_image(img)
        # img_aug = cv2.equalizeHist(img)
        img_aug = exposure.adjust_gamma(img_aug, gamma=np.random.randint(low=50, high=200, size=(1,))[0] / 100)
        # img_norm = img_norm[:, :, np.newaxis]
        cv2.namedWindow("before")
        cv2.imshow("before", img)
        cv2.namedWindow("after")
        cv2.imshow("after", img_aug)
        cv2.waitKey(0)