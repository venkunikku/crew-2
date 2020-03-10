import time
import cv2
import numpy as np


class InferImage():
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    def __init__(self, image_path=None, confidence=0.5):
        self.net = cv2.dnn.readNetFromCaffe("../model_weights/mobile_net_ssd/MobileNetSSD_deploy.prototxt",
                                            "../model_weights/mobile_net_ssd/MobileNetSSD_deploy.caffemodel")
        self.image_path = image_path
        self.image = cv2.imread(self.image_path)
        self.resized_image = None
        self.confidence = confidence

    def infer(self):
        self.resize_image()
        (h, w) = self.image.shape[:2]
        blob = cv2.dnn.blobFromImage(self.image, 0.007843, (300, 300), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()
        for idx, i in enumerate(np.arange(0, detections.shape[2])):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > self.confidence:
                # extract the index of the class label from the
                # `detections`, then compute the (x, y)-coordinates of
                # the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(self.CLASSES[idx],
                                             confidence * 100)
                print(f"Labels of the image : {label} ")
                cv2.rectangle(self.image, (startX, startY), (endX, endY),
                              self.COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(self.image, label, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.COLORS[idx], 2)

            # cv2.imwrite()

    def resize_image(self, width=400):
        (h, w) = self.image.shape[:2]
        r = width / float(w)
        dim = (width, int(h * r))
        self.resized_image = cv2.resize(self.image, dim, interpolation=cv2.INTER_AREA)
