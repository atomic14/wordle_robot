# import the solving code from the solver notebook
from ipynb.fs.defs.solver import filter_words, get_best_guess
from ipynb.fs.defs.image_processing import (
    preprocess_image,
    find_phone_corners,
    get_phone_transform,
    locate_print_bed,
    get_printer_transform,
    press_key,
    get_grid_colors,
    PolygonColor,
)
from printer_control import PrinterAPI
from camera import Camera
from words import correct_words
import time

PRINTER_URL = "http://192.168.1.240"
# these number were obtained by manually moving the printer heead
# over the purple dots and reading off the coordinates
PRINTBED_TOP_LEFT = (235, 22)
PRINTBED_TOP_RIGHT = (52, 22)
PRINTBED_BOTTOM_LEFT = (235, 190)
PRINTBED_BOTTOM_RIGHT = (52, 190)
# these values were found by manually moving the printer head
# up and down and reading off the coordinates
TOUCH_PEN_UP = 50
TOUCH_PEN_DOWN = 43
# this is the white area of the screen
PHONE_SCREEN_WIDTH = 1170
PHONE_SCREEN_HEIGHT = 2532 - (404 + 140)
PHONE_SCREEN_BOTTOM_LEFT = (0, 0)
PHONE_SCREEN_BOTTOM_RIGHT = (PHONE_SCREEN_WIDTH, 0)
PHONE_SCREEN_TOP_LEFT = (0, PHONE_SCREEN_HEIGHT)
PHONE_SCREEN_TOP_RIGHT = (PHONE_SCREEN_WIDTH, PHONE_SCREEN_HEIGHT)


def send_word(word, printer, phone_transform, printer_transform):
    for index, letter in enumerate(word):
        press_key(letter, printer, phone_transform, printer_transform, index == 4)


def process_colors(word, grid_colors, row_index):
    letters_in_word = set()
    letters_not_in_word = set()
    letters_correct_position = []
    letters_wrong_position = []

    for index, letter in enumerate(word):
        if grid_colors[row_index][index] == PolygonColor.NONE:
            letters_not_in_word.add(letter)
        if grid_colors[row_index][index] == PolygonColor.GREEN:
            letters_correct_position.append((letter, index))
            letters_in_word.add(letter)
        if grid_colors[row_index][index] == PolygonColor.ORANGE:
            letters_wrong_position.append((letter, index))
            letters_in_word.add(letter)
    return (
        letters_correct_position,
        letters_wrong_position,
        letters_in_word,
        letters_not_in_word,
    )


def main():
    # initialize the camera
    camera = Camera(url="http://wordle.local:8000/grab_frame")
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
    time.sleep(10)
    # grab a frame from the camera
    print("Grabbing frame...")
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
        PHONE_SCREEN_TOP_RIGHT,
    )
    print("Found the phone")
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
    print("Found the printer")
    # we've now got everything we need to make our first guess!
    guess = "raise"
    words = correct_words
    row_index = 0
    while len(words) > 0:
        print(f"Guessing the word... '{guess}'")
        send_word(f"{guess}\n", printer, phone_transform, printer_transform)
        # present the printer bed so we can get a clear shot of the phone
        printer.present_bed()
        # grab a frame from the camera
        print("Grabbing frame...")
        img = camera.grab_frame()
        img, gray, hsv = preprocess_image(img)
        # get the grid colors
        grid_colors, _, _ = get_grid_colors(hsv, phone_transform)
        print(grid_colors)
        # work out the colors for the guessed letters
        (
            letters_correct_position,
            letters_wrong_position,
            letters_in_word,
            letters_not_in_word,
        ) = process_colors(guess, grid_colors, row_index)
        print("Letters in correct positions", letters_correct_position)
        print("Letters in wrong positions", letters_wrong_position)
        print("Letters in word", letters_in_word)
        print("Letters not in word", letters_not_in_word)
        # have we finised?
        if len(letters_correct_position) == 5:
            print("We've found the word!")
            break
        # filter the words based on the guess and colors
        words = filter_words(
            words,
            letters_correct_position,
            letters_wrong_position,
            letters_in_word,
            letters_not_in_word,
        )
        # get the next best guess
        guess = get_best_guess(words)
        row_index = row_index + 1


if __name__ == "__main__":
    # execute only if run as the entry point into the program
    main()
