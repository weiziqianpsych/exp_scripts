#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    SVT.py
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
# instruction
instruction1 = ImageStim(win, image='pic/instruction1.png',  pos=(0, 0.1), size=(1.5/width, 1.125/height))
instruction2 = ImageStim(win, image='pic/instruction2.png',  pos=(0, 0.1), size=(1.5/width, 1.125/height))
instruction3 = ImageStim(win, image='pic/instruction3.png',  pos=(0, 0.1), size=(1.5/width, 1.125/height))
feedback1 = ImageStim(win, image='pic/feedback1.png',  pos=(0, 0.1), size=(1.5/width, 1.125/height))
feedback2 = ImageStim(win, image='pic/feedback2.png',  pos=(0, 0.1), size=(1.5/width, 1.125/height))

# the continue button
button_continue = ImageStim(win, image='pic/continue.png', pos=(0, -0.80), size=(0.15/width, 0.15/height))
rect_continue = Rect(win, size=button_continue.size*1.2, lineWidth=10, lineColor="grey", pos=button_continue.pos)

# fixation
fixation = TextStim(win=win, text='+', color="black")  # height=12 (default)

# selection buttons
check = ImageStim(win, image='pic/check.png', pos=(-0.25, -0.60), size=(0.15/width, 0.15/height))
cancel = ImageStim(win, image='pic/cancel.png', pos=(0.25, -0.60), size=(0.15/width, 0.15/height))
rect_check = Rect(win, size=check.size*1.2, lineWidth=10, lineColor="grey", fillColor=None, pos=check.pos)
rect_cancel = Rect(win, size=cancel.size*1.2, lineWidth=10, lineColor="grey", fillColor=None, pos=cancel.pos)

# trials: [SenStim, PicStim, Condition, CorrectAns]
practice = [["v1Sen1.wav", "v1Pic1.png", "1", "Y"],
            ["v1Sen2.wav", "v2Pic2.png", "2", "Y"]]
exp = [["v1Sen10.wav", "v1Pic10.png", "1", "Y"],
       ["v1Sen11.wav", "v1Pic11.png", "1", "Y"],
       ["v1Sen12.wav", "v2Pic12.png", "2", "Y"],
       ["v1Sen13.wav", "v2Pic13.png", "2", "Y"],
       ["ConSen1.wav", "ConPic14.png", "0", "N"],
       ["ConSen2.wav", "ConPic15.png", "0", "N"]]
data_tasks = ["prac"] * len(practice) + ["exp"] * len(exp)
data_materials = practice + exp

# input all items based on the lists
stimuli_prac = []
stimuli_exp = []
for i in range(0, len(practice)):
    stimuli_prac.append([
        Sound("sound/" + practice[i][0]),
        ImageStim(win, image='pic/' + practice[i][1], pos=(0, 0.3), size=(0.3*2.74/width, 0.3*2.74/height))
    ])
for i in range(0, len(exp)):
    stimuli_exp.append([
        Sound("sound/" + exp[i][0]),
        ImageStim(win, image='pic/' + exp[i][1], pos=(0, 0.3), size=(0.3*2.74/width, 0.3*2.74/height))
    ])

# data -----------------------------------------------------------------------------------------------------------------
data_question = []
data_answer_key = []
data_resp = []
data_rt = []
data_acc = []

# function -------------------------------------------------------------------------------------------------------------
frame_rate = win.getActualFrameRate(nIdentical=60, nMaxFrames=100, nWarmUpFrames=10, threshold=1)
frame_rate = 30


def instruction_page(instruction):
    # instruction
    clicked = False

    instruction.autoDraw = True
    button_continue.autoDraw = True
    rect_continue.autoDraw = True

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
            instruction.autoDraw = False
            button_continue.autoDraw = False
            rect_continue.autoDraw = False

            win.flip()


def SVT_game(trial, stimuli, feedback=False):
    # trials
    for i in range(0, len(trial)):

        # buffer, 2000 ms or 1000ms
        t = 2 if i == 0 else 1
        for n in range(0, int(round(frame_rate) * t)):
            win.flip()

        # fixation, 500 ms
        for n in range(0, int(round(frame_rate) * 0.500)):
            fixation.draw()
            win.flip()

        # buffer, 1000 ms
        for n in range(0, int(round(frame_rate) * 1)):
            win.flip()

        # recording
        stimuli[i][0].play()
        wait(stimuli[i][0].getDuration())

        # buffer, 1000 ms
        for n in range(0, int(round(frame_rate) * 1)):
            win.flip()

        # response, 60 min
        clicked = False
        t0 = getTime()
        for n in range(0, int(round(frame_rate) * 600)):

            # show stimuli
            stimuli[i][1].autoDraw = True
            check.autoDraw = True
            cancel.autoDraw = True

            if not clicked:
                if check.contains(mouse.getPos()):
                    rect_check.draw()

                if cancel.contains(mouse.getPos()):
                    rect_cancel.draw()

                if mouse.isPressedIn(check) or mouse.isPressedIn(cancel):
                    # resp
                    if mouse.isPressedIn(check):
                        item = check
                        resp = "Y"
                    elif mouse.isPressedIn(cancel):
                        item = cancel
                        resp = "N"

                    # save data
                    data_resp.append(resp)
                    data_rt.append(getTime() - t0)
                    if resp == trial[i][3]:
                        data_acc.append(1)
                    else:
                        data_acc.append(0)

                    clicked = True

            else:
                break

            win.flip()

        # remove stimuli
        stimuli[i][1].autoDraw = False
        check.autoDraw = False
        cancel.autoDraw = False
        win.flip()

        # feedback, 3000ms
        if feedback:
            if resp == trial[i][3]:
                feedback1.autoDraw = True
            else:
                feedback2.autoDraw = True

            for n in range(0, int(round(frame_rate) * 3)):
                win.flip()

            feedback1.autoDraw = False
            feedback2.autoDraw = False


# loop -----------------------------------------------------------------------------------------------------------------
instruction_page(instruction1)
SVT_game(practice, stimuli_prac, feedback=True)

# buffer, 1000 ms
for n in range(0, int(round(frame_rate) * 1)):
    win.flip()

instruction_page(instruction2)
SVT_game(exp, stimuli_exp)

# end ------------------------------------------------------------------------------------------------------------------
for n in range(0, int(round(frame_rate) * 1)):
    win.flip()

instruction3.draw()
win.flip()

# data -----------------------------------------------------------------------------------------------------------------
# get time
my_time = datetime.now()
my_time = my_time.strftime("%d%m%Y_%H%M%S")

# save as a .csv file
c = open('data/Data_SVT_{}_{}.csv'.format(sub_info['id'], my_time), 'w', encoding='utf-8', newline='')
csv_writer = writer(c)
csv_writer.writerow(['id', 'name', 'gender', 'grade', 'school',
                     'proc', 'sen_stim', 'pic_stim', 'condition', 'answer_key', 'resp', 'acc', 'rt'])  # head

for i in range(0, len(data_tasks)):
    csv_writer.writerow([
        sub_info['id'],
        sub_info['name'],
        sub_info['gender'],
        sub_info['grade'],
        sub_info['school'],
        data_tasks[i],
        data_materials[i][0],
        data_materials[i][1],
        data_materials[i][2],
        data_materials[i][3],
        data_resp[i],
        data_acc[i],
        data_rt[i]
    ])
c.close()

wait(2)
