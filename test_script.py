from future.moves import tkinter
from tkinter import *
from tkinter import simpledialog
from tkinter import ttk
from tkinter import messagebox
import os
import datetime
import tarfile
import argparse
import traceback

parser = argparse.ArgumentParser(description="VShell")
parser.add_argument('filesystem_archive', help="Path to the filesystem archive.")
parser.add_argument('--script', help="Path to a script file containing commands.")
args = parser.parse_args()
#cur_dir = args.filesystem_archive.split("/")[len(args.filesystem_archive.split("/"))-1].replace(".tar", "")
cur_dir = ""
tarfile_location = args.filesystem_archive

#setters for the program, so it knows in which directory it is and who is the current user
tar_file = tarfile.open(tarfile_location)
cur_user = os.path.abspath(__file__).split("\\")[2]
tar_file_files = tar_file.getnames()

top = Tk()  #создает окошко
top.geometry("1200x600")  #размер окошка
mem = str()

def read_and_decide(com = None):
    global cur_dir  #imports the global variables for use inside the function
    global mem
    global tar_file_files

    command = input_box.get("1.0", "end-1c")
    if com:
        command = com
    mem = mem + command + '\n'
    input_box.delete(1.0, END)
    if command == "ls":
        print("ls done: ",cur_dir)
        tar_file_files_unique = list()
        for file in tar_file_files:
            if file.startswith(str(cur_dir)):
                if str(cur_dir) in file:
                    tar_file_files_unique.append(file.lstrip(str(cur_dir)).split('/')[0])
                else:
                    tar_file_files_unique.append(file.split('/')[0])
        tar_file_files_unique = set(tar_file_files_unique)
        tar_file_files_unique = list(tar_file_files_unique)
        tar_file_files_unique.sort()
        print(str(tar_file_files_unique))
        display_box.config(state=NORMAL)
        for file in tar_file_files_unique:
            mem += file + "\n"
        display_box.delete(1.0, END)
        display_box.insert(1.0, mem)
        display_box.config(state=DISABLED)
        return mem

    elif command == "test":
        mem += str(os.path.abspath(__file__).split("\\")) + "\n"
        mem += cur_dir + "\n"
        mem += str(tar_file_files[1].split('/'))
        display_box.config(state=NORMAL)
        display_box.delete(1.0, END)
        display_box.insert(1.0, mem)
        display_box.config(state=DISABLED)

    elif command == "exit":  #exits the application
        quit()

    elif command.startswith('cd') == True:  #changes the directory by changing the cur_dir variable
        display_box.config(state=NORMAL)
        display_box.delete(1.0, END)
        display_box.insert(1.0, mem)
        display_box.config(state=DISABLED)
        print(tar_file_files)
        try:
            first_part = command.split()[0]
            print(first_part)
            second_part = command.split()[1]
            print(second_part)
        except:
            mem += "Wrong use of command cd! Try again!\n"
            display_box.config(state=NORMAL)
            display_box.delete(1.0, END)
            display_box.insert(1.0, mem)
            display_box.config(state=DISABLED)
        if second_part == '..':
            print(cur_dir.rstrip(cur_dir.split('/')[len(cur_dir.split('/'))-1]))
            cur_dir = cur_dir.rstrip(cur_dir.split('/')[len(cur_dir.split('/'))-1]+'/')
        else:
            flag = 0
            for file in tar_file_files:
                if file.startswith(second_part):
                    flag = 1
            if flag == 1:
                if cur_dir != "":
                    cur_dir += '/'
                cur_dir += second_part + "/"
                print("cd done: ", cur_dir)
            elif flag == 0:
                mem += "No such directory!\n"
                display_box.config(state=NORMAL)
                display_box.delete(1.0, END)
                display_box.insert(1.0, mem)
                display_box.config(state=DISABLED)
        return mem

    elif command == "clear":  #clear the console
        mem = ''
        display_box.config(state=NORMAL)
        display_box.delete(1.0, END)
        display_box.insert(1.0, mem)
        display_box.config(state=DISABLED)

    elif command == "date":  #outputs date
        display_box.config(state=NORMAL)
        mem = mem + str(datetime.datetime.today()) + '\n'
        display_box.delete(1.0, END)
        display_box.insert(1.0, mem)
        display_box.config(state=DISABLED)
        return mem

    elif command == "who":
        display_box.config(state=NORMAL)
        mem = mem + "Users name is " + cur_user + '\n'
        display_box.delete(1.0, END)
        display_box.insert(1.0, mem)
        display_box.config(state=DISABLED)
        return mem

    elif command.startswith('tac') == True:
        file_list = list()
        buf = str()
        num_of_files = len(command.split())
        for i in range(1, num_of_files):
            file_list.append(cur_dir + command.split()[i])
        print(str(file_list), num_of_files)
        for i in range(0, len(file_list)):
            f = tar_file.extractfile(file_list[i])
            buf += str(f.read()).replace('\r', '').replace("'", '')
        print(buf)
        mem += buf
        display_box.config(state=NORMAL)
        display_box.delete(1.0, END)
        display_box.insert(1.0, mem)
        display_box.config(state=DISABLED)
        return mem

    else:  #case for when command was not found
        display_box.config(state=NORMAL)
        mem = mem + "Error! No such command!" + '\n'
        display_box.delete(1.0, END)
        display_box.insert(1.0, mem)
        display_box.config(state=DISABLED)



test_button = Button(top, text="Ввести команду", fg="black", command=read_and_decide)  #создание кнопки
test_button.place(rely=1, relx=1, relwidth=0.1, relheight=0.05, anchor=SE)

display_box = Text(top)
display_box.config(font=(30))
display_box.place(rely=0, relx=0, relwidth=1, relheight=0.95)

input_box = Text(top)
input_box.config(font=(30))
input_box.place(rely=1, relx=0, relwidth=0.9, relheight=0.05, anchor=SW)

try:
    date = str(datetime.datetime.today())
    print("date: ", date)
    assert read_and_decide('date') == "date\n" + date + "\n"
    print("date\n" + str(datetime.datetime.today()) + "\n")
    assert read_and_decide('ls') == "date\n" + date + "\n" + "ls\naboba\nabobus\nconfig.cfg\nnew_directory\n"
    assert read_and_decide("cd ..") == "date\n" + date + "\n" + "ls\naboba\nabobus\nconfig.cfg\nnew_directory\n" + "cd ..\n"
    assert read_and_decide("cd new_directory") == "date\n" + date + "\n" + "ls\naboba\nabobus\nconfig.cfg\nnew_directory\n" + "cd ..\n" + "cd new_directory\n"
    assert read_and_decide("ls") == "date\n" + date + "\n" + "ls\naboba\nabobus\nconfig.cfg\nnew_directory\n" + "cd ..\n" + "cd new_directory\n" + "ls\n" + "aboba2.txt\n" + "abobus2.txt\n" + "more_directory\n"
except AssertionError:
    print("TEST ERROR")
    traceback.print_exc()
else:
    print("TEST PASSED")


#test = read_and_decide("ls")
#test = read_and_decide("who")
#test = read_and_decide("date")


top.mainloop()
