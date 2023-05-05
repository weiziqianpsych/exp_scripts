#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    start.py
    Copyright (C) 2023, Ziqian Wei

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    If you find it useful in your research, please consider citing.

    @misc{weiziqianpsych,
        author = {Wei, Z.},
        title = {exp_scripts},
        year = 2023,
        version = {0.0.1},
        publisher = {Github},
        url = {https://github.com/weiziqianpsych/exp_scripts}
    }
"""

from psychopy.gui import DlgFromDict
import csv
import time
from psychopy import core, event, visual
from psychopy.gui import DlgFromDict

# window ---------------------------------------------------------------------------------------------------------------
window_size = [1400, 700]

# open a window
win = visual.Window(
    size=window_size, fullscr=False, screen=0, winType='pyglet',
    allowGUI=True, allowStencil=False, color="white",
    colorSpace='rgb', units='pix')

mouse = event.Mouse(win=win)

# stimuli --------------------------------------------------------------------------------------------------------------
q1 = visual.ImageStim(
    win,
    image='/Users/weiziqian/Desktop/q1.png',
    pos=(0.0, 100),
    size=(702/2, 468/2)
)

q1_item1 = visual.ImageStim(
    win,
    image='/Users/weiziqian/Desktop/q1_item1.png',
    pos=(0, -200),
    size=(702/4, 468/4)
)

rect = visual.Rect(
    win,
    size=q1_item1.size,
    lineWidth=5,
    lineColor="grey",
    fillColor=None,
    pos=q1_item1.pos
)

# loop -----------------------------------------------------------------------------------------------------------------
clicked = False

while True:

    if q1_item1.contains(event.Mouse().getPos()):

        if not clicked:
            rect.opacity = 1

        if event.Mouse().isPressedIn(q1_item1):
            if not clicked:
                rect.opacity = 1
                clicked = True

    else:
        rect.opacity = 0

    q1.draw()
    q1_item1.draw()
    rect.draw()
    win.flip()

    if clicked:
        core.wait(2)
