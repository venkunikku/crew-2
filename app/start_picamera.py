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
import argparse
from fanshim import FanShim


fanshim = FanShim()
fanshim.set_fan(True)

utils = raspberry_utils.Utils()

cap = None
easy = EasyGoPiGo3()
easy.set_left_eye_color((10,20,30))

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

cone_color = {
        
        "red": (255, 0,0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (238, 225, 0)
        
    }

def move_around_to_find_cone(cone_obj, raw_capture, obj, degress_area_to_scan=50, degress_to_move=15,
                             loops_to_check=100):
    raw_capture.truncate(0)

    if degress_to_move > degress_area_to_scan:
        raise Exception(
            f"degress_to_move:{degress_to_move} should be lesser than degress_area_to_scan:{degress_area_to_scan}")

    turn_deg_liste = [0, 20, -40, 60, -80, 100, -120, 140, -160]

    for d in turn_deg_liste:
        easy.turn_degrees(d)
        time.sleep(1)
        i = 0
        print(f"Chekcing for Degress:{d}")
        easy.set_right_eye_color(cone_color[cone_obj.color])
        easy.set_left_eye_color(cone_color[cone_obj.color])
        for fram in obj:
            easy.open_eyes()
            i += 1
            frame = fram.array
            flag, frame_back, total_cones, boxes, cones_data = cone_obj.find_cone(frame)
            if total_cones > 0:
                print("Found cone on left side")
                # return flag, frame_back, total_cones, boxes, cones_data
                easy.close_eyes()
                return True
            if i == loops_to_check:
                raw_capture.truncate(0)
                easy.close_eyes()
                break
            raw_capture.truncate(0)
            easy.close_eyes()

    return False


def move_to_center_of_screen(height_range=(280, 360), cone_boudning_box=None):
    if cone_boudning_box[0] > height_range[1]:
        # move right
        print(F"Moving right")
        easy.open_left_eye()
        easy.steer(1, 0)
        time.sleep(1)
        easy.stop()
        easy.close_left_eye()
        

    if cone_boudning_box[0] < height_range[1]:
        # move left
        print(F"Moving left")
        easy.open_right_eye()
        
        easy.steer(0, 1)
        time.sleep(1)
        easy.close_right_eye()
        easy.stop()


def drive_forward_towards_cone(cone_bottom_mid_points_y, boundary_range=None, drive_inches=0.5):
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


def gogo(camera, raw_capture, cone_color="yellow", home_cone_color="orange"):
    fanshim.set_light(255,0,0)
    args = processe_args()
    # global is_cone_centered, forwarded, iscircle_done, temperature, frame_back, cones_data, center_of_the_screen, upper_left, upper_right, lower_left, lower_right, cone_boudning_box, height_range, rect_bottom_mind_point, cone_bottom_mid_points_y, hieght_range_forward, found_required_cone, i, b_box_rec, angle, ref, distance_to_center
    print(f"All args: {args}")    
    # cap = cv2.VideoCapture(0)
    record = args["record"]
    isflip = args["flip_imgae"]

    # cone_color = "yellow"
    cone_obj = find_objects.FindCones(color=cone_color)

    found_required_cone = False
    is_cone_centered = False
    forwarded = False
    iscircle_done = False
    frame_obj = camera.capture_continuous(raw_capture, format="bgr", use_video_port=True)
    for frm in frame_obj:
        temperature = utils.get_temperature() #raspberry_utils.processor_temperature()
        frame = frm.array
        # print(image.shape, type(image), image)
        cv2.putText(frame, f"Temp:{temperature}, {utils.get_gopigo_details()}", (50, 30), cv2.FONT_HERSHEY_TRIPLEX, .5, (255,51, 85), 2, cv2.LINE_AA)

        flag, frame_back, total_cones, boxes, cones_data = cone_obj.find_cone(frame)

        if not found_required_cone:
            # finding Cone
            print("Finding cone")
            found_required_cone = move_around_to_find_cone(cone_obj, raw_capture, frame_obj)
            raw_capture.truncate(0)
            continue

        frame_back = center_boundaries(frame_back)

        center_of_screen_coord, horiztl_line_lower_left_coord, horiztl_line_lower_right_coord, horiztl_line_upper_left_coord, horiztl_line_upper_right_coord, \
        left_bottom_bound_line_coord, left_top_bound_line_coord, right_bottom_bound_line_coord, rigth_top_bound_line_coord, width = screen_coordinates(
            frame_back)

        cv2.circle(frame_back, center_of_screen_coord, 5, [255, 0, 0], -1)
        cv2.line(frame_back, center_of_screen_coord, (center_of_screen_coord[0] + 30, center_of_screen_coord[1]),
                 [0, 255, 0],
                 3)

        # print(F"Left: {left_top},{left_bottom} and Right: {rigth_top}, {right_bottom}")

        cv2.line(frame_back, left_top_bound_line_coord, left_bottom_bound_line_coord, [232, 206, 190], 1)
        cv2.line(frame_back, rigth_top_bound_line_coord, right_bottom_bound_line_coord, [232, 206, 190], 1)

        cv2.line(frame_back, rigth_top_bound_line_coord, right_bottom_bound_line_coord, [232, 206, 190], 1)

        # Center vertical line
        cv2.line(frame_back, (center_of_screen_coord[0], 0), (center_of_screen_coord[0], width), [0, 255, 0], 1)

        cv2.line(frame_back, horiztl_line_upper_left_coord, horiztl_line_upper_right_coord, [200, 90, 60], 1)
        cv2.line(frame_back, horiztl_line_lower_left_coord, horiztl_line_lower_right_coord, [200, 90, 60], 1)

        cv2.putText(frame_back, f"Upper: {horiztl_line_upper_left_coord},{horiztl_line_upper_right_coord}",
                    horiztl_line_upper_left_coord, cv2.FONT_HERSHEY_SIMPLEX, .5,
                    (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame_back, f"Lower: {horiztl_line_lower_left_coord},{horiztl_line_lower_right_coord}",
                    horiztl_line_lower_left_coord, cv2.FONT_HERSHEY_SIMPLEX, .5,
                    (0, 255, 255), 1, cv2.LINE_AA)

        cv2.putText(frame_back, f"Temp:{temperature}", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 255), 1,
                    cv2.LINE_AA)

        if found_required_cone:

            if total_cones > 0:
                # dt = datetime.datetime.now()
                cone_boudning_box = cones_data['cone-0']['bouding_box_center']

                if not is_cone_centered:
                    center_boundary_left_right_width = (left_top_bound_line_coord[0], rigth_top_bound_line_coord[0])
                    print(
                        f"Cone no centered moving for height rnage:{center_boundary_left_right_width} and cone bouding box:{cone_boudning_box}")

                    is_cone_centered = center_cone_to_screen_and_gopio(cone_boudning_box,
                                                                       center_boundary_left_right_width)
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
                    cone_lower_rec_boundary_mid_point_height = rect_bottom_mind_point[1]
                    bottom_boundary_upper_lower_height = (
                        horiztl_line_upper_left_coord[1] + 20, horiztl_line_lower_left_coord[1] + 20)
                    if not forwarded:
                        forwarded = get_close_to_the_cone(cone_lower_rec_boundary_mid_point_height,
                                                          bottom_boundary_upper_lower_height)
                        # Center the cone while you drive forward
                        center_cone_to_screen_and_gopio(cone_boudning_box, center_boundary_left_right_width)
                print(
                    f"Flags so far forwarded:{forwarded} and the circle:{iscircle_done} and is cone centerd:{is_cone_centered}")
                if forwarded and not iscircle_done:
                    # easy.reset_all()
                    # easy.turn_degrees(30)
                    easy.turn_degrees(-90)
                    if args["is_carpet"] == "True":
                        easy.orbit(480, 60)
                    else:
                        easy.orbit(360, 60)
                    easy.turn_degrees(90)
                    easy.turn_degrees(220)
                    iscircle_done = True


        if iscircle_done:
			#print(f"Home Cone color: {home_cone_color}")
			#print(f"Home Cone color: {home_cone_color}"
            go_home(raw_capture, frame_obj, cone_color=home_cone_color)
            raw_capture.truncate(0)
            break

        cv2.imshow("PI", frame_back)
        key = cv2.waitKey(1) & 0xFF

        raw_capture.truncate(0)

        if key == ord("q"):
            break
    #fanshim.set_light(0,0,0)

def go_home(raw_capture, frame_obj, cone_color="red"):
    print(f"Home cone color: {cone_color}")
    cone_obj = find_objects.FindCones(color=cone_color)
    raw_capture.truncate(0)
    found_required_cone = False
    is_cone_centered = False
    forwarded= False
    for frm in frame_obj:
        frame = frm.array

        flag, frame_back, total_cones, boxes, cones_data = cone_obj.find_cone(frame)

        center_of_screen_coord, horiztl_line_lower_left_coord, horiztl_line_lower_right_coord, horiztl_line_upper_left_coord, horiztl_line_upper_right_coord, \
        left_bottom_bound_line_coord, left_top_bound_line_coord, right_bottom_bound_line_coord, rigth_top_bound_line_coord, width = screen_coordinates(
            frame_back)
        if not found_required_cone:
            # finding Cone
            found_required_cone = move_around_to_find_cone(cone_obj, raw_capture, frame_obj)
            raw_capture.truncate(0)
            continue

        if found_required_cone:
            if total_cones > 0:
                cone_boudning_box = cones_data['cone-0']['bouding_box_center']
                if not is_cone_centered:
                    center_boundary_left_right_width = (left_top_bound_line_coord[0], rigth_top_bound_line_coord[0])
                    print(
                        f"Cone no centered moving for height rnage:{center_boundary_left_right_width} and cone bouding box:{cone_boudning_box}")

                    is_cone_centered = center_cone_to_screen_and_gopio(cone_boudning_box,
                                                                       center_boundary_left_right_width)

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

                if is_cone_centered:
                    cone_lower_rec_boundary_mid_point_height = rect_bottom_mind_point[1]
                    bottom_boundary_upper_lower_height = (
                        horiztl_line_upper_left_coord[1] + 20, horiztl_line_lower_left_coord[1] + 20)
                    if not forwarded:
                        forwarded = get_close_to_the_cone(cone_lower_rec_boundary_mid_point_height,
                                                          bottom_boundary_upper_lower_height)
                        # Center the cone while you drive forward
                        center_cone_to_screen_and_gopio(cone_boudning_box, center_boundary_left_right_width)
                if forwarded:
                    easy.drive_inches(15)
                    easy.turn_degrees(210)
                    break
		
        cv2.imshow("PI", frame_back)
        key = cv2.waitKey(1) & 0xFF

        raw_capture.truncate(0)

        if key == ord("q"):
            break
    fanshim.set_light(0,0,0)
    #fanshim.set_fan(False)

def screen_coordinates(frame_back):
    height, width, ch = frame_back.shape
    center_of_screen_coord = (width // 2, height // 2)
    # center boundaries
    left_top_bound_line_coord, left_bottom_bound_line_coord = (width - center_of_screen_coord[0] - 20, 0), (
        width - center_of_screen_coord[0] - 20, height)
    rigth_top_bound_line_coord, right_bottom_bound_line_coord = (width - center_of_screen_coord[0] + 20, 0), (
        width - center_of_screen_coord[0] + 20, height)
    # bottom boundaries
    horiztl_line_upper_left_coord, horiztl_line_upper_right_coord = (0, height - 100), (width, height - 100)
    horiztl_line_lower_left_coord, horiztl_line_lower_right_coord = (0, height - 50), (width, height - 50)
    return center_of_screen_coord, horiztl_line_lower_left_coord, horiztl_line_lower_right_coord, horiztl_line_upper_left_coord, horiztl_line_upper_right_coord, left_bottom_bound_line_coord, left_top_bound_line_coord, right_bottom_bound_line_coord, rigth_top_bound_line_coord, width


def get_close_to_the_cone(cone_bottom_mid_points_y, height_range_forward):
    if not height_range_forward[0] <= cone_bottom_mid_points_y <= height_range_forward[1]:
        # print(f"Foward Range: {hieght_range_forward}, Cone Center: {cone_bottom_mid_points_y}")
        drive_forward_towards_cone(cone_bottom_mid_points_y, height_range_forward, drive_inches=1)
        return False
    else:
        return True


def center_cone_to_screen_and_gopio(cone_boudning_box, height_range):
    if not height_range[0] <= cone_boudning_box[0] <= height_range[1]:
        print("Centring Cone")
        move_to_center_of_screen(height_range=height_range,
                                 cone_boudning_box=cone_boudning_box)
        return False
    else:
        return True

def processe_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-carpet", "--is_carpet", required=False, help="Is the Surface carpet")
    ap.add_argument("-r", "--record", required=False, help="Path to the image")
    ap.add_argument("-flp", "--flip_imgae", required=False, help="Path to the image")
    args = vars(ap.parse_args())
    print(f"All args: {args}")
    return args


if __name__ == '__main__':
    args = processe_args()
    camera = PiCamera()
    camera.resolution = (640, 480)
    #camera.vflip = True
    raw_capture = PiRGBArray(camera, size=(640, 480))
    time.sleep(1)
    print("String the journey")
    for c in ["yellow"]:#,"red"
        gogo(camera, raw_capture,cone_color=c, home_cone_color="red")
    print("End")
    fanshim.set_fan(False)
