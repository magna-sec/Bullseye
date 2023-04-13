#!/usr/bin/python3
from termcolor import colored

# Purely to hide that ugly CTRL+C output
import signal
import sys
signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
# Purely to hide that ugly CTRL+C output

# Checks
COLOURS = ["black","blue","cyan","dark_grey","green","light_blue","light_cyan","light_green","light_grey","light_magenta","light_red","light_yellow","magenta","red","white","yellow"]
DIGITS = ["0","1","2","3","4","5","6","7","8","9"] # Sure theres a better way than this

# Splash
SPLASH = """
         _____       _ _                     
        | ___ \     | | |                    
        | |_/ /_   _| | |___  ___ _   _  ___ 
        | ___ \ | | | | / __|/ _ \ | | |/ _ \\
        | |_/ / |_| | | \__ \  __/ |_| |  __/
        \____/ \__,_|_|_|___/\___|\__, |\___|
                                __/ |     
                                |___/
                   ___      ____ 
     ___.:::::::._/___/     \___\_.:::::::.___
        ':::::::' \\___\\     /___/ ':::::::'                       
"""

# Menus
MAIN = {"1":"Training", "2":"COMING SOON", "3":"Exit"}
TRAINING = {"1:":"Build WiFi", "2:":"Build COMING SOON"}

# Ques
WIFI_QUES = [["How many students?", DIGITS]]

class Que:
    def __init__(self, question):
        self.question = question[0]
        self.possibles = question[1]
        self.choice = ""
        self.ask_que()
    
    def ask_que(self):
        while self.choice not in self.possibles:
            print(colored(self.question, 'green'), end = "")
            print(colored(": ", 'white'), end = "")
            self.choice = input()    



class Menu:
    def __init__(self, menu_list, possibles):
        self.menu_list = menu_list
        self.possibles = possibles
        self.choice = ""
        self.print_menu()
    
    def print_menu(self):
        menu = self.menu_list
        for key in menu:
            tab = key + ": "

            print(colored(tab, 'white'), end = "") # e.g. 1:
            print(colored(menu[key], 'blue'))

        self.choice = self.get_input()

    def get_input(self):
        cursor = "Choice -> "

        while self.choice not in self.possibles:
            print(colored(cursor, 'magenta'), end = "")
            self.choice = input()
        return self.choice

def splash():
    print(SPLASH)

def start():
    running = True
    splash()
    while(running):
        main_menu = Menu(MAIN, DIGITS)
        if main_menu.choice == "1":
            training_menu = Menu(TRAINING, DIGITS)
            if(training_menu.choice == "1"): wifi_que = Que(WIFI_QUES[0])
        if main_menu.choice == "2":
            print("COMING SOON")
        if main_menu.choice == "3":
            running = False

if __name__ == "__main__":
    start()
