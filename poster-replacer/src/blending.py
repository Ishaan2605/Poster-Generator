import cv2
import numpy as np

def reinhard_color_transfer(source_img, target_img):
    source = cv2.cvtColor(source_img, cv2.COLOR_BGR2LAB).astype(np.float32)
    target = cv2.cvtColor(target_img, cv2.COLOR_BGR2LAB).astype(np.float32)

    src_means, src_stds = cv2.meanStdDev(source)
    tar_means, tar_stds = cv2.meanStdDev(target)

    l, a, b = cv2.split(target)
    l = (l - tar_means[0][0]) * (src_stds[0][0] / tar_stds[0][0]) + src_means[0][0]
    a = (a - tar_means[1][0]) * (src_stds[1][0] / tar_stds[1][0]) + src_means[1][0]
    b = (b - tar_means[2][0]) * (src_stds[2][0] / tar_stds[2][0]) + src_means[2][0]

    result = cv2.merge([l, a, b])
    result = np.clip(result, 0, 255).astype(np.uint8)
    return cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
