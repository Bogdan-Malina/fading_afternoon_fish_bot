import time
import numpy as np
import cv2
from mss import mss
from PIL import Image
import pyautogui as pg

mon = {'top': 500, 'left': 3225, 'width': 200, 'height': 200}
# mon = {'top': 640, 'left': 2630, 'width': 90, 'height': 90}

TEMPLATE_NO_ACTIV = cv2.imread('img/no_activ.png', cv2.IMREAD_GRAYSCALE)
# TEMPLATE_NO_ACTIV = cv2.imread('img/img.png', cv2.IMREAD_GRAYSCALE)
TEMPLATE_ACTIV = cv2.imread('img/activ.png', cv2.IMREAD_GRAYSCALE)
# TEMPLATE_ACTIV = cv2.imread('img/img_1.png', cv2.IMREAD_GRAYSCALE)
THRESHOLD = 0.8

minigame_status = False
fish_status = False

time.sleep(3)


def get_match(image_gray, template):
    res = cv2.matchTemplate(image_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res > THRESHOLD)

    for _ in loc:
        if _.any() >= THRESHOLD:
            return True
    return False


def minigame(btn_pressed, btn_no_pressed, status):
    if btn_no_pressed and not status:
        pg.keyDown('z')
        return True
    elif btn_no_pressed:
        pg.keyUp('z')
    elif btn_pressed:
        pg.keyDown('z')
    else:
        pg.keyUp('z')
        if status:
            return False
        elif not status:
            pg.keyDown('z')
            pg.keyUp('z')


with mss() as sct:
    while True:
        screenShot = sct.grab(mon)
        img = Image.frombytes(
            'RGB',
            (screenShot.width, screenShot.height),
            screenShot.rgb,
        )
        pix = np.array(img)
        img_gray = cv2.cvtColor(pix, cv2.COLOR_BGRA2GRAY)

        activ_button = get_match(
            image_gray=img_gray,
            template=TEMPLATE_ACTIV
        )
        no_activ_button = get_match(
            image_gray=img_gray,
            template=TEMPLATE_NO_ACTIV
        )

        minigame_status = minigame(
            btn_pressed=activ_button,
            btn_no_pressed=no_activ_button,
            status=minigame_status
        )

        print(no_activ_button, activ_button)

        if cv2.waitKey(33) & 0xFF in (
            ord('q'),
            27,
        ):
            break