import numpy as np
import cv2


class FindCones:
    __colors_dic = {

        "red": {
            "lower_c": [np.array([0, 135, 135]), np.array([15, 255, 255])],
            "upper_c": [np.array([150, 135, 135]), np.array([180, 255, 255])]

        },
        "yellow": {
            "lower_c": [np.array([19, 167, 140]), np.array([119, 255, 255])] # [np.array([15, 112, 221]), np.array([45, 255, 255])]

        },
        "green": {
            "lower_c": [np.array([25-5, 42, 50]), np.array([95, 255, 255])] #45/75
        },
        "purple": {
            "lower_c": [np.array([120, 59, 152]), np.array([164, 255, 250])]
        }
    }
    
    __bgr_dic = {
        
        "red": [0, 0, 255],
        "green": [0, 255, 0],
        "blue": [255, 0, 0],
        "yellow": [0, 225, 238],
        "purple": [128, 0, 128]
        
    }
    
    def __init__(self, color="red"):
        self.color = color
        print(f"Finding Follwoing color:{self.color} and color: {self.__colors_dic[color]}")
        if color in self.__colors_dic:
            if self.color == "red":
                self.lowerc_array = self.__colors_dic[color]["lower_c"]
                self.upperc_array = self.__colors_dic[color]["upper_c"]
            else:
                self.lowerc_array = self.__colors_dic[color]["lower_c"]

        else:
            raise Exception("Color is not in the dictionary")

    def find_cone(self, img):
        '''
        Method to find cone in an image
        :param img: Numpy image Array
        :return: Tuple (resultsing image, Total Cones in the Image, Bounding boxes for the image.
        '''

        try:

            # converting color image to HSV. HSV helps to filter colors much better than RGB.
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            if self.color == "red":
                # filtering color based on the object it was initialized.
                imgLowThreshold = cv2.inRange(hsv, self.lowerc_array[0], self.lowerc_array[1])
                imgHighThreshold = cv2.inRange(hsv, self.upperc_array[0], self.upperc_array[1])
                # cv2.imshow("Orginal", img)

                # combining low and high threshold image to get only the color eg red in the picture.
                imgThresh = cv2.bitwise_or(imgLowThreshold, imgHighThreshold)
            else:
                imgThresh = cv2.inRange(hsv, self.lowerc_array[0], self.lowerc_array[1])

            # cv2.imshow("imgThresh", imgThresh)

            # applying erosion and dilation on the image using kernel 5. Always Kernel should be a odd number
            kernel = np.ones((5, 5))
            img_thresh_opened = cv2.morphologyEx(imgThresh, cv2.MORPH_OPEN, kernel)

            # cv2.imshow("img_threh_opened", img_thresh_opened)

            # blurring the image. You can see objects better when you blur the image in image processing.
            img_thresh_blurred = cv2.medianBlur(img_thresh_opened, 5)

            # cv2.imshow("img_Median Blur", img_thresh_blurred)

            # here we are detecting the edge of the objects we have filtered so far using above steps.
            img_edges = cv2.Canny(img_thresh_blurred, 80, 160)

            # cv2.imshow("Canny edges (img_edges)", img_edges)

            # Finding contour for the image based on the canny edges.
            contours, hierarchy = cv2.findContours(np.array(img_edges), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # this is just drawing the contours we identified above on to the image. So we can visually see.
            img_contours = np.zeros_like(img_edges)
            cv2.drawContours(img_contours, contours, -1, (255, 255, 255), 2)

            # cv2.imshow("Contours from edges (img_edges)", img_contours)

            # We are trying to find the approximate points/shape of the object in the image.
            approx_contours = []

            for c in contours:
                approx = cv2.approxPolyDP(c, 8.0, closed=True)
                approx_contours.append(approx)

            img_approx_contours = np.zeros_like(img_edges)
            cv2.drawContours(img_approx_contours, approx_contours, -1, (255, 255, 255), 1)

            # cv2.imshow("Approx Poly DP from edges (img_approx_contours)", img_approx_contours)

            # convex Hull smooth's the points of the cone. Canny edges will detect the edges of the object. For example
            # for the cone case, it will detect the base too in the canny edges. Convex Hull smoothing will remove those
            # bases as edges and just draws a smooth 3 point triangle to the cone.
            all_convex_hulls = []
            for ac in approx_contours:
                all_convex_hulls.append(cv2.convexHull(ac))

            img_all_convex_hulls = np.zeros_like(img_edges)
            cv2.drawContours(img_all_convex_hulls, all_convex_hulls, -1, (255, 255, 255), 2)

            # cv2.imshow("img_all_convex_hulls", img_approx_contours)

            # here are filtering only objects that are having 3 to 10 points (or shape or edges). So in our case of cone
            # any object that has at least 3 points to form an approx triangle for cone.
            convex_hulls_3to10 = []
            for ch in all_convex_hulls:
                if 3 <= len(ch) <= 10:
                    convex_hulls_3to10.append(cv2.convexHull(ch))

            img_convex_hulls_3to10 = np.zeros_like(img_edges)
            cv2.drawContours(img_convex_hulls_3to10, convex_hulls_3to10, -1, (255, 255, 255), 2)

            # cv2.imshow("img_convex_hulls_3to10", img_convex_hulls_3to10)

            # here are only picking triangle that are points upwards. SO if the cone is upside down, our code will not
            # detect that as the cone.
            cones = []
            cones_obj = dict()
            bounding_rects = []
            i = 0
            for ch in convex_hulls_3to10:
                if FindCones.__convex_hull_pointing_up(ch):
                    cones.append(ch)
                    rect = cv2.boundingRect(ch)
                    bounding_rects.append(rect)
                    cones_obj[f"cone-{i}"] = {"cone": ch}
                    i += 1
    
            img_cones = np.zeros_like(img_edges)
            cv2.drawContours(img_cones, cones, -1, (255, 255, 255), 2)
            # cv2.drawContours(img_cones, , -1, (1,255,1), 2)

            #cv2.imshow("img_cones", img_cones)

            img_res = img.copy()
            cv2.drawContours(img_res, cones, -1, (255, 255, 255), 2)

            for idx, rect in enumerate(bounding_rects):
                cv2.rectangle(img_res, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (1, 255, 1), 3)
                centX, centY = (rect[0]+rect[0]+rect[2])//2, (rect[1] + rect[1] + rect[3])//2
                cv2.circle(img_res, (centX, centY), 2, [0,255,0], -1)
                cone_index = f"cone-{idx}"
                c_obj = cones_obj[cone_index]
                c_obj["bouding_box_center"] = (centX, centY)
                cv2.putText(img_res, f"{self.color}-{cone_index}", (rect[0], rect[1]-4), cv2.FONT_HERSHEY_SIMPLEX, .5, self.__bgr_dic[self.color], 1, cv2.LINE_AA)
                cv2.putText(img_res, f"coord: {c_obj['bouding_box_center']}", (centX, centY), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,255, 255), 1, cv2.LINE_AA)

            # cv2.imshow("img_res", img_res)

            # print(f"Total Cones Found:{str(len(bounding_rects))}")
            
            

            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            total_cone = len(bounding_rects)
            if total_cone > 0:
                return True, img_res, total_cone, bounding_rects, cones_obj
            return False, img_res, 0, None, None

        except Exception as e:
            raise e

    @staticmethod
    def __convex_hull_pointing_up(ch):
        '''
        This method will identify objects that are points upwards. An convex Hull numpy array is passed to this object.
        :param ch: Is a numpy array
        :return: boolean. Returns True if the object is pointing upwards else False
        '''
        points_above_center, points_below_center = [], []

        x, y, w, h = cv2.boundingRect(ch)
        aspect_ratio = w / h

        # if the height is > width of the identified object in the image then return true
        if aspect_ratio < 0.8:

            # calculate the center of the object in the image.
            vertical_center = y + h / 2

            # Divide the points that are above center and below center
            for point in ch:
                if point[0][1] < vertical_center:
                    points_above_center.append(point)
                elif point[0][1] >= vertical_center:
                    points_below_center.append(point)

            # find the left extreme and right extreme point.
            # Separate the points below center to the left points and right points based on the extreme points
            left_x = points_below_center[0][0][0]
            right_x = points_below_center[0][0][0]
            for point in points_below_center:
                if point[0][0] < left_x:
                    left_x = point[0][0]
                if point[0][0] > right_x:
                    right_x = point[0][0]
            # if any of the points above the center are > right greatest point and < left point calculate above
            # (for points below the center) then return false as this is not a triangle like shape.
            for point in points_above_center:
                if (point[0][0] < left_x) or (point[0][0] > right_x):
                    return False
        else:
            return False

        return True


if __name__ == '__main__':
    c = FindCones(color="orange")
    print(c.find_cone(cv2.imread("../../data/Images/8.jpg")))
