from app.utils.video_stream import StreamThreaded
from app.utils.robot_custome_exception import ConeColorMissing
from app.utils.modeling import infer_image
import cv2
from threading import Thread
from app.utils.find_objects import FindCones
import numpy as np
from easygopigo3 import EasyGoPiGo3
import time
import logging
from queue import Queue
from app.utils.raspberry_utils import processor_temperature
from app.audio_models.hmm_models.hmm_audio_detection_modified import start_audio_model
from app.post_results.robo_client import connection
from app.image_models.tiny_yolov3.yolo_v3_tiny import main_run_model
import sys
'''
@newfield team: Venku Buragadda
'''


class NavigateRajani:
    '''
    Navigating the robot
    @author: Venku Buragadda
    '''

    def __init__(self, home_cone_color="yellow", destination_cone_color="red",
                 show_video=False, show_video_limit=False, inference=False, is_audio_inference=False):
        self.log = logging.getLogger('gpg.find_cone')

        self.camera = StreamThreaded()
        self.camera.start()

        self.gopi_easy = EasyGoPiGo3()
        self.servo = self.gopi_easy.init_servo()
        self.servo.reset_servo()

        self.home_cone_color = home_cone_color
        self.show_video = show_video
        self.cv2_window = None
        self.show_video_limit = show_video_limit
        self.hard_stop = False
        self.destination_cone_color = None
        self.cone_data = None
        # self.find_cone_obj = FindCones(color=self.destination_cone_color)
        self.find_cone_obj = None
        self.is_audio_inference = is_audio_inference

        self.inference = inference
        self.img_inference = None
        self.q = None
        # if self.inference:
        #     self.q = Queue()
        #     self.img_inference = Thread(target=infer_image, args=(self.q, 0.5))
        #     self.img_inference.start()
        if self.inference:
            self.q = Queue()
            self.img_inference = Thread(target=main_run_model, args=(self.q, 0.5))
            self.img_inference.start()

        self.audio_inference = None
        if self.is_audio_inference:
            self.audio_inference = Thread(target=start_audio_model, args=())
            self.audio_inference.start()

    def create_objects(self, destination_cone_color="red"):
        self.destination_cone_color = destination_cone_color
        self.find_cone_obj = FindCones(color=self.destination_cone_color)

        # This will open a new cv2 to show the video feed in a different thread.
        if self.show_video:
            self.cv2_window = Thread(target=self.show_video_feed, args=(self.show_video_limit,),
                                     name="Video Feed Thread")
            print("thread-2", self.cv2_window)
            self.cv2_window.start()
            print("Starting thread-2")

        return self

    def find_cone(self, cone_color=None):
        turn_deg_list = [0, 20, -40, 60, -80, 100, -120, 140, -160, 180, -200, 220, -240, 260, -280, 300, -320, 340,
                         -360]

        while True:
            for turn_to_degree in turn_deg_list:
                print("Checking Degree", turn_to_degree)
                # self.log.info(f"Moving to the following degree {turn_to_degree}")
                self.gopi_easy.turn_degrees(turn_to_degree)
                time.sleep(1)
                frame = self.camera.read()
                flag, frame_back, total_cones, boxes, cones_data = self.get_cone_coordinates(frame)
                if total_cones > 0:
                    self.cone_data = cones_data
                    return self
            else:
                break

    def get_cone_coordinates(self, frame):
        flag, frame_back, total_cones, boxes, cones_data = self.find_cone_obj.find_cone(frame)
        # print("Find code class called: ", total_cones)
        return flag, frame_back, total_cones, boxes, cones_data

    def check_util_cone_data_is_returned_from_view_feed(self):
        while True:
            frame = self.camera.read()
            flag, frame_back, total_cones, boxes, cones_data = self.get_cone_coordinates(frame)
            if total_cones > 0:
                return flag, frame_back, total_cones, boxes, cones_data

    def center_the_cone(self, height_range=(280, 360), precise=False):
        frame = self.camera.read()
        center_of_screen_coord, horiztl_line_lower_left_coord, horiztl_line_lower_right_coord, horiztl_line_upper_left_coord, \
        horiztl_line_upper_right_coord, left_bottom_bound_line_coord, left_top_bound_line_coord, right_bottom_bound_line_coord, \
        rigth_top_bound_line_coord, width = NavigateRajani.screen_coordinates(frame)
        while True:
            # time.sleep(3)
            frame = self.camera.read()
            flag, frame_back, total_cones, boxes, cones_data = self.get_cone_coordinates(frame)

            if total_cones > 0:
                cone_bounding_box = cones_data['cone-0']['bouding_box_center']

                # print(f"Cone data: {cone_bounding_box}")
                # print(f"Coordinates: ", left_top_bound_line_coord, rigth_top_bound_line_coord)
                steer = 1
                if precise:
                    time.sleep(1)
                    frame = self.camera.read()
                    flag, frame_back, total_cones, boxes, cones_data = self.check_util_cone_data_is_returned_from_view_feed()
                    cone_bounding_box = cones_data['cone-0']['bouding_box_center']

                    # Steer by 1 is making the coordinate to change by 10 to 25 at least
                    center_boundary_left_right_width = (
                        left_top_bound_line_coord[0] - 25, rigth_top_bound_line_coord[0] + 25)
                    self.gopi_easy.set_eye_color((255, 0, 255))
                else:
                    center_boundary_left_right_width = (
                        left_top_bound_line_coord[0] - 50, rigth_top_bound_line_coord[0] + 50)
                    steer = 3
                    self.gopi_easy.set_eye_color((0, 255, 127))
                #print(f"************Center Boundary", center_boundary_left_right_width)
                #print(
                #    f" cone_bounding_box[0] > height_range[1] : {cone_bounding_box[0] > height_range[1]}, {cone_bounding_box[0]},{height_range[1]}")
                if not center_boundary_left_right_width[0] <= cone_bounding_box[0] <= center_boundary_left_right_width[
                    1]:
                    # print(
                    #     f"Centring Cone: {cone_bounding_box[0] > height_range[1]} and the values {cone_bounding_box[0]} and {height_range[1]}")
                    if cone_bounding_box[0] > height_range[1]:
                        # move right
                        print(F"Moving right")
                        self.gopi_easy.open_left_eye()
                        self.gopi_easy.steer(steer, 0)
                        time.sleep(1)
                        self.gopi_easy.stop()
                        self.gopi_easy.close_left_eye()
                        continue
                    # print(
                    #     f"Centring Cone - < condition : {cone_bounding_box[0] < height_range[1]} and the values {cone_bounding_box[0]} and {height_range[1]}")
                    if cone_bounding_box[0] < height_range[1]:
                        # move left
                        print(F"Moving left")
                        self.gopi_easy.open_right_eye()

                        self.gopi_easy.steer(0, steer)
                        time.sleep(1)
                        self.gopi_easy.close_right_eye()
                        self.gopi_easy.stop()
                        continue
                else:
                    # getting update cone data after the robot is centered.
                    self.cone_data = cones_data
                    return self

    def move_towards_the_cone_using_distance_sensor(self, metrics="inches"):
        dist_sensor = self.gopi_easy.init_distance_sensor()
        if metrics == 'inches':
            return dist_sensor.read_inches()
        if metrics == "mm":
            return dist_sensor.read_mm()

    def move_towards_the_cone(self, drive_inches=3, dist_to_object=("inches", 10), dist_sensor_error=3):
        is_cone_in_picture = 0
        while True:
            self.center_the_cone()
            frame = self.camera.read()
            distance_to_cone = self.move_towards_the_cone_using_distance_sensor(metrics=dist_to_object[0])
            flag, frame_back, total_cones, boxes, cones_data = self.get_cone_coordinates(frame)
            is_cone_in_picture += 1
            if total_cones:
                is_cone_in_picture = 0
                cone_bottom_mid_point = self.get_cone_bottom_mid_point(boxes)

                # Cone rectangel box bottom line mid point
                cone_lower_rec_boundary_mid_point_height = cone_bottom_mid_point[1]
                center_of_screen_coord, horiztl_line_lower_left_coord, horiztl_line_lower_right_coord, horiztl_line_upper_left_coord, horiztl_line_upper_right_coord, \
                left_bottom_bound_line_coord, left_top_bound_line_coord, right_bottom_bound_line_coord, rigth_top_bound_line_coord, width = NavigateRajani.screen_coordinates(
                    frame)

                # Screen bottom box line. top(upper) bottom(lower) left coordinates of Y

                bottom_boundary_upper_lower_height = (
                    horiztl_line_upper_left_coord[1] - 10, horiztl_line_lower_left_coord[1] + 40)

                # print(f"*********Boundaries calculated {bottom_boundary_upper_lower_height}")
                # if the cone bounding box bottom line center is not with in the boundary
                print(
                    f"Top level if and else check {bottom_boundary_upper_lower_height[0]} <= {cone_lower_rec_boundary_mid_point_height}, <= {bottom_boundary_upper_lower_height[1]}  condition: {bottom_boundary_upper_lower_height[0] <= cone_lower_rec_boundary_mid_point_height <= bottom_boundary_upper_lower_height[1]}")
                if not bottom_boundary_upper_lower_height[0] <= cone_lower_rec_boundary_mid_point_height <= \
                       bottom_boundary_upper_lower_height[1]:
                    # print(f"Checking if and  elif ")
                    if bottom_boundary_upper_lower_height[0] > cone_lower_rec_boundary_mid_point_height:
                        # print(
                        #     F"boundr upp lower height is greated-dr fwd {bottom_boundary_upper_lower_height[0]} > {cone_lower_rec_boundary_mid_point_height}")
                        self.gopi_easy.drive_inches(drive_inches)
                    else:
                        # print(
                        #     F"boundr upp lower height is lower-dr back: {bottom_boundary_upper_lower_height[0]} < {cone_lower_rec_boundary_mid_point_height}")
                        self.gopi_easy.drive_inches(-drive_inches)
                elif horiztl_line_lower_left_coord[1] <= cone_lower_rec_boundary_mid_point_height:
                    # self.gopi_easy.drive_inches(-1)
                    self.fine_tune_distance_to_the_cone(dist_sensor_error, dist_to_object)
                    time.sleep(2)

                else:
                    self.center_the_cone(precise=True)
                    # finally before the cone starts to orbit we are making it more precise.
                    self.fine_tune_distance_to_the_cone(dist_sensor_error, dist_to_object)
                    return self
                self.center_the_cone(precise=False)
            elif is_cone_in_picture > 30:
                self.gopi_easy.drive_inches(-10)

    def fine_tune_distance_to_the_cone(self, dist_sensor_error, dist_to_object):
        distance_to_cone = self.move_towards_the_cone_using_distance_sensor(metrics=dist_to_object[0])
        required_dist_to_cone = dist_to_object[1]
        print(f"Precise: {required_dist_to_cone}, {distance_to_cone} ")
        if required_dist_to_cone < distance_to_cone:
            print(
                f"Audjusting to this distance: {(distance_to_cone + dist_sensor_error) - required_dist_to_cone}")
            self.gopi_easy.drive_inches((distance_to_cone + dist_sensor_error) - required_dist_to_cone)
        else:
            print(f"Adjusting to negative distance: {((distance_to_cone + dist_sensor_error) - required_dist_to_cone)}")
            self.gopi_easy.drive_inches(-((distance_to_cone + dist_sensor_error) - required_dist_to_cone))

    def circle_the_cone(self, carpet=False, degrees=40, drive_inches_back_by=6):

        self.gopi_easy.turn_degrees(-90)
        if carpet:
            self.gopi_easy.orbit(480, degrees)
        else:
            self.gopi_easy.orbit(85, degrees)
            self.servo.reset_servo()
            self.servo.rotate_servo(10)
            time.sleep(1)
            self.camera.camera.capture('foo1.jpg')
            time.sleep(2)
            self.infer_image('foo1.jpg')

            # second semi circle
            self.gopi_easy.orbit(80, degrees)
            self.gopi_easy.turn_degrees(90)
            self.gopi_easy.drive_inches(-drive_inches_back_by)
            self.servo.reset_servo()
            time.sleep(2)
            self.camera.camera.capture('foo2.jpg')
            time.sleep(1)
            self.infer_image('foo2.jpg')
            self.gopi_easy.drive_inches(drive_inches_back_by)
            self.gopi_easy.turn_degrees(-90)
            self.servo.rotate_servo(10)

            self.gopi_easy.orbit(75, degrees)
            time.sleep(2)
            self.camera.camera.capture('foo3.jpg')
            self.gopi_easy.orbit(120, degrees)
            self.servo.reset_servo()
        self.gopi_easy.turn_degrees(90)
        self.gopi_easy.turn_degrees(220)
        return self

    def infer_image(self, image_path):
        self.q.put((image_path, self.destination_cone_color))

    def there_is_nothing_like_home(self):
        self.find_cone_obj = FindCones(color=self.home_cone_color)
        self.find_cone().center_the_cone(precise=True).move_towards_the_cone(drive_inches=8,
                                                                             dist_to_object=("inches", 5))
        # self.gopi_easy.drive_inches(10)
        self.gopi_easy.turn_degrees(180)
        return self

    def get_cone_bottom_mid_point(self, boxes):
        x, y, w, h = boxes[0]
        x1, y1, x4, y4 = (x, y, x + w, y + h)
        # tl = (x1, y1)
        # tr = (x4, y1)
        br = (x4, y4)
        bl = (x1, y4)
        # # (tl, tr, br, bl) = boxes[0]
        # (tlblX, tlblY) = NavigateRajani.midpoint(tl, bl)
        # (trbrX, trbrY) = NavigateRajani.midpoint(tr, br)
        rect_bottom_mind_point = NavigateRajani.midpoint(bl, br)
        return rect_bottom_mind_point

    @staticmethod
    def midpoint(ptA, ptB):
        return (ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5

    def show_video_feed(self, show_video_limit):
        logging.info("Showing the video feed")
        while True:
            frame = self.camera.read()
            if not (frame is None):
                center_of_screen_coord, horiztl_line_lower_left_coord, horiztl_line_lower_right_coord, horiztl_line_upper_left_coord, horiztl_line_upper_right_coord, \
                left_bottom_bound_line_coord, left_top_bound_line_coord, right_bottom_bound_line_coord, rigth_top_bound_line_coord, width = NavigateRajani.screen_coordinates(
                    frame)
                break

        while True:
            frame = self.camera.read()
            if not (frame is None):
                if not show_video_limit:
                    flag, frame_back, total_cones, boxes, cones_data = self.get_cone_coordinates(frame)
                    if total_cones:
                        rect_bottom_mind_point = self.get_cone_bottom_mid_point(boxes)
                        cv2.putText(frame_back, f"bottom: {rect_bottom_mind_point}",
                                    (int(rect_bottom_mind_point[0]), int(rect_bottom_mind_point[1])),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    .5, (0, 255, 255), 1, cv2.LINE_AA)
                        frame = frame_back
                    frame = NavigateRajani.center_boundaries(frame)

                    cv2.line(frame, left_top_bound_line_coord, left_bottom_bound_line_coord, [232, 206, 190], 1)
                    cv2.line(frame, rigth_top_bound_line_coord, right_bottom_bound_line_coord, [232, 206, 190], 1)

                    cv2.line(frame, rigth_top_bound_line_coord, right_bottom_bound_line_coord, [232, 206, 190], 1)

                    # Center vertical line
                    # print("Central vertical line", center_of_screen_coord[0], (center_of_screen_coord[0], width))
                    cv2.line(frame, (center_of_screen_coord[0], 0), (center_of_screen_coord[0], width), [0, 255, 0], 1)

                    cv2.line(frame, horiztl_line_upper_left_coord, horiztl_line_upper_right_coord, [200, 90, 60], 1)
                    cv2.line(frame, horiztl_line_lower_left_coord, horiztl_line_lower_right_coord, [200, 90, 60], 1)

                    cv2.line(frame, (horiztl_line_upper_left_coord[0], horiztl_line_upper_left_coord[1] - 60),
                             (horiztl_line_upper_right_coord[0], horiztl_line_upper_right_coord[1] - 60),
                             [90, 120, 160], 2)

                    cv2.putText(frame,
                                f"Upper: {horiztl_line_upper_left_coord},{horiztl_line_upper_right_coord}::: {horiztl_line_upper_left_coord[1] + 40}",
                                horiztl_line_upper_left_coord, cv2.FONT_HERSHEY_SIMPLEX, .5,
                                (0, 255, 255), 1, cv2.LINE_AA)
                    cv2.putText(frame, f"Lower: {horiztl_line_lower_left_coord},{horiztl_line_lower_right_coord}",
                                horiztl_line_lower_left_coord, cv2.FONT_HERSHEY_SIMPLEX, .5,
                                (0, 255, 255), 1, cv2.LINE_AA)
                temperature = processor_temperature()
                cv2.putText(frame, f"Temp:{temperature}", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 0), 1,
                            cv2.LINE_AA)

                cv2.imshow("Video Feed - 1", frame)
                if self.hard_stop:
                    print("Stop is called")
                    cv2.destroyAllWindows()
                    break
                key = cv2.waitKey(1) & 0xFF

    @staticmethod
    def screen_coordinates(frame):
        height, width, ch = frame.shape
        center_of_screen_coord = (width // 2, height // 2)
        # center boundaries
        left_top_bound_line_coord, left_bottom_bound_line_coord = (width - center_of_screen_coord[0] - 20, 0), (
            width - center_of_screen_coord[0] - 20, height)
        rigth_top_bound_line_coord, right_bottom_bound_line_coord = (width - center_of_screen_coord[0] + 20, 0), (
            width - center_of_screen_coord[0] + 20, height)
        # bottom boundaries
        horiztl_line_upper_left_coord, horiztl_line_upper_right_coord = (0, height - 100), (width, height - 100)
        horiztl_line_lower_left_coord, horiztl_line_lower_right_coord = (0, height - 50), (width, height - 50)
        return center_of_screen_coord, horiztl_line_lower_left_coord, horiztl_line_lower_right_coord, \
               horiztl_line_upper_left_coord, horiztl_line_upper_right_coord, left_bottom_bound_line_coord, \
               left_top_bound_line_coord, right_bottom_bound_line_coord, rigth_top_bound_line_coord, width

    @staticmethod
    def center_boundaries(frame):

        he, wi, ch = frame.shape
        center_of_the_screen = (wi // 2, he // 2)
        cv2.circle(frame, center_of_the_screen, 5, [255, 0, 0], -1)
        cv2.line(frame, center_of_the_screen, (center_of_the_screen[0] + 30, center_of_the_screen[1]), [0, 255, 0], 3)

        left_top, left_bottom = (wi - center_of_the_screen[0] - 40, 0), (wi - center_of_the_screen[0] - 40, he)
        right_top, right_bottom = (wi - center_of_the_screen[0] + 40, 0), (wi - center_of_the_screen[0] + 40, he)

        # print(F"Left: {left_top},{left_bottom} and Right: {right_top}, {right_bottom}")

        cv2.line(frame, left_top, left_bottom, [232, 206, 190], 1)
        cv2.line(frame, right_top, right_bottom, [232, 206, 190], 1)
        return frame

    def __enter__(self):
        # self.log.info("Context open")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        send_log_to_server()
        # self.log.info("Destroying all the resources")
        self.hard_stop = True
        self.camera.stop()
        if self.show_video:
            self.cv2_window.join()
        if self.inference:
            self.img_inference.join()
        cv2.destroyAllWindows()
        sys.exit()



def send_log_to_server():
    HOST, PORT = 'datastream.ilykei.com', 30078
    login = 'venku@uchicago.edu'
    password = 'Bne3SqJG'
    split_id = 19
    filename = 'gopigo.log'
    c = connection(HOST, PORT, login, password, split_id, filename)
    print(f"Logs Sent to the server: {c}")
