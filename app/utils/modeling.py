import time
import cv2
import numpy as np
from threading import Thread
import logging

class InferImage:
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    def __init__(self, confidence=0.5, tpu=True):
        self.net = cv2.dnn.readNetFromCaffe("../model_weights/mobile_net_ssd/MobileNetSSD_deploy.prototxt",
                                            "../model_weights/mobile_net_ssd/MobileNetSSD_deploy.caffemodel")
        self.tpu = tpu
        if self.tpu:
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)

        self.resized_image = None
        self.confidence = confidence

    def run(self):
        pass

    def infer(self, image_path=None):
        image = cv2.imread(image_path)
        image = InferImage.resize_image(image)
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(image, 0.007843, (300, 300), 127.5)
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
                cv2.rectangle(image, (startX, startY), (endX, endY),
                              self.COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(image, label, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.COLORS[idx], 2)

            # cv2.imwrite()

    @staticmethod
    def resize_image(self, image, width=400):
        (h, w) = image.shape[:2]
        r = width / float(w)
        dim = (width, int(h * r))
        resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        return resized_image


def infer_image(q, conf):
    log = logging.getLogger('gpg.find_cone')
    net = cv2.dnn.readNetFromCaffe("./model_weights/mobile_net_ssd/MobileNetSSD_deploy.prototxt",
                                           "./model_weights/mobile_net_ssd/MobileNetSSD_deploy.caffemodel")
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)
    log.info("Inferring the image")
    while True:
        image_path = q.get()
        log.info("Path to image")
        print(f"Image we got for the image in the queue:", image_path)
        if image_path:
            print(f"yes we got an image")
            CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                       "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                       "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                       "sofa", "train", "tvmonitor"]
            COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
            
            image = cv2.imread(image_path)
            #print(image)
            width = 400
            (h, w) = image.shape[:2]
            r = width / float(w)
            dim = (width, int(h * r))
            
            print(f"Resizing done")
            resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
            blob = cv2.dnn.blobFromImage(image, 0.007843, (300, 300), 127.5)
            print("Puitting into setInput")
            net.setInput(blob)
            print("forwarding")
            detections = net.forward()
            for idx, i in enumerate(np.arange(0, detections.shape[2])):
                #print("Inside for loop")
                # extract the confidence (i.e., probability) associated with
                # the prediction
                confidence = detections[0, 0, i, 2]

                # filter out weak detections by ensuring the `confidence` is
                # greater than the minimum confidence
                if confidence > conf:
                    # extract the index of the class label from the
                    # `detections`, then compute the (x, y)-coordinates of
                    # the bounding box for the object
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    # draw the prediction on the frame
                    label = "{}: {:.2f}%".format(CLASSES[idx],
                                                 confidence * 100)
                    print(f"Labels of the image : {label} ")
                    cv2.rectangle(image, (startX, startY), (endX, endY),
                                  COLORS[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(image, label, (startX, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                    cv2.imwrite("{}_inference.png".format(idx), image)
                            
    
