# POKE THE DOTS VERSION 5
# This is a graphical frame where two dots move around the screen, bouncing off the edges.

# HOW TO RUN-
# keep this file and uagame.py file (module from course) in the same folder with .py extension
# open cmd, navigate to the folder in which you have saved the file
# type this command- 
# python pokev5.py
# voila!

# INSTRUCTIONS-
# This is a graphical frame where two dots move around the screen, bouncing off the edges.
# The goal is to not let the two dots collide 
# When mouse button is pressed(with cursor within the screen) the dots are teleported to random locations.
# Each time the dots are about to collide click and teleport them to different locations.
# Score is time based. The longer you survived, the greater the score
# Goodluck !

from uagame import Window
from random import randint
from math import sqrt
from pygame.time import Clock, get_ticks
from pygame.event import get as get_events
from pygame import QUIT, Color, MOUSEBUTTONUP
from pygame.draw import circle as draw_circle

def main():
    game = Game()
    game.play()

class Game:
    def __init__(self):
        self._window = Window("Poke the Dots", 500, 400)
        self._adjust_window()
        self._frame_rate = 90 
        self._close_selected = False
        self._clock = Clock()
        self._small_dot = Dot('red', [50,75], 30, [1,2], self._window)
        self._big_dot = Dot('blue', [200,100], 40, [2,1], self._window)
        self._small_dot.randomize()
        self._big_dot.randomize()
        self._score = 0   
        self._continue_game = True
    def _adjust_window(self):
        self._window.set_font_name('ariel')
        self._window.set_font_size(64)
        self._window.set_font_color('white')
        self._window.set_bg_color("black")   
    def play(self):
        while not self._close_selected:
            self.handle_events()
            self.draw()
            self.update()
        self._window.close()
    def handle_events(self):
        event_list = get_events()
        for event in event_list:
            self.handle_one_event(event)
    def handle_one_event(self, event):
        if event.type ==  QUIT:
            self._close_selected = True
        elif event.type ==MOUSEBUTTONUP:
            self.handle_mouse_up(event)
    def handle_mouse_up(self, event):
        self._small_dot.randomize()
        self._big_dot.randomize()
    def draw(self):
        self._window.clear()
        self.draw_score()
        self._small_dot.draw()
        self._big_dot.draw()
        if not self._continue_game:  # perform game over actions
            self.draw_game_over()        
        self._window.update()        
    def update(self):
        if self._continue_game:
            self._small_dot.move()
            self._big_dot.move()
            self._score = get_ticks() // 1000 
        self._clock.tick(self._frame_rate)
        if self._small_dot.intersects(self._big_dot):
            self._continue_game = False
    def draw_game_over(self):
        string = 'GAME OVER'
        font_color = self._small_dot.get_color()
        bg_color = self._big_dot.get_color()
        original_font_color = self._window.get_font_color()
        original_bg_color = self._window.get_bg_color()
        self._window.set_font_color(font_color)
        self._window.set_bg_color(bg_color)
        height = self._window.get_height() - self._window.get_font_height()
        self._window.draw_string(string, 0, height)
        self._window.set_font_color(original_font_color)
        self._window.set_bg_color(original_bg_color)        
        
    def draw_score(self):
        string = "Score" + str(self._score)
        self._window.draw_string(string, 0, 0)
class Dot:
    def __init__(self, color, center, radius, velocity, window):
        self._color = color
        self._center = center
        self._radius = radius
        self._velocity = velocity
        self._window = window
    def move(self):
        size = [self._window.get_width(), self._window.get_height()]
        for index in range(0, 2):
            #update centre at index
            self._center[index] = self._center[index] + self._velocity[index]
            if (self._center[index] + self._radius >= size[index]) or (self._center[index] <= self._radius):
                self._velocity[index] = - self._velocity[index]        
    def draw(self):
        surface = self._window.get_surface()
        color = Color(self._color)
        draw_circle(surface, color, self._center, self._radius) 
    def intersects(self, dot):
        distance = sqrt((self._center[0] - dot._center[0])**2 + (self._center[1] - dot._center[1])**2)
        return distance <= self._radius + dot._radius        
    def get_color(self):
        return self._color
    def randomize(self):
        size = [self._window.get_width(), self._window.get_height()]
        for index in range(0, 2):
            self._center[index] = randint(self._radius, size[index] - self._radius)        

main()
