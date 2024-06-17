#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Visual_perception.py
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
# from psychopy.sound import Sound
from psychopy.event import Mouse, getKeys
from psychopy.core import wait, getTime, quit

from datetime import datetime
from csv import writer
from os import path, listdir

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
instruction1 = ImageStim(win, image='pic/instruction1.png', pos=(0, 0.1), size=(1.5/width, 1.125/height))
instruction_start = ImageStim(win, image='pic/instruction_start.png', pos=(0, 0.1), size=(1.5/width, 1.125/height))
instruction_end = ImageStim(win, image='pic/instruction_end.png', pos=(0, 0.1), size=(1.5/width, 1.125/height))

s3_q1_feedback = ImageStim(win, image='pic/s3_q1_feedback.png', pos=(0, 0.1), size=(1.5/width, 1.125/height))
s3_q2_feedback = ImageStim(win, image='pic/s3_q2_feedback.png', pos=(0, 0.1), size=(1.5/width, 1.125/height))
s4_q1_feedback = ImageStim(win, image='pic/s4_q1_feedback.png', pos=(0, 0.1), size=(1.5/width, 1.125/height))
s4_q2_feedback = ImageStim(win, image='pic/s4_q2_feedback.png', pos=(0, 0.1), size=(1.5/width, 1.125/height))
s5_q1_feedback = ImageStim(win, image='pic/s5_q1_feedback.png', pos=(0, 0.1), size=(1.5/width, 1.125/height))
s5_q2_feedback = ImageStim(win, image='pic/s5_q2_feedback.png', pos=(0, 0.1), size=(1.5/width, 1.125/height))

# the continue button
button_continue = ImageStim(win, image='pic/continue.png', pos=(0, -0.8), size=(0.15/width, 0.15/height))
rect_continue = Rect(win, size=button_continue.size*1.2, lineWidth=10, lineColor="grey", pos=button_continue.pos)

# another continue buttons (in the question pages)
button_go = ImageStim(win, image='pic/continue.png', pos=(0.8, -0.8), size=(0.15/width, 0.15/height))
rect_go = Rect(win, size=button_go.size*1.2, lineWidth=10, lineColor="grey", pos=button_go.pos)

# the position
initial_pos3 = [(-0.25, -0.5), (0.0, -0.5), (0.25, -0.5)]
initial_pos4 = [(-0.375, -0.5), (-0.125, -0.5), (0.125, -0.5), (0.375, -0.5)]
initial_pos5 = [(-0.5, -0.5), (-0.25, -0.5), (0.0, -0.5), (0.25, -0.5), (0.5, -0.5)]
initial_pos6 = [(-0.525, -0.5), (-0.375, -0.5), (-0.125, -0.5), (0.125, -0.5), (0.375, -0.5), (0.625, -0.5)]
initial_pos7 = [(-0.75, -0.5), (-0.5, -0.5), (-0.25, -0.5), (0.0, -0.5), (0.25, -0.5), (0.5, -0.5), (0.75, -0.5)]
initial_pos8 = [(-0.875, -0.5), (-0.625, -0.5), (-0.375, -0.5), (-0.125, -0.5), (0.125, -0.5), (0.375, -0.5), (0.625, -0.5), (0.875, -0.5)]

sections = []
parent_folder = "pic"
subfolders = ["S3", "S4", "S5"]
for subfolder in subfolders:

    subfolder_path = path.join(parent_folder, subfolder)

    # lists
    questions = []
    items = []

    # get picture names
    for file_name in listdir(subfolder_path):

        if ".DS_Store" not in file_name:
            file_path = path.join(subfolder_path, file_name)

            items_for_this_question = []
            for item_folder in listdir(file_path):
                item_folder_path = path.join(file_path, item_folder)
                if ".DS_Store" not in item_folder_path:
                    if "item" not in item_folder_path[-9:-1]:
                        questions.append(item_folder_path)  # item_folder_path
                    else:
                        items_for_this_question.append(item_folder_path)  # item_folder_path
                items_for_this_question.sort()

            items.append(items_for_this_question)

    questions.sort()
    items.sort()

    if [] in items:
        items.remove([])

    # Open a file in write mode
    with open('output_quest_'+subfolder+'.txt', 'w') as file:
        # Iterate over the list elements
        for item in questions:
            # Write each element to a new line in the file
            file.write(str(item) + '\n')
    with open('output_items_'+subfolder+'.txt', 'w') as file:
        # Iterate over the list elements
        for item in items:
            # Write each element to a new line in the file
            file.write(str(item) + '\n')

    # create stimuli for this section
    stim_questions = []
    stim_items = []
    for quest_name in questions:
        # question
        stim_questions.append(ImageStim(win,
                                        image=quest_name,
                                        name=quest_name,
                                        pos=(0, 0.3),
                                        size=(0.5/width, 0.5/height)))
    for items_for_each_question in items:
        stim_some_items = []

        # position
        for initial_pos in [initial_pos3, initial_pos4, initial_pos5, initial_pos6, initial_pos7, initial_pos8]:
            if len(initial_pos) == len(items_for_each_question):
                my_pos = initial_pos

        # item
        for i in range(0, len(items_for_each_question)):
            stim_some_items.append(ImageStim(win,
                                             image=items_for_each_question[i],
                                             name=items_for_each_question[i],
                                             pos=my_pos[i],
                                             size=(0.2/width, 0.2/height)))

        stim_items.append(stim_some_items)

    sections.append([stim_questions, stim_items])

# distribute stimuli
quest_s3_prac = sections[0][0][:2]
stim_s3_prac = sections[0][1][:2]
quest_s3_exp = sections[0][0][2:]
stim_s3_exp = sections[0][1][2:]

quest_s4_prac = sections[1][0][:2]
stim_s4_prac = sections[1][1][:2]
quest_s4_exp = sections[1][0][2:]
stim_s4_exp = sections[1][1][2:]

quest_s5_prac = sections[2][0][:2]
stim_s5_prac = sections[2][1][:2]
quest_s5_exp = sections[2][0][2:]
stim_s5_exp = sections[2][1][2:]

# rect
rect3 = []  # rectangles for each question
rect4 = []
rect5 = []
rect6 = []
rect7 = []
rect8 = []
for j in range(0, len(initial_pos3)):
    rect3.append(Rect(win, size=(0.2*1.2/width, 0.2*1.2/height), lineWidth=10,
                      lineColor="grey", fillColor=None, pos=initial_pos3[j]))
for j in range(0, len(initial_pos4)):
    rect4.append(Rect(win, size=(0.2*1.2/width, 0.2*1.2/height), lineWidth=10,
                      lineColor="grey", fillColor=None, pos=initial_pos4[j]))
for j in range(0, len(initial_pos5)):
    rect5.append(Rect(win, size=(0.2*1.2/width, 0.2*1.2/height), lineWidth=10,
                      lineColor="grey", fillColor=None, pos=initial_pos5[j]))
for j in range(0, len(initial_pos6)):
    rect6.append(Rect(win, size=(0.2*1.2/width, 0.2*1.2/height), lineWidth=10,
                      lineColor="grey", fillColor=None, pos=initial_pos6[j]))
for j in range(0, len(initial_pos7)):
    rect7.append(Rect(win, size=(0.2*1.2/width, 0.2*1.2/height), lineWidth=10,
                      lineColor="grey", fillColor=None, pos=initial_pos7[j]))
for j in range(0, len(initial_pos8)):
    rect8.append(Rect(win, size=(0.2*1.2/width, 0.2*1.2/height), lineWidth=10,
                      lineColor="grey", fillColor=None, pos=initial_pos8[j]))
all_rect = [rect3, rect4, rect5, rect6, rect7, rect8]

# data -----------------------------------------------------------------------------------------------------------------
data_quest = []
data_resp = []
data_rt = []

answer_key = []


# function ----------------------------------------------------------------------------------------------------------
def instruction_page(instruction):

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


frame_rate = win.getActualFrameRate(nIdentical=60, nMaxFrames=100, nWarmUpFrames=10, threshold=1)
frame_rate = 30


def VP_game(quests, stims, feedback=False, section_index=None):

    for i in range(0, len(quests)):  # run each question

        resp = set()  # multiple choices

        # draw stimuli for this question
        quests[i].autoDraw = True
        for stim in stims[i]:
            stim.autoDraw = True
        rect = all_rect[len(stims[i]) - 3]
        # button_go.autoDraw = False
        # rect_go.autoDraw = False
        button_go.autoDraw = True

        # rect_visible = False

        t_click = getTime()  # buffer = 200 ms (don't detecting mouse clicks after one click has been done for 200 ms)
        t0 = getTime()
        clicked = False

        for n in range(0, int(round(frame_rate) * 600)):
            while not clicked:
                # animation of the items
                for stim in stims[i]:
                    if mouse.getPressed()[0] and stim.contains(mouse):
                        if getTime() - t_click > 0.2:
                            if stim.name not in resp:
                                resp.add(stim.name)
                                rect[stims[i].index(stim)].autoDraw = True
                            else:
                                resp.discard(stim.name)
                                rect[stims[i].index(stim)].autoDraw = False
                        t_click = getTime()  # record the time of this click

                # animation of the continue button
                if button_go.autoDraw and not resp:  # show the button when at least one item is selected
                    button_go.autoDraw = False
                elif not button_go.autoDraw and resp:
                    button_go.autoDraw = True
                if button_go.autoDraw:
                    if button_go.contains(mouse.getPos()):
                        rect_go.autoDraw = True
                    else:
                        rect_go.autoDraw = False
                    if mouse.isPressedIn(button_go):
                        t1 = getTime()
                        clicked = True

                if not clicked:
                    # print(resp)
                    win.flip()
                    wait(0.001)

                else:  # get ready to move to the next question

                    # remove stimuli in this question
                    quests[i].autoDraw = False
                    for x in range(0, len(stims[i])):
                        stims[i][x].autoDraw = False
                        rect[x].autoDraw = False
                    button_go.autoDraw = False
                    rect_go.autoDraw = False

                    # record
                    data_quest.append(quests[i].name)
                    data_rt.append(t1 - t0)
                    data_resp.append(resp)

                    win.flip()
                    wait(0.5)  # 500ms interval

                    # feedback, 3000ms
                    if feedback:
                        if section_index == "s3":
                            if i == 0:
                                s3_q1_feedback.autoDraw = True
                            elif i == 1:
                                s3_q2_feedback.autoDraw = True
                        if section_index == "s4":
                            if i == 0:
                                s4_q1_feedback.autoDraw = True
                            elif i == 1:
                                s4_q2_feedback.autoDraw = True
                        if section_index == "s5":
                            if i == 0:
                                s5_q1_feedback.autoDraw = True
                            elif i == 1:
                                s5_q2_feedback.autoDraw = True

                        for n in range(0, int(round(frame_rate) * 3)):
                            win.flip()

                        s3_q1_feedback.autoDraw = False
                        s3_q2_feedback.autoDraw = False
                        s4_q1_feedback.autoDraw = False
                        s4_q2_feedback.autoDraw = False
                        s5_q1_feedback.autoDraw = False
                        s5_q2_feedback.autoDraw = False

                        win.flip()
                        wait(0.5)  # 500ms interval


# loop -----------------------------------------------------------------------------------------------------------------
instruction_page(instruction1)
VP_game(quest_s3_prac, stim_s3_prac, feedback=True, section_index="s3")
instruction_page(instruction_start)
VP_game(quest_s3_exp, stim_s3_exp)

instruction_page(instruction1)
VP_game(quest_s4_prac, stim_s4_prac, feedback=True, section_index="s4")
instruction_page(instruction_start)
VP_game(quest_s4_exp, stim_s4_exp)

instruction_page(instruction1)
VP_game(quest_s5_prac, stim_s5_prac, feedback=True, section_index="s5")
instruction_page(instruction_start)
VP_game(quest_s5_exp, stim_s5_exp)

# end ------------------------------------------------------------------------------------------------------------------
instruction_end.draw()
win.flip()

# data -----------------------------------------------------------------------------------------------------------------
# get time
my_time = datetime.now()
my_time = my_time.strftime("%d%m%Y_%H%M%S")

# save as a .csv file
c = open('data/Data_Visual_perception_{}_{}.csv'.format(sub_info['id'], my_time), 'w', encoding='utf-8', newline='')
csv_writer = writer(c)
csv_writer.writerow(['id', 'name', 'gender', 'grade', 'school', 'question', 'resp', 'rt'])  # head
for i in range(0, len(data_quest)):
    csv_writer.writerow([
        sub_info['id'],
        sub_info['name'],
        sub_info['gender'],
        sub_info['grade'],
        sub_info['school'],
        data_quest[i],
        data_resp[i],
        data_rt[i]
    ])
c.close()

wait(2)
