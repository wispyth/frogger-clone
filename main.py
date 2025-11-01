import cv2
import numpy as np

print("OpenCV version:", cv2.__version__)
img = np.zeros((200, 300, 3), dtype=np.uint8)   # чёрная картинка
cv2.imshow("test", img)
cv2.waitKey(1000)   # показываем окно 1 секунду
cv2.destroyAllWindows()
