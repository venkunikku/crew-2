import cv2
import numpy as np
from app.utils import find_objects, raspberry_utils, gopigo_controls
import datetime
import argparse
from easygopigo3 import EasyGoPiGo3
import math
import time
from picamera.array import PiRGBArray
from picamera import PiCamera


cap = None
easy = EasyGoPiGo3()


# def center_cone():
# 	b_box_rec = cones_data['cone-0']['bouding_box_center']
# 	print(f"Center of the rectangle-{b_box_rec}")
# 	print(f"Center of the screen-{center_of_the_screen}")
# 	cv2.line(frame_back, b_box_rec, center_of_the_screen, [0, 255, 0], 3)
# 	if center_of_the_screen[0] != b_box_rec[0]: # if the angle is not equal to 90 only do thistohis else we are getting divde by 0 error
# 		angle = int(math.atan((b_box_rec[1] - center_of_the_screen[1])/(b_box_rec[0] - center_of_the_screen[0])) * 180/math.pi )
# 	else:
# 		angle = 90
# 	print(F"Angle is{angle}")
# 	cv2.putText(frame_back, f"Angle: {angle}", (center_of_the_screen[0]-10, center_of_the_screen[1]-10), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,255, 255), 1, cv2.LINE_AA)
#
# 	#if b_box_rec[0] > center_of_the_screen[0]:
# 	#	print("Percentages", b_box_rec[0]/center_of_the_screen[0], center_of_the_screen[0]/b_box_rec[0])
# 	#	perc = round(center_of_the_screen[0]/b_box_rec[0], 2)
# 	#	#easy.right()
# 	#	easy.steer(perc, 0)
# 	#	#easy.stop()
# 	#	print("yes greated")
# 	#if angle >0:
# 		#easy.turn_degrees(angle/2)
# 		#import time
# 		#time.sleep(10)
# 		#break

def move_around_to_find_cone(cone_obj, raw_capture, obj, degress_area_to_scan=50, degress_to_move=15,
                             loops_to_check=100):
    raw_capture.truncate(0)

    if degress_to_move > degress_area_to_scan:
        raise Exception(
            f"degress_to_move:{degress_to_move} should be lesser than degress_area_to_scan:{degress_area_to_scan}")

    turn_deg_liste = [0, 15, -30, 45, -90]

    for d in turn_deg_liste:
        easy.turn_degrees(d)
        time.sleep(1)
        i = 0
        print(f"Chekcing for Degress:{d}")

        for fram in obj:
            i += 1
            frame = fram.array
            flag, frame_back, total_cones, boxes, cones_data = cone_obj.find_cone(frame)
            if total_cones > 0:
                print("Found cone on left side")
                # return flag, frame_back, total_cones, boxes, cones_data
                return True
            if i == loops_to_check:
                raw_capture.truncate(0)
                break
            raw_capture.truncate(0)

    return False


def move_to_center_of_screen(height_range=(280, 360), cone_boudning_box=None):
    if cone_boudning_box[0] > height_range[1]:
        # move right
        print(F"Moving right")
        easy.steer(1, 0)
        time.sleep(1)
        easy.stop()

    if cone_boudning_box[0] < height_range[1]:
        # move left
        print(F"Moving left")
        easy.steer(0, 1)
        time.sleep(1)
        easy.stop()


def move_close_to_the_cone(cone_bottom_mid_points_y, boundary_range=None, drive_inches=0.5):
    if boundary_range:
        if boundary_range[0] > cone_bottom_mid_points_y:
            easy.drive_inches(drive_inches)
        else:
            easy.drive_inches(-drive_inches)


def get_center_boundaries(frame):
    he, wi, ch = frame.shape
    center_of_the_screen = (wi // 2, he // 2)
    left_top, left_bottom = (wi - center_of_the_screen[0] - 40, 0), (wi - center_of_the_screen[0] - 40, he)
    rigth_top, right_bottom = (wi - center_of_the_screen[0] + 40, 0), (wi - center_of_the_screen[0] + 40, he)
    return left_top[0], rigth_top[0]


def center_boundaries(frm):
    frame = frm.copy()
    he, wi, ch = frame.shape
    center_of_the_screen = (wi // 2, he // 2)
    cv2.circle(frame, center_of_the_screen, 5, [255, 0, 0], -1)
    cv2.line(frame, center_of_the_screen, (center_of_the_screen[0] + 30, center_of_the_screen[1]), [0, 255, 0], 3)

    left_top, left_bottom = (wi - center_of_the_screen[0] - 40, 0), (wi - center_of_the_screen[0] - 40, he)
    rigth_top, right_bottom = (wi - center_of_the_screen[0] + 40, 0), (wi - center_of_the_screen[0] + 40, he)

    # print(F"Left: {left_top},{left_bottom} and Right: {rigth_top}, {right_bottom}")

    cv2.line(frame, left_top, left_bottom, [232, 206, 190], 1)
    cv2.line(frame, rigth_top, right_bottom, [232, 206, 190], 1)
    return frame


# def rest_to_original_position(no_of_turns, degress_to_move):
#     print(f"To set to original position. Turn: {no_of_turns} and Degress to move: {degress_to_move}")
#     easy.turn_degrees((no_of_turns) * degress_to_move)
#     easy.stop()


# def records_for_proofs(filename='output_with_cones.avi', w=640, h=480):
#     fourcc = cv2.VideoWriter_fourcc(*"XVID")
#     out = cv2.VideoWriter(filename, fourcc, 20.0, (w, h))  # 20 frams
#     return out


def midpoint(ptA, ptB):
    return (ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5


def euclidean_distance(pt1, pt2):
    p1 = (pt1[0] - pt2[0]) ** 2
    p2 = (pt1[1] - pt2[1]) ** 2
    return math.sqrt(p1 + p2)


def gogo():
    # global is_cone_centered, forwarded, iscircle_done, temperature, frame_back, cones_data, center_of_the_screen, upper_left, upper_right, lower_left, lower_right, cone_boudning_box, height_range, rect_bottom_mind_point, cone_bottom_mid_points_y, hieght_range_forward, found_required_cone, i, b_box_rec, angle, ref, distance_to_center
    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--record", required=False, help="Path to the image")
    ap.add_argument("-flp", "--flip_imgae", required=False, help="Path to the image")
    args = vars(ap.parse_args())
    # cap = cv2.VideoCapture(0)
    record = args["record"]
    isflip = args["flip_imgae"]

    camera = PiCamera()
    camera.resolution = (640, 480)
    # camera.vflip = True
    raw_capture = PiRGBArray(camera, size=(640, 480))
    time.sleep(1)
    cone_color = "yellow"
    cone_obj = find_objects.FindCones(color=cone_color)
    aline_cone_to_the_center = False
    found_required_cone = False
    is_cone_centered = False
    forwarded = False
    iscircle_done = False
    frame_obj = camera.capture_continuous(raw_capture, format="bgr", use_video_port=True)
    for frm in frame_obj:
        temperature = raspberry_utils.processor_temperature()
        frame = frm.array
        # print(image.shape, type(image), image)

        flag, frame_back, total_cones, boxes, cones_data = cone_obj.find_cone(frame)

        if not found_required_cone:
            # finding Cone
            found_required_cone = move_around_to_find_cone(cone_obj, raw_capture, frame_obj)
            raw_capture.truncate(0)
            continue

        frame_back = center_boundaries(frame_back)

        he, wi, ch = frame_back.shape
        center_of_the_screen = (wi // 2, he // 2)
        cv2.circle(frame_back, center_of_the_screen, 5, [255, 0, 0], -1)
        cv2.line(frame_back, center_of_the_screen, (center_of_the_screen[0] + 30, center_of_the_screen[1]), [0, 255, 0],
                 3)

        # center boundaries
        left_top, left_bottom = (wi - center_of_the_screen[0] - 20, 0), (wi - center_of_the_screen[0] - 20, he)
        rigth_top, right_bottom = (wi - center_of_the_screen[0] + 20, 0), (wi - center_of_the_screen[0] + 20, he)

        # print(F"Left: {left_top},{left_bottom} and Right: {rigth_top}, {right_bottom}")

        cv2.line(frame_back, left_top, left_bottom, [232, 206, 190], 1)
        cv2.line(frame_back, rigth_top, right_bottom, [232, 206, 190], 1)

        cv2.line(frame_back, rigth_top, right_bottom, [232, 206, 190], 1)

        # Center vertical line
        cv2.line(frame_back, (center_of_the_screen[0], 0), (center_of_the_screen[0], wi), [0, 255, 0], 1)

        # bottom boundaries
        upper_left, upper_right = (0, he - 100), (wi, he - 100)
        lower_left, lower_right = (0, he - 50), (wi, he - 50)
        cv2.line(frame_back, upper_left, upper_right, [200, 90, 60], 1)
        cv2.line(frame_back, lower_left, lower_right, [200, 90, 60], 1)

        cv2.putText(frame_back, f"Upper: {upper_left},{upper_right}", upper_left, cv2.FONT_HERSHEY_SIMPLEX, .5,
                    (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame_back, f"Lower: {lower_left},{lower_right}", lower_left, cv2.FONT_HERSHEY_SIMPLEX, .5,
                    (0, 255, 255), 1, cv2.LINE_AA)

        cv2.putText(frame_back, f"Temp:{temperature}", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 255), 1,
                    cv2.LINE_AA)

        if found_required_cone:

            if total_cones > 0:
                # dt = datetime.datetime.now()
                cone_boudning_box = cones_data['cone-0']['bouding_box_center']

                if not is_cone_centered:
                    height_range = (left_top[0], rigth_top[0])
                    print(
                        f"Cone no centered moving for height rnage:{height_range} and cone bouding box:{cone_boudning_box}")

                    is_cone_centered = center_cone_to_screen_and_gopio(cone_boudning_box, height_range)
                x, y, w, h = boxes[0]
                x1, y1, x4, y4 = (x, y, x + w, y + h)
                tl = (x1, y1)
                tr = (x4, y1)
                br = (x4, y4)
                bl = (x1, y4)
                # (tl, tr, br, bl) = boxes[0]
                (tlblX, tlblY) = midpoint(tl, bl)
                (trbrX, trbrY) = midpoint(tr, br)
                rect_bottom_mind_point = midpoint(bl, br)

                cv2.putText(frame_back, f"bottom: {rect_bottom_mind_point}",
                            (int(rect_bottom_mind_point[0]), int(rect_bottom_mind_point[1])), cv2.FONT_HERSHEY_SIMPLEX,
                            .5, (0, 255, 255), 1, cv2.LINE_AA)

                if is_cone_centered:
                    cone_bottom_mid_points_y = rect_bottom_mind_point[1]
                    hieght_range_forward = (upper_left[1] + 20, lower_left[1] + 20)
                    if not forwarded:
                        if not hieght_range_forward[0] <= cone_bottom_mid_points_y <= hieght_range_forward[1]:
                            print(f"Foward Range: {hieght_range_forward}, Cone Center: {cone_bottom_mid_points_y}")
                            move_close_to_the_cone(cone_bottom_mid_points_y, hieght_range_forward, )
                        else:
                            forwarded = True
                            is_cone_centered = False
                print(
                    f"Flags so far forwarded:{forwarded} and the circle:{iscircle_done} and is cone centerd:{is_cone_centered}")
                if forwarded and not iscircle_done:
                    # easy.reset_all()
                    # easy.turn_degrees(30)
                    easy.turn_degrees(-90)
                    easy.orbit(360, 75)
                    easy.turn_degrees(90)
                    easy.turn_degrees(180)
                    iscircle_done = True

        cv2.imshow("PI", frame_back)
        key = cv2.waitKey(1) & 0xFF

        raw_capture.truncate(0)

        if key == ord("q"):
            break


def center_cone_to_screen_and_gopio(cone_boudning_box, height_range):
    if not height_range[0] <= cone_boudning_box[0] <= height_range[1]:
        print("Centring Cone")
        move_to_center_of_screen(height_range=height_range,
                                 cone_boudning_box=cone_boudning_box)
        return False
    else:
        return True


if __name__ == '__main__':
    gogo()
