#!/usr/bin/python3
import random
import sys
import yaml
import zlib
import os
import time
from termcolor import colored

# Purely to hide that ugly CTRL+C output
import signal
import subprocess
signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
# Purely to hide that ugly CTRL+C output

# SCR Variables
WORD_LIST = "words.txt"
CHALLENGE_ENCRYPTED = "roles/tech_scr/tasks/challenges/cryptography/encrypt.yml"
CHALLENGE_DECRYPTED = "roles/tech_scr/tasks/challenges/cryptography/decrypt.yml"
ENCRYPT_TYPES = ["AES256"]
DECRYPT_TYPES = ["3DES", "AES56"]
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
MAIN = {"1":"Training Builds", "2":"COMING SOON", "3":"Exit"}
TRAINING = {"1":"WiFi", "2":"Tech SCR - COMING SOON", "3":"Radio - COMING SOON"}

# Ques
WIFI_QUES = [["How many students?", DIGITS]]

class PacketTracer:
    def __init__(self):
        self.decrypt_file("temp.xml")
        self.edit_xml("PacketTracer/temp.xml", "ILikTurtles")
        self.encrypt_file("temp.xml")

    def decrypt_file(self, pt_xml):
        pt_file = "lab81-configure-and-modify-standard-ipv4-acls.pka"

        command = f"sudo docker run -v `pwd`/PacketTracer:/pkt  quentinn42/pka2xml:latest pka2xml -d /pkt/{pt_file} /pkt/{pt_xml}"
        subprocess.check_output(command, shell=True)
        # Just to allow the file to write
        time.sleep(5)


    def edit_xml(self, pt_xml, flag):
        command = f"sudo chmod 777 {pt_xml}"
        subprocess.check_output(command, shell=True)


        new_flag = f'<OVERALL_COMPLETE_FEEDBACK translate="true" >Congrations! Flag: {flag}</OVERALL_COMPLETE_FEEDBACK>'
        file1 = open(pt_xml, 'r')
        Lines = file1.readlines()
 
        # Strips the newline character
        for line in Lines:
            if("OVERALL_COMPLETE_FEEDBACK" in line):
                index = Lines.index(line)
                Lines[index] = new_flag

        file1 = open(pt_xml, 'w')
        file1.writelines(Lines)
        file1.close()


    def encrypt_file(self, pt_xml):
        pt_new = "mod.pkt"

        command = f"sudo docker run -v `pwd`/PacketTracer:/pkt  quentinn42/pka2xml:latest pka2xml -e /pkt/{pt_xml} /pkt/{pt_new}"
        subprocess.check_output(command, shell=True)
        
        remove = f"PacketTracer/{pt_xml}"
       # os.remove(remove)



class Scr:
    def __init__(self):
        convert_pt = PacketTracer()
        #self.init_encrypt()
        #self.init_decrypt()

    def edit_cryptography(self, encrypted, decrypted, file_path):
        # Using readlines()
        file1 = open(file_path, 'r')
        Lines = file1.readlines()
 
        # Strips the newline character
        for line in Lines:
            if("decrypted: " in line):
                index = Lines.index(line)
                Lines[index] = "    decrypted: " + decrypted
            if("encrypted: " in line):
                print("HI")
                index = Lines.index(line)
                Lines[index] = "    encrypted: " + encrypted + "\n"        
        
        file1 = open(file_path, 'w')
        file1.writelines(Lines)
        file1.close()

    # echo -n "hellothere" | openssl enc -pbkdf2 -des3 -base64 -pass pass:mysecretpassword
    def init_encrypt(self):
        random_word = random.choice(open(WORD_LIST).readlines())

        command = f'echo -n "{random_word}"  | openssl enc -pbkdf2 -des3 -base64 -pass pass:mysecretpassword'
        encrypted = subprocess.check_output(command, shell=True).decode('utf-8').strip()

        self.edit_cryptography(encrypted, random_word, CHALLENGE_ENCRYPTED)
        

    # echo "U2FsdGVkX1+x2JIRVf04ppVKudXBukdtUYziRNgnCBg=" | base64 --decode | openssl enc -pbkdf2 -des3 -d -pass pass:mysecretpassword
    def init_decrypt(self):
        random_word = random.choice(open(WORD_LIST).readlines())
        
        command = f'echo -n "{random_word}"  | openssl enc -pbkdf2 -des3 -base64 -pass pass:mysecretpassword'
        encrypted = subprocess.check_output(command, shell=True).decode('utf-8').strip()

        self.edit_cryptography(encrypted, random_word, CHALLENGE_DECRYPTED)

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
            if(training_menu.choice == "2"): scr_exam = Scr()
        if main_menu.choice == "2":
            print("COMING SOON")
        if main_menu.choice == "3":
            running = False

if __name__ == "__main__":
    start()
