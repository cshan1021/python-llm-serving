import cv2
import numpy as np
import math

class PythonUtil:
  @staticmethod
  def image_resize(cv2_image, pixel_size):
    h, w = cv2_image.shape[:2]

    if w >= h:
      target_w = pixel_size
      target_h = int(h * (pixel_size / w))
    else:
      target_h = pixel_size
      target_w = int(w * (pixel_size / h))

    return cv2.resize(cv2_image, (target_w, target_h), interpolation=cv2.INTER_AREA)

  @staticmethod
  def save_image(img, save_path):
      # 이미지를 지정된 경로에 저장합니다.
      cv2.imwrite(save_path, img)