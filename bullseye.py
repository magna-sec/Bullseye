#!/usr/bin/python3
import random
import sys
import yaml
import zlib
import os
import time
import string
from termcolor import colored
import cv2

# Purely to hide that ugly CTRL+C output
import signal
import subprocess
signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
# Purely to hide that ugly CTRL+C output

TERRAFORM_VARS = "terraform/vars.tf"
ALL_VARS = "group_vars/all.yml"
# SCR Variables
WORD_LIST = "words.txt"
CHALLENGE_ENCRYPTED = "roles/tech_scr/tasks/challenges/cryptography/encrypt.yml"
CHALLENGE_DECRYPTED = "roles/tech_scr/tasks/challenges/cryptography/decrypt.yml"
CHALLENGE_PACKETTRACER = "roles/tech_scr/tasks/challenges/networking/packettracer.yml"
CHALLENGE_LINUX_LINES= "roles/tech_scr/tasks/challenges/linux/line_count.yml"
CHALLENGE_LINUX_CHARS = "roles/tech_scr/tasks/challenges/linux/char_count.yml"
CHALLENGE_LINUX_HIDDEN = "roles/tech_scr/tasks/challenges/linux/hidden_file.yml"

LINUX_ADMIN_BOT = "roles/linux_admin/files/bot.py"
CHALLENGE_LINUX_LINES_FILE = "roles/linux_admin/files/line_count.txt"
CHALLENGE_LINUX_CHARS_FILE = "roles/linux_admin/files/char_count.txt"
CHALLENGE_LINUX_HIDDEN_FILE = "roles/linux_admin/files/hidden_file.txt"

CHALLENGE_LINUX_PERMS = "roles/tech_scr/tasks/challenges/linux/perms.yml"
CHALLENGE_LINUX_PERMS_GROUP_R = "Add group read to the folder"
CHALLENGE_LINUX_PERMS_GROUP_W = "Add group write to the folder"
CHALLENGE_LINUX_PERMS_PUBLIC_R = "Add public read to the folder"
CHALLENGE_LINUX_PERMS_PUBLIC_W = "Add public write to the folder"
CHALLENGE_LINUX_PERMS_DICT = {"640":CHALLENGE_LINUX_PERMS_GROUP_R,"620":CHALLENGE_LINUX_PERMS_GROUP_W,"604":CHALLENGE_LINUX_PERMS_PUBLIC_R,"602":CHALLENGE_LINUX_PERMS_PUBLIC_W}

CHALLENGE_LINUX_CUSER = "roles/tech_scr/tasks/challenges/linux/create_user.yml"
CHALLENGE_LINUX_CGROUP = "roles/tech_scr/tasks/challenges/linux/create_group.yml"
CHALLENGE_LINUX_USERGROUP = "roles/tech_scr/tasks/challenges/linux/user_groups.yml"


AP_NAMES = "ap_names.txt"
WIFI_WPA_CONFIG = "roles/wifi/tasks/wpa.yml"
WIFI_WEP_CONFIG = "roles/wifi/tasks/wep.yml"
WIFI_BOT = "roles/wifi/files/bot.py"
STREAM_SERVICE = "roles/tech_scr/files/vlc.sh"
CHALLENGE_WIFI_WPA = "roles/tech_scr/tasks/challenges/wifi/wpa.yml"
CHALLENGE_JOIN_WIFI = "roles/tech_scr/tasks/challenges/wifi/join_wifi.yml"
CHALLENGE_WIFI_WEP = "roles/tech_scr/tasks/challenges/wifi/wep.yml"
CHALLENGE_STREAM_BASE = "roles/tech_scr/files/base.mp4"
CHALLENGE_STREAM_FILE = "rles/tech_scr/files/stream.mp4"
CHALLENGE_WIFI_STREAM_FILE = "roles/tech_scr/tasks/challenges/wifi/stream.yml"


ENCRYPT_TYPES = ["AES256"]
DECRYPT_TYPES = ["3DES", "AES256"]
# Checks
COLOURS = ["black","blue","cyan","dark_grey","green","light_blue","light_cyan","light_green","light_grey","light_magenta","light_red","light_yellow","magenta","red","white","yellow"]
DIGITS = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"] # Sure theres a better way than this

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



def edit_file(file_path, field, value):
    # Using readlines()
    file1 = open(file_path, 'r')
    Lines = file1.readlines()

    # Strips the newline character
    for line in Lines:
        # ansible files
        if(".yml" in file_path):
            if(f"{field}: " in line):
                index = Lines.index(line)
                temp = Lines[index].split(':')
                Lines[index] = f"{temp[0]}: " + str(value).strip() + "\n"
        # python files
        if(".py" in file_path):
            if(f"{field} = " in line):
                index = Lines.index(line)
                temp = Lines[index].split(' ')
                Lines[index] = f'{temp[0]} = "' + str(value).strip() + '"\n'
        # terraform vars files
        if(".tf" in file_path):
            if(f"{field}" in line):
                index = Lines.index(line)
                while("default" not in Lines[index]):
                    index += 1
                temp = Lines[index].split('=')
                Lines[index] = f'{temp[0]}= ' + str(value).strip() + '\n'
                break
    
    file1 = open(file_path, 'w')
    file1.writelines(Lines)
    file1.close()

class PacketTracer:
    def __init__(self):
        # Variables
        self.random_file = random.choice(os.listdir("PacketTracer")) 
        print("FILE: " + self.random_file)
        self.flag = random.choice(open(WORD_LIST).readlines())
        self.pt_file = "PacketTracer/" + self.random_file
        self.pt_xml = "PacketTracer/temp.xml"

        # Functions
        self.decrypt_file()
        self.edit_xml()
        self.encrypt_file()
        edit_file(CHALLENGE_PACKETTRACER, "file_name", self.random_file)
        

    def decrypt_file(self):
        try:
            command = f"./pka2xml -d {self.pt_file} {self.pt_xml} 2>/dev/null"
            subprocess.check_output(command, shell=True)
        except:
            with open(self.pt_file, 'rb') as f:
                in_data = bytearray(f.read())

            i_size = len(in_data)

            out = bytearray()
            # Decrypting each byte with decreasing file length
            for byte in in_data:
                out.append((byte ^ i_size).to_bytes(4, "little")[0])
                i_size = i_size - 1

            # We decompress the file without the 4 first bytes
            with open(self.pt_xml, 'wb') as f:
                f.write(zlib.decompress(out[4:]))

        # Just to allow the file to write
        time.sleep(5)


    def edit_xml(self):
        new_flag = f'<OVERALL_COMPLETE_FEEDBACK translate="true" >Congrations! Flag: {self.flag}</OVERALL_COMPLETE_FEEDBACK>'
        file1 = open(self.pt_xml, 'r')
        Lines = file1.readlines()
 
        # Change Flag and timer from 30mins to 60mins
        for line in Lines:
            if("OVERALL_COMPLETE_FEEDBACK" in line):
                index = Lines.index(line)
                Lines[index] = new_flag
            if('COUNTDOWNMS="1800000" >' in line):
                index = Lines.index(line)
                Lines[index] = line.replace("1800000", "3600000")


        file1 = open(self.pt_xml, 'w')
        file1.writelines(Lines)
        file1.close()


    def encrypt_file(self):
        try:
            command = f"./pka2xml -e {self.pt_xml} {self.pt_file} 2>/dev/null"
            subprocess.check_output(command, shell=True)
        except:
            with open(self.pt_xml, 'rb') as f:
                in_data = bytearray(f.read())

            i_size = len(in_data)

            # Convert uncompressed size to bytes
            i_size = i_size.to_bytes(4, 'big')

            # Compress the file and add the uncompressed size
            out_data = zlib.compress(in_data)
            out_data = i_size + out_data
            o_size = len(out_data)

            xor_out = bytearray()
            # Encrypting each byte with decreasing file length
            for byte in out_data:
                xor_out.append((byte ^ o_size).to_bytes(4, "little")[0])
                o_size = o_size - 1

            # We decompress the file without the 4 first bytes
            with open(self.pt_file, 'wb') as f:
                f.write(xor_out)

        os.remove(self.pt_xml)
class Cryptography:
    def __init__(self):
        self.init_decrypt()
        self.init_encrypt()

    def encrypt_string(self, cleartext, encrypt_type):
        match encrypt_type:
            case "3DES":
                command =  f'echo -n "{cleartext.strip()}"  | openssl enc -pbkdf2 -des3 -base64 -pass pass:mysecretpassword -nosalt'
                encrypted = subprocess.check_output(command, shell=True).decode('utf-8').strip()
                return encrypted

            case "AES256":
                # Obtain key
                command1 = f'openssl enc -aes-256-cbc -k mysecretpassword -P -md sha1 -nosalt -pbkdf2 | grep "key" | cut -d "=" -f 2'
                command1_key = subprocess.check_output(command1, shell=True).decode('utf-8').strip()

                # Encrypt using said key
                command2 = f'echo -n "{cleartext.strip()}" | openssl enc -aes-256-cbc -K {command1_key} -iv 0 -base64 2>/dev/null'
                encrypted = subprocess.check_output(command2, shell=True).decode('utf-8').strip()
                return encrypted

    def init_encrypt(self):
        random_enc = random.choice(ENCRYPT_TYPES)
        random_word = random.choice(open(WORD_LIST).readlines())
        
        encrypted = self.encrypt_string(random_word.strip(), random_enc)
        edit_file(CHALLENGE_ENCRYPTED, "encrypted", encrypted)
        edit_file(CHALLENGE_ENCRYPTED, "decrypted", random_word)
        edit_file(CHALLENGE_ENCRYPTED, "type", random_enc)

    def init_decrypt(self):
        random_enc = random.choice(DECRYPT_TYPES)
        random_word = random.choice(open(WORD_LIST).readlines())
        
        encrypted = self.encrypt_string(random_word.strip(), random_enc)
        edit_file(CHALLENGE_ENCRYPTED, "encrypted", encrypted)
        edit_file(CHALLENGE_ENCRYPTED, "decrypted", random_word)
        edit_file(CHALLENGE_ENCRYPTED, "type", random_enc)
class Linux:
    def __init__(self):
        self.length_count()
        self.character_count()
        self.hidden_file()
        self.create_group()
        self.create_user()
        self.user_groups()
        self.perms()



    def length_count(self):
        random_length = random.choice(range(10, 500))
        with open(CHALLENGE_LINUX_LINES_FILE, "w") as my_file:
            for a in range(0, random_length):
                my_file.write("Hello There\n")
        edit_file(CHALLENGE_LINUX_LINES, "flag_token", random_length)

    def character_count(self):
        random_length = random.choice(range(10, 10000))
        with open(CHALLENGE_LINUX_CHARS_FILE, "w") as my_file:
            for a in range(0, random_length):      
                my_file.write(random.choice(string.ascii_lowercase))
        edit_file(CHALLENGE_LINUX_CHARS, "flag_token", random_length)

    def hidden_file(self):
        flag = random.choice(open(WORD_LIST).readlines())
        with open(CHALLENGE_LINUX_HIDDEN_FILE, "w") as my_file:
            my_file.write(flag)
        edit_file(CHALLENGE_LINUX_HIDDEN, "flag_token", flag)


    def create_group(self):
        flag = random.choice(open(WORD_LIST).readlines())

        # Edit bot
        edit_file(LINUX_ADMIN_BOT, "create_group_flag", flag)

        # Edit ansible challenge files
        edit_file(CHALLENGE_LINUX_CGROUP, "flag_token", flag)

    def create_user(self):
        flag = random.choice(open(WORD_LIST).readlines())

        # Edit bot
        edit_file(LINUX_ADMIN_BOT, "create_user_flag", flag)

        # Edit ansible challenge files
        edit_file(CHALLENGE_LINUX_CUSER, "flag_token", flag)

    def user_groups(self):
        flag = random.choice(open(WORD_LIST).readlines())
        
        # Edit bot
        edit_file(LINUX_ADMIN_BOT, "user_groups_flag", flag)

        # Edit ansible challenge files
        edit_file(CHALLENGE_LINUX_USERGROUP, "flag_token", flag)

    def perms(self):
        flag = random.choice(open(WORD_LIST).readlines())
        perm = random.choice(list(CHALLENGE_LINUX_PERMS_DICT.keys()))
        question = CHALLENGE_LINUX_PERMS_DICT[perm]

        # Edit bot
        edit_file(LINUX_ADMIN_BOT, "folder_perms_check", perm)
        edit_file(LINUX_ADMIN_BOT, "folder_perms_flag", flag)

        # Edit ansible challenge files
        edit_file(CHALLENGE_LINUX_PERMS, "permissions", question)
        edit_file(CHALLENGE_LINUX_PERMS, "flag_token", flag)


class Scr:
    def __init__(self):
        edit_file(ALL_VARS, "SCR", "True")
        self.get_users()
        convert_pt = PacketTracer()
        crypto = Cryptography()
        linux = Linux()
        wifi = Wifi(True)
        edit_file(ALL_VARS, "SCR", "False")

    def get_users(self):
        ask_u_que = Que(WIFI_QUES[0])
        edit_file(TERRAFORM_VARS, "amount_of_users", ask_u_que.answer)
        edit_file(ALL_VARS, "AmountOfUsers", ask_u_que.answer)
class Wifi:
    def __init__(self, scr):
        self.ssid = ""
        self.password = ""
        self.edit_wpa()
        self.edit_wep()
        self.overlay_video()
        if(scr): self.scr_conf()
    
    def edit_wpa(self):
        # Random SSID
        self.ssid = random.choice(open(AP_NAMES).readlines())
        # Random Password
        self.password = random.choice(open(WORD_LIST).readlines())

        # Edit ansible wifi config files
        edit_file(WIFI_WPA_CONFIG, "WPA_Name", self.ssid)
        edit_file(WIFI_WPA_CONFIG, "WPA_Pass", self.password)

        # Edit ansible challenge files
        edit_file(CHALLENGE_WIFI_WPA, "WPA_Name", self.ssid)
        edit_file(CHALLENGE_WIFI_WPA, "flag_token", self.password)
        
    def scr_conf(self):
        flag = random.choice(open(WORD_LIST).readlines())
        while(flag == self.password):
            flag = random.choice(open(WORD_LIST).readlines())

        # Edit bot
        edit_file(WIFI_BOT, "join_wifi", "True")
        edit_file(WIFI_BOT, "join_wifi_flag", flag)

        # Edit ansible challenge files
        edit_file(CHALLENGE_JOIN_WIFI, "WPA_Name", self.ssid)
        edit_file(CHALLENGE_JOIN_WIFI, "flag_token", flag)


    def overlay_video(self):
        flag = random.choice(open(WORD_LIST).readlines())
        # Read the video file
        video = cv2.VideoCapture(CHALLENGE_STREAM_BASE)

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(CHALLENGE_STREAM_FILE, fourcc, 30.0, (int(video.get(3)), int(video.get(4))))

        # Loop through the video frames
        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break

            # Add text overlay to the frame
            text = flag.strip()
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            thickness = 2
            text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
            text_x = int((frame.shape[1] - text_size[0]) / 2)
            text_y = int((frame.shape[0] + text_size[1]) / 2)
            cv2.putText(frame, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

            # Write the frame to the output video
            out.write(frame)

        # Release the resources
        video.release()
        out.release()
        cv2.destroyAllWindows()

        # Edit ansible challenge files
        edit_file(CHALLENGE_WIFI_STREAM_FILE, "flag_token", flag)

    def edit_wep(self):
        return

class Que:
    def __init__(self, question):
        self.question = question[0]
        self.possibles = question[1]
        self.choice = ""
        self.answer = ""
        self.ask_que()
    
    def ask_que(self):
        while self.choice not in self.possibles:
            print(colored(self.question, 'green'), end = "")
            print(colored(": ", 'white'), end = "")
            self.choice = input()  
        self.answer = self.choice  

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

def main():
    running = True
    splash()
    while(running):
        edit_file(ALL_VARS, "SCR", "False")
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
    main()
