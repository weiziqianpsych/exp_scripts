#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Raven_test.py
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
from psychopy.visual import Window, ImageStim, TextStim, Rect
from psychopy.sound import Sound
from psychopy.event import Mouse, getKeys
from psychopy.core import wait, getTime, quit

from datetime import datetime
from csv import writer

# setting --------------------------------------------------------------------------------------------------------------
n_quest = 23  # how many questions/trials?
n_item = 6  # how many items for each question/trial?

# dialog ---------------------------------------------------------------------------------------------------------------
sub_info = {'id': '', 'name': '', 'gender': ['male', 'female'],
            'grade': '', 'school': ''}

inputDlg = DlgFromDict(dictionary=sub_info, title='basic information',
                       order=['id', 'name', 'gender', 'grade', 'school'])

# window ---------------------------------------------------------------------------------------------------------------
width = 1.366
height = 0.768

win = Window(
    size=(width*1000, height*1000),
    fullscr=False, screen=0, winType='pyglet',
    allowGUI=True, allowStencil=False, color="white",
    colorSpace='rgb', units='norm')

mouse = Mouse()

# stimuli --------------------------------------------------------------------------------------------------------------
# recording
my_sound = Sound("sound/sound.wav")

# instruction
instruction1 = ImageStim(win, image='pic/instruction1.png', pos=(0, 0.1), size=(1.5/width, 1.125/height))
instruction2 = ImageStim(win, image='pic/instruction2.png', pos=(0, 0.1), size=(1.5/width, 1.125/height))

# the continue button
button_continue = ImageStim(win, image='pic/continue.png', pos=(0, -0.80), size=(0.15/width, 0.15/height))
rect_continue = Rect(win, size=button_continue.size*1.2, lineWidth=10, lineColor="grey", pos=button_continue.pos)

# questions
quest = []
for i in range(0, n_quest):  # number of questions
    quest.append(ImageStim(win, image='pic/q{}.png'.format(i), name='q{}.png'.format(i), pos=(0, 0.3),
                           size=(0.3*2.74/width, 0.3*1.83/height)))

# items
item = dict()  # item pictures for each question
initial_pos = [(-0.2, -0.3), (0.0, -0.3), (0.2, -0.3), (-0.2, -0.6), (0.0, -0.6), (0.2, -0.6)]
for i in range(0, len(quest)):  # number of questions
    some_items = []
    for j in range(0, n_item):  # number of items for a single question

        some_items.append(ImageStim(
            win,
            image='pic/q{}_item{}.png'.format(i, j),
            name='q{}_item{}.png'.format(i, j),
            pos=(initial_pos[j][0], initial_pos[j][1]),
            size=(0.2*1.03/width, 0.2*0.65/height)
        ))

    item['q{}'.format(i)] = some_items

# rectangle
rect = []  # rectangles for each question
for j in range(0, n_item):
    rect.append(Rect(win, size=item['q1'][j].size*1.2, lineWidth=10, lineColor="grey", pos=item['q1'][j].pos))

# data -----------------------------------------------------------------------------------------------------------------
data_question = []
data_resp = []
data_rt = []

answer_key = []

# instruction ----------------------------------------------------------------------------------------------------------
clicked = False

instruction1.autoDraw = True
button_continue.autoDraw = True
rect_continue.autoDraw = True

my_sound.play()

while not clicked:

    # the cursor
    if button_continue.contains(mouse.getPos()):
        if not clicked:
            rect_continue.autoDraw = True

        if mouse.isPressedIn(button_continue):
            if not clicked:
                clicked = True
    else:
        rect_continue.autoDraw = False

    if not clicked:
        win.flip()

    else:
        instruction1.autoDraw = False
        button_continue.autoDraw = False
        rect_continue.autoDraw = False

        win.flip()

        my_sound.stop()

# loop -----------------------------------------------------------------------------------------------------------------
frame_rate = win.getActualFrameRate(nIdentical=60, nMaxFrames=100, nWarmUpFrames=10, threshold=1)
frame_rate = 30

for i in range(0, len(quest)):  # run each question

    # draw stimuli for this question
    quest[i].autoDraw = True
    for x in range(0, n_item):
        item['q{}'.format(i)][x].autoDraw = True
        rect[x].autoDraw = False

    t0 = getTime()
    clicked = False

    for n in range(0, round(frame_rate) * 600):
        while not clicked:  # what happens in each question's interface
            # the cursor
            for x in range(0, n_item):
                if item['q{}'.format(i)][x].contains(mouse.getPos()):
                    # show the border when the cursor moves in
                    if not clicked:
                        rect[x].autoDraw = True

                    if mouse.isPressedIn(item['q{}'.format(i)][x]):
                        if not clicked:
                            t1 = getTime()
                            resp = item['q{}'.format(i)][x].name

                            rect[x].autoDraw = True
                            clicked = True
                else:
                    rect[x].autoDraw = False

            if not clicked:
                win.flip()

            else:  # get ready to move to the next question

                # remove stimuli in this question
                quest[i].autoDraw = False
                for x in range(0, n_item):
                    item['q{}'.format(i)][x].autoDraw = False
                    rect[x].autoDraw = False

                # record
                data_rt.append(t1 - t0)
                data_question.append(quest[i].name)
                data_resp.append(resp)

                win.flip()
                wait(0.5)  # 500ms interval

# end ------------------------------------------------------------------------------------------------------------------
instruction2.draw()
win.flip()

# accuracy -------------------------------------------------------------------------------------------------------------
answer_key = [
    3, 4, 0, 1, 5,  # A1 to B12
    2, 5, 1, 0, 2,
    3, 4,
    1, 5, 0, 1, 0,  # B1 to B12
    2, 4, 5, 3, 2,
    3, 4
]

data_acc = []
for i in range(0, len(data_resp)):
    if data_resp[i] == "q{}_item{}.png".format(i, answer_key[i]):
        data_acc.append(1)
    else:
        data_acc.append(0)

# data -----------------------------------------------------------------------------------------------------------------
# get time
my_time = datetime.now()
my_time = my_time.strftime("%d%m%Y_%H%M%S")

# save as a .csv file
c = open('data/Data_Raven_{}_{}.csv'.format(sub_info['id'], my_time), 'w', encoding='utf-8', newline='')
csv_writer = writer(c)
csv_writer.writerow(['id', 'name', 'gender', 'grade', 'school', 'question', 'resp', 'acc', 'rt'])  # head
for i in range(0, len(data_question)):
    csv_writer.writerow([
        sub_info['id'],
        sub_info['name'],
        sub_info['gender'],
        sub_info['grade'],
        sub_info['school'],
        data_question[i],
        data_resp[i],
        data_acc[i],
        data_rt[i]
    ])
c.close()

wait(2)
