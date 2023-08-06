#!/usr/bin/env python
'''
mouse_and_match.py [-i path | --input path: default ../data/]

Demonstrate using a mouse to interact with an image:
 Read in the images in a directory one by one
 Allow the user to select parts of an image with a mouse
 When they let go of the mouse, it correlates (using matchTemplate) that patch with the image.

 SPACE for next image
 ESC to exit
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2 as cv

# built-in modules
import os
import sys
import glob
import argparse
from math import *

from briecheese_interface import BriecheeseInterface
from frame_handler import FrameHandler

class App():

    def __init__(self):
        self.briecheeseInterface = BriecheeseInterface()

        parser = argparse.ArgumentParser(description='Demonstrate mouse interaction with images')
        parser.add_argument("-i","--input", default='../data/', help="Input directory.")
        args = parser.parse_args()
        path = args.input

        cv.namedWindow("point_select_view",1)
        cv.setMouseCallback("point_select_view", self.onmouse)

        self.frameHandler = FrameHandler(glob.glob( os.path.join(path, '*.*') ))

    def onmouse(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONUP:

            view = self.briecheeseInterface.set_point(x, y)
            cv.imshow("point_select_view", view)

    def run(self):
        while True:
            current_file_name, current_frame = self.frameHandler.get_current_img()

            try:
                view = self.briecheeseInterface.set_frame(current_file_name, current_frame)
            except RuntimeError as e:
                print(e)
                self.frameHandler.show_next()
                continue

            cv.imshow("point_select_view", view)
            user_input = cv.waitKey()

            if user_input == ord("n"):
                self.frameHandler.show_next()
            if user_input == ord("p"):
                self.frameHandler.show_previous()
            if user_input == ord("c"):
                self.briecheeseInterface.calculation()
            if user_input == ord("q"):
                break

        print('Done')


if __name__ == '__main__':
    print(__doc__)
    App().run()
    cv.destroyAllWindows()
