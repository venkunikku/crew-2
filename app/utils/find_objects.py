import numpy as np
import cv2


class FindCones:
    __colors_dic = {

        "orange": {
            "lower_c": [np.array([0, 135, 135]), np.array([15, 255, 255])],
            "upper_c": [np.array([159, 135, 135]), np.array([179, 255, 255])]

        },
        "yellow" :{
            "lower_c": [np.array([0, 58, 213]), np.array([75, 194, 255])],
            "upper_c": [np.array([0, 61, 220]), np.array([75, 194, 255])]

        }
    }

    def __init__(self, color="orange"):
        if color in self.__colors_dic:
            self.lowerc_array = self.__colors_dic[color]["lower_c"]
            self.upperc_array = self.__colors_dic[color]["upper_c"]

        else:
            raise Exception("Color is not in the dictionary")

    def find_cone(self, img):

        try:

            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            imgLowThreshold = cv2.inRange(hsv, np.array([0, 135, 135]), np.array([15, 255, 255]))
            imgHighThreshold = cv2.inRange(hsv, np.array([159, 135, 135]), np.array([179, 255, 255]))

            # cv2.imshow("Orginal", img)

            # combining low and high threshold image
            imgThresh = cv2.bitwise_or(imgLowThreshold, imgHighThreshold)

            # cv2.imshow("imgThresh", imgThresh)

            kernel = np.ones((5, 5))
            img_thresh_opened = cv2.morphologyEx(imgThresh, cv2.MORPH_OPEN, kernel)

            # cv2.imshow("img_threh_opened", img_thresh_opened)

            img_thresh_blurred = cv2.medianBlur(img_thresh_opened, 5)

            # cv2.imshow("img_Median Blur", img_thresh_blurred)

            img_edges = cv2.Canny(img_thresh_blurred, 80, 160)

            # cv2.imshow("Canny edges (img_edges)", img_edges)

            # Finding contour
            contours, hierarchy = cv2.findContours(np.array(img_edges), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            img_contours = np.zeros_like(img_edges)
            cv2.drawContours(img_contours, contours, -1, (255, 255, 255), 2)

            # cv2.imshow("Contours from edges (img_edges)", img_contours)

            approx_contours = []

            for c in contours:
                approx = cv2.approxPolyDP(c, 8.0, closed=True)
                approx_contours.append(approx)

            img_approx_contours = np.zeros_like(img_edges)
            cv2.drawContours(img_approx_contours, approx_contours, -1, (255, 255, 255), 1)

            # cv2.imshow("Approx Poly DP from edges (img_approx_contours)", img_approx_contours)

            all_convex_hulls = []
            for ac in approx_contours:
                all_convex_hulls.append(cv2.convexHull(ac))

            img_all_convex_hulls = np.zeros_like(img_edges)
            cv2.drawContours(img_all_convex_hulls, all_convex_hulls, -1, (255, 255, 255), 2)

            # cv2.imshow("img_all_convex_hulls", img_approx_contours)

            convex_hulls_3to10 = []
            for ch in all_convex_hulls:
                if 3 <= len(ch) <= 10:
                    convex_hulls_3to10.append(cv2.convexHull(ch))

            img_convex_hulls_3to10 = np.zeros_like(img_edges)
            cv2.drawContours(img_convex_hulls_3to10, convex_hulls_3to10, -1, (255, 255, 255), 2)

            # cv2.imshow("img_convex_hulls_3to10", img_convex_hulls_3to10)

            cones = []
            bounding_rects = []
            for ch in convex_hulls_3to10:
                if FindCones.__convex_hull_pointing_up(ch):
                    cones.append(ch)
                    rect = cv2.boundingRect(ch)
                    bounding_rects.append(rect)

            img_cones = np.zeros_like(img_edges)
            cv2.drawContours(img_cones, cones, -1, (255, 255, 255), 2)
            # cv2.drawContours(img_cones, , -1, (1,255,1), 2)

            cv2.imshow("img_cones", img_cones)

            img_res = img.copy()
            cv2.drawContours(img_res, cones, -1, (255, 255, 255), 2)

            for rect in bounding_rects:
                cv2.rectangle(img_res, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (1, 255, 1), 3)

            # cv2.imshow("img_res", img_res)

            # print(f"Total Cones Found:{str(len(bounding_rects))}")

            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            total_cone = len(bounding_rects)
            if total_cone > 0:
                return True, img_res, total_cone, bounding_rects
            return False, img_res, 0, None

        except Exception as e:
            raise e

    @staticmethod
    def __convex_hull_pointing_up(ch):
        points_above_center, points_below_center = [], []

        x, y, w, h = cv2.boundingRect(ch)
        aspect_ratio = w / h

        if aspect_ratio < 0.8:

            vertical_center = y + h / 2

            for point in ch:
                if point[0][1] < vertical_center:
                    points_above_center.append(point)
                elif point[0][1] >= vertical_center:
                    points_below_center.append(point)

            left_x = points_below_center[0][0][0]
            right_x = points_below_center[0][0][0]
            for point in points_below_center:
                if point[0][0] < left_x:
                    left_x = point[0][0]
                if point[0][0] > right_x:
                    right_x = point[0][0]

            for point in points_above_center:
                if (point[0][0] < left_x) or (point[0][0] > right_x):
                    return False
        else:
            return False

        return True


if __name__ == '__main__':
    c = FindCones(color="orange")
    print(c.find_cone(cv2.imread("../../data/Images/8.jpg")))
