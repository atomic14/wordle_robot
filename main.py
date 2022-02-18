# import the solving code from the solver notebook
import ipynb.fs.defs.solver
from ipynb.fs.defs.image_processing import (
    preprocess_image,
    find_phone_corners,
    get_phone_transform,
    locate_print_bed,
    get_printer_transform,
)
from printer_control import PrinterAPI
from camera import Camera

PRINTER_URL = "http://192.168.1.240"
# these number were obtained by manually moving the printer heead
# over the purple dots and reading off the coordinates
PRINTBED_TOP_LEFT = (52, 190)
PRINTBED_TOP_RIGHT = (235, 190)
PRINTBED_BOTTOM_LEFT = (52, 22)
PRINTBED_BOTTOM_RIGHT = (235, 22)
# these values were found by manually moving the printer head
# up and down and reading off the coordinates
TOUCH_PEN_UP = 50
TOUCH_PEN_DOWN = 43
# this is the white area of the screen
PHONE_SCREEN_WIDTH = 1170
PHONE_SCREEN_HEIGHT = 1952
PHONE_SCREEN_BOTTOM_LEFT = (0, 0)
PHONE_SCREEN_BOTTOM_RIGHT = (PHONE_SCREEN_WIDTH, 0)
PHONE_SCREEN_TOP_LEFT = (0, PHONE_SCREEN_HEIGHT)
PHONE_SCREEN_TOP_RIGHT = (PHONE_SCREEN_WIDTH, PHONE_SCREEN_HEIGHT)


def main():
    # initialize the camera
    camera = Camera(url="http://wordle.local/grab_frame")
    # initialize the printer
    printer = PrinterAPI(PRINTER_URL)
    printer.connect()
    # home the printer and then move it so the printer bed is presented
    if not printer.is_homed():
        printer.home()
    # move the pen up so we don't crash into the bed
    printer.move(z=TOUCH_PEN_UP)
    # move the print bed all the way out to the front
    printer.present_bed()
    # we're now ready to start solving
    input("Put your phone on the bed and press enter...")
    # grab a frame from the camera
    img = camera.grab_frame()
    img, gray, hsv = preprocess_image(img)
    # find the phone corners in the camer image
    (
        camera_phone_top_right,
        camera_phone_bottom_left,
        camera_phone_top_left,
        camera_phone_bottom_right,
    ) = find_phone_corners(gray)
    # get the phone transform - this maps from locations on the phone
    # screen to locations in the camera image
    phone_transform = get_phone_transform(
        camera_phone_bottom_left,
        camera_phone_bottom_right,
        camera_phone_top_right,
        PHONE_SCREEN_BOTTOM_LEFT,
        PHONE_SCREEN_BOTTOM_RIGHT,
        PHONE_SCREEN_TOP_LEFT,
    )
    # locate the printer bed
    (
        camera_printbed_top_right,
        camera_printbed_bottom_left,
        camera_printbed_top_left,
    ) = locate_print_bed(hsv)
    # get the transform from the camera image to the printer bed
    printer_transform = get_printer_transform(
        camera_printbed_top_left,
        camera_printbed_top_right,
        camera_printbed_bottom_left,
        PRINTBED_TOP_LEFT,
        PRINTBED_TOP_RIGHT,
        PRINTBED_BOTTOM_LEFT,
    )
    # we've now got everything we need to make our first guess!


if __name__ == "__main__":
    # execute only if run as the entry point into the program
    main()
