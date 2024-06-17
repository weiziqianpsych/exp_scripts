#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Mental_rotation.py
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
from random import shuffle

# dialog ---------------------------------------------------------------------------------------------------------------
sub_info = {'id': '', 'name': '', 'gender': ['male', 'female'],
            'grade': '', 'school': ''}

inputDlg = DlgFromDict(dictionary=sub_info, title='basic information',
                       order=['id', 'name', 'gender', 'grade', 'school'])

# window ---------------------------------------------------------------------------------------------------------------
width = 1.366
height = 0.768

win = Window(
    size=(width * 1000, height * 1000),
    fullscr=False, screen=0, winType='pyglet',
    allowGUI=True, allowStencil=False, color="white",
    colorSpace='rgb', units='norm')

mouse = Mouse()

# stimuli --------------------------------------------------------------------------------------------------------------
# recording
my_sound1 = Sound("sound/sound1.wav")
my_sound2 = Sound("sound/sound2.wav")

# instruction
instruction1 = ImageStim(win, image='pic/instruction1.png', pos=(0, 0.1), size=(1.5 / width, 1.125 / height))
instruction2 = ImageStim(win, image='pic/instruction2.png', pos=(0, 0.1), size=(1.5 / width, 1.125 / height))
instruction3 = ImageStim(win, image='pic/instruction3.png', pos=(0, 0.1), size=(1.5 / width, 1.125 / height))
prompt = ImageStim(win, image='pic/prompt.png', pos=(0, 0.1), size=(1.5 / width, 1.125 / height))
feedback_correct = ImageStim(win, image='pic/feedback_correct.png', pos=(0, 0.1), size=(1.5 / width, 1.125 / height))
feedback_incorrect = ImageStim(win, image='pic/feedback_incorrect.png', pos=(0, 0.1),
                               size=(1.5 / width, 1.125 / height))

# the continue button
button_continue = ImageStim(win, image='pic/continue.png', pos=(0, -0.80), size=(0.15 / width, 0.15 / height))
rect_continue = Rect(win, size=button_continue.size * 1.2, lineWidth=10, lineColor="grey", pos=button_continue.pos)

# trials and stimuli
materials_practice = [
    ["hamburger", "Ans_135", "Mir_180", "Mir_45"],
    ["strawberry", "Mir_45", "Mir_180", "Ans_135"],
    ["airplane", "Mir_135", "Ans_90", "Mir_45"],
    ["lemonade", "Mir_90", "Mir_45", "Ans_135"]
]

material_exp = [
    ["dope", "Ans_45", "Mir_90", "Mir_135"],
    ["tanner", "Mir_180", "Ans_90", "Mir_135"],
    ["keeper", "Mir_180", "Mir_90", "Ans_135"],
    ["lawyer", "Ans_180", "Mir_45", "Mir_90"],
    ["stagecoach", "Mir_90", "Ans_45", "Mir_180"],
    ["skipper", "Mir_45", "Mir_135", "Ans_90"],
    ["codfish", "Ans_135", "Mir_45", "Mir_90"],
    ["hog", "Mir_180", "Ans_180", "Mir_45"],
    ["dugout", "Mir_90", "Mir_180", "Ans_45"],
    ["colt", "Ans_90", "Mir_45", "Mir_135"],
    ["axe", "Mir_45", "Ans_135", "Mir_90"],
    ["fairy", "Mir_135", "Mir_45", "Ans_180"],
    ["fiddle", "Ans_180", "Mir_90", "Mir_135"],
    ["fox", "Mir_90", "Ans_135", "Mir_180"],
    ["astronaut", "Mir_135", "Mir_180", "Ans_90"],
    ["pigeon", "Ans_45", "Mir_135", "Mir_180"],
    ["bamboo", "Mir_90", "Ans_180", "Mir_180"],
    ["hippo", "Mir_45", "Mir_180", "Ans_135"],
    ["dairy", "Ans_90", "Mir_135", "Mir_180"],
    ["teakettle", "Mir_135", "Ans_45", "Mir_90"],
    ["tiger", "Mir_45", "Mir_90", "Ans_180"],
    ["calf", "Ans_135", "Mir_90", "Mir_180"],
    ["castle", "Mir_135", "Ans_90", "Mir_45"],
    ["tie", "Mir_135", "Mir_90", "Ans_45"],
    ["hospital", "Ans_45", "Mir_180", "Mir_90"],
    ["bee", "Mir_45", "Ans_90", "Mir_180"],
    ["sunflower", "Mir_90", "Mir_45", "Ans_135"],
    ["peach", "Ans_180", "Mir_135", "Mir_45"],
    ["bunny", "Mir_180", "Ans_45", "Mir_135"],
    ["chocolate", "Mir_180", "Mir_45", "Ans_90"],
    ["slippers", "Ans_135", "Mir_180", "Mir_45"],
    ["comb", "Mir_45", "Ans_180", "Mir_90"],
    ["corn", "Mir_180", "Mir_135", "Ans_45"],
    ["keys", "Ans_90", "Mir_180", "Mir_45"],
    ["tomato", "Mir_180", "Ans_135", "Mir_45"],
    ["cup", "Mir_90", "Mir_135", "Ans_180"]
]

stim_prac = []  # structure: [["hamburger", "Ans_135", "Mir_180", "Mir_45"],...]
stim_exp = []
for stim in [stim_prac, stim_exp]:

    if stim == stim_prac:
        material = materials_practice
    else:
        material = material_exp

    for i in range(0, len(material)):  # number of questions
        item0 = ImageStim(win,
                          image='pic/{}.png'.format(material[i][0]),
                          name=material[i][0],
                          pos=(-0.6, 0),
                          size=(0.3/width, 0.3/height))

        item1 = ImageStim(win,
                          image='pic/{}_{}.png'.format(material[i][0], material[i][1]),
                          name=material[i][1],
                          pos=(-0.2, 0),
                          size=(0.3/width, 0.3/height))

        item2 = ImageStim(win,
                          image='pic/{}_{}.png'.format(material[i][0], material[i][2]),
                          name=material[i][2],
                          pos=(0.2, 0),
                          size=(0.3/width, 0.3/height))

        item3 = ImageStim(win,
                          image='pic/{}_{}.png'.format(material[i][0], material[i][3]),
                          name=material[i][3],
                          pos=(0.6, 0),
                          size=(0.3/width, 0.3/height))

        stim.append([item0, item1, item2, item3])

    if material == material_exp:
        shuffle(stim)  # randomising

rect = []
for item in [stim_prac[0][1], stim_prac[0][2], stim_prac[0][3]]:
    rect.append(Rect(win, size=(item.size[0]*1.2, item.size[1]*1.2), lineWidth=10, lineColor="grey",
                     fillColor=None, pos=item.pos))

# data -----------------------------------------------------------------------------------------------------------------
data_question = []
data_item1 = []
data_item2 = []
data_item3 = []
data_resp = []
data_rt = []

answer_key = []


# functions ------------------------------------------------------------------------------------------------------------
def instruction_page(instruction, my_sound):
    clicked = False

    instruction.autoDraw = True
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
            instruction.autoDraw = False
            button_continue.autoDraw = False
            rect_continue.autoDraw = False

            win.flip()

            my_sound.stop()

            wait(2)  # interval


frame_rate = win.getActualFrameRate(nIdentical=60, nMaxFrames=100, nWarmUpFrames=10, threshold=1)
frame_rate = 30


def MR_game(stim, feedback=False, key=None):
    for i in range(0, len(stim)):  # run each question

        # draw stimuli for this question
        if feedback:
            prompt.autoDraw = True
        for item in stim[i]:
            item.autoDraw = True

        t0 = getTime()
        clicked = False

        for n in range(0, int(round(frame_rate) * 600)):
            while not clicked:  # what happens in each question's interface
                # the cursor
                for x in [1, 2, 3]:  # options
                    if stim[i][x].contains(mouse.getPos()):
                        # show the border when the cursor moves in
                        if not clicked:
                            rect[x - 1].autoDraw = True

                        if mouse.isPressedIn(stim[i][x]):
                            if not clicked:
                                t1 = getTime()
                                resp = stim[i][x].name

                                rect[x - 1].autoDraw = True
                                clicked = True
                    else:
                        rect[x - 1].autoDraw = False

                if not clicked:
                    win.flip()

                else:  # get ready to move to the next question
                    # remove stimuli in this question
                    if feedback:
                        prompt.autoDraw = False
                    for item in stim[i]:
                        item.autoDraw = False
                    for item in rect:
                        item.autoDraw = False

                    if not feedback:
                        data_rt.append(t1 - t0)
                        data_question.append(stim[i][0].name)
                        data_item1.append(stim[i][1].name)
                        data_item2.append(stim[i][2].name)
                        data_item3.append(stim[i][3].name)
                        data_resp.append(resp)

                    win.flip()
                    wait(0.5)  # 500ms interval

                    # feedback
                    if feedback:
                        if resp[0:3] == "Ans":
                            feedback_correct.draw()
                            for item in stim[i]:
                                item.draw()
                            rect[key[i]].draw()
                        else:
                            feedback_incorrect.draw()
                            for item in stim[i]:
                                item.draw()
                            rect[key[i]].draw()
                        win.flip()
                        wait(1.5)


# loop -----------------------------------------------------------------------------------------------------------------
instruction_page(instruction1, my_sound1)
MR_game(stim_prac, feedback=True, key=[0, 2, 1, 2])
instruction_page(instruction2, my_sound2)
MR_game(stim_exp)

# end ------------------------------------------------------------------------------------------------------------------
instruction3.draw()
win.flip()

# accuracy -------------------------------------------------------------------------------------------------------------
data_acc = []
for i in range(0, len(data_resp)):
    if data_resp[i][0:3] == "Ans":
        data_acc.append(1)
    else:
        data_acc.append(0)

# data -----------------------------------------------------------------------------------------------------------------
# get time
my_time = datetime.now()
my_time = my_time.strftime("%d%m%Y_%H%M%S")

# save as a .csv file
c = open('data/Data_Mental_rotation_{}_{}.csv'.format(sub_info['id'], my_time), 'w', encoding='utf-8', newline='')
csv_writer = writer(c)
csv_writer.writerow(['id', 'name', 'gender', 'grade', 'school',
                     'question', 'item 1', 'item 2', 'item 3',
                     'resp', 'acc', 'rt'])  # head
for i in range(0, len(data_question)):
    csv_writer.writerow([
        sub_info['id'],
        sub_info['name'],
        sub_info['gender'],
        sub_info['grade'],
        sub_info['school'],
        data_question[i],
        data_item1[i],
        data_item2[i],
        data_item3[i],
        data_resp[i],
        data_acc[i],
        data_rt[i]
    ])
c.close()

wait(2)
