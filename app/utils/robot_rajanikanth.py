from app.utils.video_stream import StreamThreaded
from app.utils.robot_custome_exception import ConeColorMissing
import cv2
from threading import Thread
from app.utils.find_objects import FindCones
import numpy as np
from easygopigo3 import EasyGoPiGo3
import time
import logging

'''
@newfield team: Venku Buragadda
'''


class NavigateRajani:
    '''
    Navigating the robot
    @author: Venku Buragadda
    '''

    def __init__(self, home_cone_color=None, show_video=False):
        self.log = logging.getLogger("main.navigation")
        self.camera = StreamThreaded()
        self.home_cone_color = home_cone_color
        self.camera.start()

        self.gopi_easy = EasyGoPiGo3()
        self.show_video = show_video
        self.cv2_window = None
        
        self.hard_stop = False
        
        # This will open a new cv2 to show the video feed in a different thread.
        if self.show_video:
            self.cv2_window = Thread(target=self.show_video_feed, args=())
            print("threade-2", self.cv2_window)
            self.cv2_window.start()
            print("Starting thread-2")

    def find_cone(self, cone_color=None):
        turn_deg_list = [0, 20, -40, 60, -80, 100, -120, 140, -160]
        find_cone_obj = FindCones(color=cone_color)
        if cone_color:
            while True:
                for turn_to_degree in turn_deg_list:
                    print("Checking Degree", turn_to_degree)
                    self.log.info(f"Moving to the following degree {turn_to_degree}")
                    self.gopi_easy.turn_degrees(turn_to_degree)
                    time.sleep(2)
                    frame = self.camera.read()
                    flag, frame_back, total_cones, boxes, cones_data = find_cone_obj.find_cone(frame)
                    if total_cones > 0:
                        return self
                else:
                    break

        else:
            raise ConeColorMissing("Cone color is required here and is missing")

    def show_video_feed(self):
        while True:
            frame = self.camera.read()
            if not (frame is None):
                frame = NavigateRajani.center_boundaries(frame)
                center_of_screen_coord, horiztl_line_lower_left_coord, horiztl_line_lower_right_coord, horiztl_line_upper_left_coord, horiztl_line_upper_right_coord, \
                left_bottom_bound_line_coord, left_top_bound_line_coord, right_bottom_bound_line_coord, rigth_top_bound_line_coord, width = NavigateRajani.screen_coordinates(frame)

                cv2.line(frame, left_top_bound_line_coord, left_bottom_bound_line_coord, [232, 206, 190], 1)
                cv2.line(frame, rigth_top_bound_line_coord, right_bottom_bound_line_coord, [232, 206, 190], 1)

                cv2.line(frame, rigth_top_bound_line_coord, right_bottom_bound_line_coord, [232, 206, 190], 1)

                # Center vertical line
                cv2.line(frame, (center_of_screen_coord[0], 0), (center_of_screen_coord[0], width), [0, 255, 0], 1)

                cv2.line(frame, horiztl_line_upper_left_coord, horiztl_line_upper_right_coord, [200, 90, 60], 1)
                cv2.line(frame, horiztl_line_lower_left_coord, horiztl_line_lower_right_coord, [200, 90, 60], 1)

                cv2.putText(frame, f"Upper: {horiztl_line_upper_left_coord},{horiztl_line_upper_right_coord}",
                            horiztl_line_upper_left_coord, cv2.FONT_HERSHEY_SIMPLEX, .5,
                            (0, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(frame, f"Lower: {horiztl_line_lower_left_coord},{horiztl_line_lower_right_coord}",
                            horiztl_line_lower_left_coord, cv2.FONT_HERSHEY_SIMPLEX, .5,
                            (0, 255, 255), 1, cv2.LINE_AA)

                # cv2.putText(frame, f"Temp:{temperature}", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 255), 1,
                #             cv2.LINE_AA)

                cv2.imshow("Video Feed", frame)
                if self.hard_stop:
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
        return center_of_screen_coord, horiztl_line_lower_left_coord, horiztl_line_lower_right_coord, horiztl_line_upper_left_coord, horiztl_line_upper_right_coord, left_bottom_bound_line_coord, left_top_bound_line_coord, right_bottom_bound_line_coord, rigth_top_bound_line_coord, width

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
        self.log.info("Context open")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.log.info("Destroying all the resources")
        self.hard_stop = True
        self.camera.stop()
        if self.show_video:
            self.cv2_window.join()
        cv2.destroyAllWindows()
        
