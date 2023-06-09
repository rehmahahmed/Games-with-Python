# Hacking  Version 8

# HOW TO RUN-
# keep this file and uagame.py file (module from course) in the same folder with .py extension
# open cmd, navigate to the folder in which you have saved the file
# type this command- 
# python hackingv8.py
# voila!

# INSTRUCTIONS-
# This is a text based-password guessing game.
# The game starts with a start menu with short instructions.(NEW)
# On pressing Enter the game starts with a heading and No. of Attempts left (top left corner)
# Next, a list of potential passwords mixed within confusing symbols is displayed(below attempts no.)
# The correct password is different every time the game is played.(NEW)
# The player has 4 attempt to guess the password.
# On each failed attempt the player is given a hint(top right corner
# After 3rd failed attempt a lockout warning is displayed(bottom right corner)
# After 4 failed attempts terminal is locked- Game Over Mate!
# if correct password is guessed within 4 attempts you will exit debug mode - You Won!

from uagame import Window
from time import sleep
from random import randint, choice
def main():
    location = [0, 0]
    attempts = 4
    window = create_window()
    main_screen(window)
    set_values(window)
    display_header(window, location, attempts)
    password = display_password_list(window, location)
    guess = get_guesses(window, password, location, attempts)
    end_game(window, guess, password)

def create_window():
    window = Window("Hacking", 600, 500)
    window.set_font_name("couriernew")
    window.set_font_size(18)
    window.set_font_color("green")
    window.set_bg_color("black")
    return window

def main_screen(window):
    window.set_font_name("couriernew")
    window.set_font_size(64)
    window.set_font_color("green")
    window.set_bg_color("black")
    
    title = "HACKING"
    start_prompt = "_ENTER TO CONTINUE DEBUG PROCESS_"
    
    title_location = [(window.get_width() - window.get_string_width(title)) // 2 , (window.get_height() - window.get_font_height()*2) // 2]
    window.draw_string(title, title_location[0], title_location[1])
    h = (title_location[1]+window.get_font_height())
    window.update()
    set_values(window)  
    instruct1 = "THE SYSTEM HAS BEEN LOCKED"
    instruct2 = "ENTER DEBUG MODE AND UNLOCK THE SYSTEM"
    instruct3 = "REMEMBER! YOU ONLY HAVE 4 ATTEMPTS"
    instruction = [instruct1, instruct2, instruct3]
    
    for i in instruction:
        sleep(0.3)
        h += window.get_font_height()
        loc = [(window.get_width() - window.get_string_width(i)) // 2, h]
        display_line(window, i, loc)
    sleep(0.3)
    start_prompt_location = [(window.get_width() - window.get_string_width(start_prompt)), (window.get_height() - window.get_font_height())]
    prompt_user(window, start_prompt, start_prompt_location)
    window.clear()
    
def set_values(window):
    window.set_font_name("couriernew")
    window.set_font_size(18)
    window.set_font_color("green")
    window.set_bg_color("black") 

def display_header(window, location, attempts):
    headers = ["DEBUG MODE", str(attempts) + " ATTEMPT(S) LEFT", ""]
    for header in headers:
        display_line(window, header, location)

def display_password_list(window, location):
    embedded_size = 20
    passwords = ["PROVIDE", "SETTING", "CANTINA", "CUTTING", "HUNTERS", "SURVIVE", "HEARING", "HUNTING", "REALIZE", "NOTHING", "OVERLAP", "FINDING", "PUTTING"]    
    for password in passwords:    
        password_line = embed_password(password, embedded_size)
        display_line(window, password_line, location)
    display_line(window, "", location)
    password_count = len(passwords)
    password_index = randint(0, password_count - 2)
    correct_password = passwords[password_index]    
    return correct_password
        
def embed_password(password, size):
    fill = "!@#$%^&*()-+=~[]{}"
    embedding= ""
    password_size = len(password)
    split_index = randint(0, size - password_size)
    for index in range(0, split_index):
        embedding = embedding + choice(fill)
    embedding = embedding + password
    for index in range(split_index + password_size, size):
        embedding = embedding + choice(fill)
    return embedding

def get_guesses(window, password, location, attempts):
    prompt = "ENTER PASSWORD >"
    feedback_location = [window.get_width() // 2, 0]
    line_x = 0
    guess = prompt_user(window, prompt, location)
    attempts -= 1
    while guess != password and attempts>0:
        window.draw_string(str(attempts), line_x, window.get_font_height())
        check_warning(window, attempts)
        display_hint(window, password, guess, feedback_location)
        guess = prompt_user(window, prompt, location)
        attempts -= 1 
    return guess

def check_warning(window, attempts):
    warning = "*** LOCKOUT WARNING ***"
    if attempts == 1:
        wx = window.get_width() - window.get_string_width(warning)
        wy = window.get_height() - window.get_font_height()
        window.draw_string(warning, wx, wy)
        
def display_hint(window, password, guess, location):
    string = guess + ' INCORRECT'
    display_line(window, string, location)
    index = 0
    correct = 0
    max = len(password)
    for letter in guess:
        # check letter
        if (index < max) and (letter == password[index]):
            correct = correct + 1
        index = index + 1
    string = str(correct) + '/' + str(max) + ' IN MATCHING POSITIONS'
    display_line(window, string, location)    
        
def end_game(window, guess, password):
    window.clear()
    if guess == password:
        outcomes = [guess, "", "EXITING DEBUG MODE", "", "LOGIN SUCCESSFUL - WELCOME BACK", ""]
        end = "PRESS ENTER TO CONTINUE"
    else:
        outcomes = [guess, "", "LOGIN FAILURE - TERMINAL LOCKED", "", "PLEASE CONTACT AN ADMINISTRATOR", ""]
        end = "PRESS ENTER TO EXIT"     
    location = display_outcome(window, outcomes)
    location[0] = (window.get_width() - window.get_string_width(end)) // 2
    prompt_user(window, end, location)
    window.close()

def display_outcome(window, outcomes):
    string_height = window.get_font_height()
    outcome_height = (len(outcomes) + 1)*string_height
    y_space = window.get_height() - outcome_height
    line_y = y_space // 2
    
    location = [0, line_y]
    for outcome_line in outcomes: 
        x_space = window.get_width() - window.get_string_width(outcome_line)
        location[0] = x_space // 2
        display_line(window, outcome_line, location)
    return location

def display_line(window, string, location):
    #Display string in window and update the location
    # - window is the Window to display in
    # - string is the str to display 
    # - location is the tuple containing the int x and y coords
    # of where the string should be displayed and it should be updated
    # to one "line" below the top left corner of the displayed string
    pause = 0.3
    string_height = window.get_font_height()    
    window.draw_string(string, location[0], location[1])
    window.update() 
    sleep(pause)
    location[1] = location[1] + string_height    

def prompt_user(window, prompt, location):
    inpt = window.input_string(prompt, location[0], location[1])
    location[1] = location[1] + window.get_font_height()
    return inpt
 
main()

