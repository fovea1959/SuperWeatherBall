# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This examples shows the use of anchor_point and anchored_position.
"""
import board
import terminalio
import displayio
from adafruit_display_text import label

def fill(text_group, text):

    DISPLAY_WIDTH = 160
    DISPLAY_HEIGHT = 240

    text_area_top_left = label.Label(terminalio.FONT, text=text)
    text_area_top_left.anchor_point = (0.0, 0.0)
    text_area_top_left.anchored_position = (0, 0)

    text_area_top_middle = label.Label(terminalio.FONT, text=text)
    text_area_top_middle.anchor_point = (0.5, 0.0)
    text_area_top_middle.anchored_position = (DISPLAY_WIDTH / 2, 0)

    text_area_top_right = label.Label(terminalio.FONT, text=text)
    text_area_top_right.anchor_point = (1.0, 0.0)
    text_area_top_right.anchored_position = (DISPLAY_WIDTH, 0)

    text_area_middle_left = label.Label(terminalio.FONT, text=text)
    text_area_middle_left.anchor_point = (0.0, 0.5)
    text_area_middle_left.anchored_position = (0, DISPLAY_HEIGHT / 2)

    text_area_middle_middle = label.Label(terminalio.FONT, text=text)
    text_area_middle_middle.anchor_point = (0.5, 0.5)
    text_area_middle_middle.anchored_position = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)

    text_area_middle_right = label.Label(terminalio.FONT, text=text)
    text_area_middle_right.anchor_point = (1.0, 0.5)
    text_area_middle_right.anchored_position = (DISPLAY_WIDTH, DISPLAY_HEIGHT / 2)

    text_area_bottom_left = label.Label(terminalio.FONT, text=text)
    text_area_bottom_left.anchor_point = (0.0, 1.0)
    text_area_bottom_left.anchored_position = (0, DISPLAY_HEIGHT)

    text_area_bottom_middle = label.Label(terminalio.FONT, text=text)
    text_area_bottom_middle.anchor_point = (0.5, 1.0)
    text_area_bottom_middle.anchored_position = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT)

    text_area_bottom_right = label.Label(terminalio.FONT, text=text)
    text_area_bottom_right.anchor_point = (1.0, 1.0)
    text_area_bottom_right.anchored_position = (DISPLAY_WIDTH, DISPLAY_HEIGHT)

    text_group.append(text_area_top_middle)
    text_group.append(text_area_top_left)
    text_group.append(text_area_top_right)
    text_group.append(text_area_middle_middle)
    text_group.append(text_area_middle_left)
    text_group.append(text_area_middle_right)
    text_group.append(text_area_bottom_middle)
    text_group.append(text_area_bottom_left)
    text_group.append(text_area_bottom_right)

master_group = displayio.Group()

text_group0 = displayio.Group()
fill(text_group0, '0')
master_group.append(text_group0)

text_group1 = displayio.Group(x=160)
fill(text_group1, '1')
master_group.append(text_group1)

board.DISPLAY.show(master_group)

while True:
    pass
