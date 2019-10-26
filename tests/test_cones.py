import cv2
from app.utils import find_objects


def check_cv2():
    print(cv2.__version__)



if __name__ == '__main__':
    check_cv2()
    img = cv2.imread("../data/Images/1.jpg")
    c = find_objects.FindCones()
    flag, img_ret, number_cone, rect = c.find_cone(img)
    cv2.imshow("Cones", img_ret)
    cv2.waitKey(0)
    cv2.destroyAllWindows()