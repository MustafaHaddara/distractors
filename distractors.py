#!/usr/local/bin/python
# testing distractors
# todo distractors on the side

# stdlib imports
import os
import random
import sys
import time

# external lib imports
# import numpy as np
import pygame

# event type constants
from pygame import KEYDOWN, KEYUP, QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP

# allowed key constants
from pygame import K_ESCAPE, K_RETURN, K_SPACE

# for text input
# taken from http://www.pygame.org/project-EzText-920-.html
import eztext

WINDOW_HEIGHT = 900
WINDOW_WIDTH = 1440

TIME_TO_SHOW = 1000

MAIN_TEXT = None
SIDE_TEXT = None
SIDE_COLOR = None

WINDOW = None
FONT = None
MSG = ''

ORDER = []
MAX_LEN = 4

DIST_TEXT = 1
DIST_RECT = 2

DISTRACTOR_DESCRIPTIONS = {
    0: 'No Distractor',
    DIST_TEXT: 'Text Distractor',
    DIST_RECT: 'Rect Distractor'
}

DISTRACTOR = 0

outputfile = open('data.csv', 'w')
outputfile.write('expected, entered, time, distractor type, success\n')

def draw_text(t=None):
    length = 0
    if t is None:
        length = ORDER.pop()
        text = genRandString(length)
        distractor(DISTRACTOR, length)
    else:
        text = t
    print DISTRACTOR
    text_obj = FONT.render(text, True, pygame.Color('#000000'))
    pos = text_obj.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
    WINDOW.blit(text_obj, pos)
    return text

def genRandString(l):
    return ''.join([chr(random.randint(65,90)) for _ in range(l)])

def distractor(t, l=0):
    if t is None:
        return
    elif t == DIST_TEXT:
        text = genRandString(l)
        text_obj = FONT.render(text, True, pygame.Color('#000000'))
        text_pos = text_obj.get_rect()
        pos = (0, WINDOW_HEIGHT/2 - text_pos.height/2)
        WINDOW.blit(text_obj, pos)
    elif t == DIST_RECT:
        height = 50
        width = 150
        top = WINDOW_HEIGHT/2 - (height/2)
        WINDOW.fill(color=pygame.Color('#00FF00'), rect=pygame.Rect(0, top, width, height))

def clear_window():
    WINDOW.fill(color=pygame.Color('white'))

def check_text(time, expected_text):
    entered = INPUT_BOX.value.upper()
    outputfile.write('%s,%s,%s,%s,%s\n' % (expected_text, entered, time, DISTRACTOR_DESCRIPTIONS[DISTRACTOR], entered==expected_text))
    INPUT_BOX.value = ''

def init():
    global WINDOW, FONT, INPUT_BOX
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Distractors')
    pygame.init()    
    WINDOW.fill(color=pygame.Color('white'))

    FONT = pygame.font.SysFont('Arial', size=72)

    INPUT_BOX = eztext.Input(maxlength=9, font=FONT, prompt='enter the text: ')
    init_ordering()

def init_ordering():
    global ORDER
    ORDER = range(3, MAX_LEN+1)
    random.shuffle(ORDER)

def main():
    global ORDER, DISTRACTOR
    init()
    set_timer = False
    draw_box = False
    started = False
    TEXT_TIMER_EVENT = pygame.USEREVENT
    CLEAR_TIMER_EVENT = pygame.USEREVENT + 1
    clock = pygame.time.Clock()
    start = 0
    message = ''
    draw_text('Press space to start')
    while True:
        if set_timer:
            # 3 - 5 seconds
            if len(ORDER) == 0:
                DISTRACTOR += 1
                init_ordering()
                if DISTRACTOR not in DISTRACTOR_DESCRIPTIONS:
                    quit()
            time_to_text = random.randint(3000, 5000)
            time_to_clear = time_to_text + TIME_TO_SHOW
            pygame.time.set_timer(TEXT_TIMER_EVENT, time_to_text)
            pygame.time.set_timer(CLEAR_TIMER_EVENT, time_to_clear)
            set_timer = False

        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
                if event.key == K_RETURN:
                    check_text(pygame.time.get_ticks() - start, message)
                    clear_window()
                    set_timer = True
                    draw_box = False
                if event.key == K_SPACE and not started:
                    set_timer = True
                    started = True
                    clear_window()

            if event.type == TEXT_TIMER_EVENT:
                pygame.time.set_timer(TEXT_TIMER_EVENT, 0)
                message = draw_text()

            if event.type == CLEAR_TIMER_EVENT:
                pygame.time.set_timer(CLEAR_TIMER_EVENT, 0)
                clear_window()
                start = pygame.time.get_ticks()
                draw_box = True
                INPUT_BOX.value = ''
            if event.type == QUIT:
                quit()

        INPUT_BOX.update(events)

        if draw_box:
            INPUT_BOX.draw(WINDOW)

        pygame.display.flip()
        clock.tick(120)


def quit():
    outputfile.close()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
