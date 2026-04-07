import base64
import cv2
import numpy as np

class PythonUtil:
  @staticmethod
  def bytes_to_base64(bytes_image, pixel_size=None):
    nparr = np.frombuffer(bytes_image, np.uint8)
    cv2_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if pixel_size:
      cv2_image = PythonUtil.image_resize(cv2_image, pixel_size)

    _, buffer = cv2.imencode('.jpg', cv2_image)
    base64_image = base64.b64encode(buffer).decode('utf-8')

    return base64_image

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