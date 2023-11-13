#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 13 Nov 2023

@author: Mikhail Stolpovskiy mikhail.stolpovsky@gmail.com
"""

import pygame
#import game_state
#import os
#import player
from math import sin, cos, pi
from random import randint

# Color definition
BKG = (20, 9, 5)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (173, 159, 52)
RED = (255, 0, 0)
PAPER = (246,238,227)


# Copied from 
# https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame
def blit_text(surface, text, rect, font, color=pygame.Color('black')):
    words = text
    space = font.size(' ')[0]  # The width of a space.
    x, y, max_width, max_height = rect
    word_width, word_height = 0., 0.
    for line in words.split('\n'):
        for word in line.split(' '):
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= rect[0] + max_width:
                x = rect[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = rect[0]  # Reset the x.
        y += word_height  # Start on new row.        


# Read questions from file
with open('questions.txt', 'r') as f:
    questions = f.read()
    questions = questions.split('\n\n\n')

pygame.init()
pygame.font.init()
questionfont = pygame.font.SysFont('Arial', 30)
timerfont = pygame.font.SysFont('Arial', 70)


# Set up the drawing window
width = 1400
height = 800
logo_size = (400, 300)
screen = pygame.display.set_mode([width, height], pygame.RESIZABLE)

# Import logo
logo = pygame.image.load("logo.png")
logo = pygame.transform.scale(logo, logo_size)

# Import spinning top image
top = pygame.image.load('top.png')
top = pygame.transform.scale(top, (100, 100))

# Some variables that store the current state of the game
number_of_questions = len(questions)
rot = 0. # rotation angle of the arrow
rotating = False
question = 0
show_question = False
show_answer = False
asked_questions = []
nrounds = 0
time = 0
time_init = 3
fps = 30
timer_coord = (700, 620)
start_timer = False
question_box = (650, 50, 600, 550)

# Clock to set the FPS
clock = pygame.time.Clock()

# Run until the user asks to quit
running = True

# main game loop
while running:
    dt = clock.tick(fps)
    # Fill the background with dark brown
    screen.fill(BKG)

    pygame.draw.rect(screen, PAPER,
                     pygame.Rect(question_box[0],
                                 question_box[1],
                                 question_box[2],
                                 question_box[3]))
    
    # Draw logo
    screen.blit(logo, (0, 0))
    
    # Draw circle with sections
    center = (350, 450)
    pygame.draw.circle(screen, BLACK, center, 250)
    pygame.draw.circle(screen, GOLD, center, 250, 5)
    for sector in range(number_of_questions):
        ang = sector / number_of_questions * 2 * pi
        pygame.draw.line(screen, GOLD, center, 
                         (center[0] + 250 * cos(ang),
                          center[1] + 250 * sin(ang)), 5)     
    
    # Draw rotating arrow
    if rotating:
        rot += 0.005 * dt
        if rot / 2 / pi > 1:
            rot -= 2 * pi
            nrounds -= 1
        if nrounds <= 0 and \
           abs(rot - (question + 0.5) / number_of_questions * 2 * pi) < 0.1:
            rotating = False
            show_question = True
            time = time_init
            
    pygame.draw.polygon(screen, RED, [[center[0] + 5 * cos(rot + pi/2),
                                       center[1] + 5 * sin(rot + pi/2)],
                                      [center[0] + 5 * cos(rot - pi/2),
                                       center[1] + 5 * sin(rot - pi/2)],
                                      [center[0] + 200 * cos(rot),
                                       center[1] + 200 * sin(rot)]])
    # Draw spinning top
    screen.blit(top, (300, 400))
    
    # Show question
    if show_question:
        text = questions[question].split('\n')
        for i in range(len(text)):
            if text[i][:6] == 'Вопрос':
                text = text[i]
                break
        blit_text(screen, text, (question_box[0] + 20, 
                                 question_box[1] + 20,
                                 question_box[2] - 40,
                                 question_box[3] - 40),
                  questionfont)
        # Show timer
        timer = f'{time:.2f}'
        textsurface = timerfont.render(timer, True, RED)
        screen.blit(textsurface, timer_coord)
        
        if start_timer:
            time -= dt / 1000
            if time <= 0:
                time = 0.
                start_timer = False
                
    # Show answer
    if show_answer:
        text = questions[question]
        blit_text(screen, text, (question_box[0] + 20, 
                                 question_box[1] + 20,
                                 question_box[2] - 40,
                                 question_box[3] - 40),
                  questionfont)
        asked_questions.append(question)
            
    
    
    # Listen to events
    for event in pygame.event.get():
        # Did the user click the window close button?
        if event.type == pygame.QUIT:
            running = False

        # Did the user resize the window?            
        elif event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            screen = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
            width = event.w
            height = event.h
            
        # Click listener
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            
            # Did the user click on the spinning top?
            if not rotating and \
               abs(pos[0] - center[0]) < 50 and \
               abs(pos[1] - center[1]) < 50:
                rot = 0.
                rotating = True
                while True:
                    question = randint(0, number_of_questions - 1)
                    if question not in asked_questions:
                        break
                nrounds = randint(2, 4)
                show_question = False
                show_answer = False
                start_timer = False

            # Did the user click on the timer?
            if show_question and \
               pos[0] > timer_coord[0] and \
               pos[0] < timer_coord[0] + 100 and \
               pos[1] > timer_coord[1] and \
               pos[1] < timer_coord[1] + 100:
                start_timer = True
                time = time_init
                
            # Did user click on the question box?
            if show_question and time == 0. and \
               pos[0] > question_box[0] and \
               pos[0] < question_box[0] + question_box[2] and \
               pos[1] > question_box[1] and \
               pos[1] < question_box[1] + question_box[3]:
                show_answer = True
                show_question = False
        
                
            
    pygame.display.update()
                

# Done! Time to quit.
pygame.quit()
