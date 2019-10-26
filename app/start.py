import cv2
import numpy as np
from app.utils import find_objects

cap = cv2.VideoCapture(0)

cone_obj = find_objects.FindCones()

while True:

    res, frame = cap.read()
    flag, frame_back, total_cones, boxes = cone_obj.find_cone(frame)

    cv2.imshow("Cone", frame_back)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
