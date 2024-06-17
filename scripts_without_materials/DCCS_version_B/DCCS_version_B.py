#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    DCCS_version_A/B.py
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
# recording
sound_CIns = Sound("sound/CIns.wav")
sound_CTip = Sound("sound/ColorIns.wav")
sound_C1true = Sound("sound/CP1R.wav")
sound_C1false = Sound("sound/CP1W.wav")
sound_C2true = Sound("sound/CP2R.wav")
sound_C2false = Sound("sound/CP2W.wav")

sound_SIns = Sound("sound/SIns.wav")
sound_STip = Sound("sound/ShapeIns.wav")
sound_S1true = Sound("sound/SP1R.wav")
sound_S1false = Sound("sound/SP1W.wav")
sound_S2true = Sound("sound/SP2R.wav")
sound_S2false = Sound("sound/SP2W.wav")

sound_MIns = Sound("sound/MIns.wav")
sound_MTip = Sound("sound/MixIns.wav")
sound_M1true = Sound("sound/MP1R.wav")
sound_M1false = Sound("sound/MP1W.wav")
sound_M2true = Sound("sound/MP2R.wav")
sound_M2false = Sound("sound/MP2W.wav")

sound_go = Sound("sound/PracEnd.wav")

# instruction
instruction1 = ImageStim(win, image='pic/instruction1.png', pos=(0, 0.1), size=(1.5/width, 1.125/height))
instruction2 = ImageStim(win, image='pic/instruction2.png', pos=(0, 0.1), size=(1.5/width, 1.125/height))
instruction3 = ImageStim(win, image='pic/instruction3.png', pos=(0, 0.1), size=(1.5/width, 1.125/height))
instruction4 = ImageStim(win, image='pic/instruction4.png', pos=(0, 0.1), size=(1.5/width, 1.125/height))
instruction_start = ImageStim(win, image='pic/instruction_start.png', pos=(0, 0.1), size=(1.5/width, 1.125/height))

# the continue button
button_continue = ImageStim(win, image='pic/continue.png', pos=(0, -0.80), size=(0.15/width, 0.15/height))
rect_continue = Rect(win, size=button_continue.size*1.2, lineWidth=10, lineColor="grey", pos=button_continue.pos)

# all items
my_size = (0.406*1.5/width, 0.265*1.5/height)
my_pos = (0, 0.45)
rabbit = ImageStim(win, image='pic/rabbit.png', name='rabbit', pos=my_pos, size=my_size)
boat = ImageStim(win, image='pic/boat.png', name='boat', pos=my_pos, size=my_size)
rabbit_border = ImageStim(win, image='pic/rabbit_border.png', name='rabbit_border', pos=my_pos, size=my_size)
boat_border = ImageStim(win, image='pic/boat_border.png', name='boat_border', pos=my_pos, size=my_size)
target1 = ImageStim(win, image='pic/target1.png', name='target1', pos=(-0.5, -0.45), size=my_size)
target2 = ImageStim(win, image='pic/target2.png', name='target2', pos=(0.5, -0.45), size=my_size)
finger1 = ImageStim(win, image='pic/finger.png', pos=(-0.5, -0.80), size=(0.1/width, 0.1/height))
finger2 = ImageStim(win, image='pic/finger.png', pos=(0.5, -0.80), size=(0.1/width, 0.1/height))

# trial order of the colour game
colour_game_practice = [
    [boat, target1],  # [the question, the correct answer]
    [rabbit, target2],
]
colour_game = [
    [rabbit, target2],
    [boat, target1],
    [boat, target1],
    [rabbit, target2],
    [boat, target1],
    [rabbit, target2],
]

# trial order of the shape game
shape_game_practice = [
    [boat, target2],
    [rabbit, target1]
]
shape_game = [
    [rabbit, target1],
    [boat, target2],
    [rabbit, target1],
    [boat, target2],
    [boat, target2],
    [rabbit, target1]
]

# trial order of the shape game
mixed_game_practice = [
    [rabbit, target1],
    [rabbit_border, target2]
]
mixed_game = [
    [rabbit_border, target2],
    [boat_border, target1],
    [boat, target2],
    [rabbit, target1],
    [boat_border, target1],
    [rabbit, target1],
    [rabbit, target1],
    [rabbit_border, target2],
    [rabbit_border, target2],
    [boat, target2],
    [rabbit_border, target2],
    [boat_border, target1]
]

# data -----------------------------------------------------------------------------------------------------------------
data_question = []
data_answer_key = []
data_resp = []
data_rt = []
data_acc = []
data_task = []

# function -------------------------------------------------------------------------------------------------------------
frame_rate = win.getActualFrameRate(nIdentical=60, nMaxFrames=100, nWarmUpFrames=10, threshold=1)
frame_rate = 30


def instruction_page(instruction_imagestim, sound_Ins):

    clicked = False

    target1.autoDraw = False
    target2.autoDraw = False
    instruction_imagestim.autoDraw = True
    button_continue.autoDraw = True
    rect_continue.autoDraw = True

    sound_Ins.play()

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
            instruction_imagestim.autoDraw = False
            button_continue.autoDraw = False
            rect_continue.autoDraw = False

            win.flip()

            sound_Ins.stop()

            wait(0.5)  # interval


def game_page(trial_list,
              sound_Tip,
              sound_1true,
              sound_1false,
              sound_2true,
              sound_2false,
              feedback=False):

    for i in range(0, len(trial_list)):  # run each question

        # recording
        target1.draw()
        target2.draw()
        win.flip()
        sound_Tip.play()
        wait(sound_Tip.getDuration())
        win.flip()

        total_dis = target1.pos[1] - trial_list[i][0].pos[1]
        t0 = getTime()
        dragged = False
        clicked = False

        # draw stimuli for this question
        # item_central.pos = trial_list[i][0].pos
        target1.autoDraw = True
        target2.autoDraw = True
        trial_list[i][0].autoDraw = True  # the question

        for n in range(0, round(frame_rate) * 600):

            while not dragged:
                if target1.contains(mouse.getPos()):
                    finger1.draw()

                if target2.contains(mouse.getPos()):
                    finger2.draw()

                if mouse.isPressedIn(target1) or mouse.isPressedIn(target2):

                    for z in range(0, int(round(frame_rate) * 0.3)):  # animation
                        if mouse.isPressedIn(target1):
                            finger1.pos = (-0.5, finger1.pos[1] + 0.001)
                            finger1.autoDraw = True
                            resp = target1.name
                        if mouse.isPressedIn(target2):
                            finger2.pos = (0.5, finger2.pos[1] + 0.001)
                            finger2.autoDraw = True
                            resp = target2.name
                        win.flip()
                    finger1.pos = (-0.5, -0.80)
                    finger2.pos = (0.5, -0.80)

                    if not feedback:
                        data_resp.append(resp)
                        data_rt.append(getTime() - t0)
                        data_task.append(task)
                        data_question.append(trial_list[i][0].name)
                        data_answer_key.append(trial_list[i][1].name)
                        if resp == data_answer_key[-1]:
                            data_acc.append(1)
                        else:
                            data_acc.append(0)

                    win.flip()

                    break

                if not dragged:
                    win.flip()

            # remove stimuli
            if feedback:
                target1.autoDraw = False
                target2.autoDraw = False
            trial_list[i][0].autoDraw = False  # the question
            trial_list[i][0].pos = my_pos
            finger1.autoDraw = False
            finger2.autoDraw = False

            win.flip()
            wait(0.5)

            # feedback
            if feedback:
                trial_list[i][0].pos = my_pos
                trial_list[i][0].draw()  # the question
                trial_list[i][1].draw()  # the answer key
                win.flip()
                # recording
                if resp == trial_list[i][1].name and i == 0:
                    sound_1true.play()
                    wait(sound_1true.getDuration())
                elif resp != trial_list[i][1].name and i == 0:
                    sound_1false.play()
                    wait(sound_1false.getDuration())
                elif resp == trial_list[i][1].name and i == 1:
                    sound_2true.play()
                    wait(sound_2true.getDuration())
                elif resp != trial_list[i][1].name and i == 1:
                    sound_2false.play()
                    wait(sound_2false.getDuration())

            win.flip()
            wait(0.5)

            break


# loop -----------------------------------------------------------------------------------------------------------------
# the shape game
task = "shape"
instruction_page(instruction2, sound_SIns)
game_page(shape_game_practice, sound_STip, sound_S1true, sound_S1false, sound_S2true, sound_S2false, feedback=True)
instruction_page(instruction_start, sound_go)
game_page(shape_game, sound_STip, sound_S1true, sound_S1false, sound_S2true, sound_S2false)

# the colour game
task = "colour"
instruction_page(instruction1, sound_CIns)
game_page(colour_game_practice, sound_CTip, sound_C1true, sound_C1false, sound_C2true, sound_C2false, feedback=True)
instruction_page(instruction_start, sound_go)
game_page(colour_game, sound_CTip, sound_C1true, sound_C1false, sound_C2true, sound_C2false)

# the mixed game
task = "mixed"
instruction_page(instruction3, sound_MIns)
game_page(mixed_game_practice, sound_MTip, sound_M1true, sound_M1false, sound_M2true, sound_M2false, feedback=True)
instruction_page(instruction_start, sound_go)
game_page(mixed_game, sound_MTip, sound_M1true, sound_M1false, sound_M2true, sound_M2false)

# end ------------------------------------------------------------------------------------------------------------------
target1.autoDraw = False
target2.autoDraw = False

instruction4.draw()
win.flip()

# data -----------------------------------------------------------------------------------------------------------------
# get time
my_time = datetime.now()
my_time = my_time.strftime("%d%m%Y_%H%M%S")

# save as a .csv file
c = open('data/Data_DCCS_versionB_{}_{}.csv'.format(sub_info['id'], my_time), 'w', encoding='utf-8', newline='')
csv_writer = writer(c)
csv_writer.writerow(['id', 'name', 'gender', 'grade', 'school',
                     'task', 'question', 'resp', 'acc', 'rt'])  # head
for i in range(0, len(data_question)):
    csv_writer.writerow([
        sub_info['id'],
        sub_info['name'],
        sub_info['gender'],
        sub_info['grade'],
        sub_info['school'],
        data_task[i],
        data_question[i],
        data_resp[i],
        data_acc[i],
        data_rt[i]
    ])
c.close()

wait(2)
