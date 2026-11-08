#!/usr/bin/env python3
'''
Copyright (c) 2026 @crazycatlover98544

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

You may also read these terms at the following website: https://opensource.org/license/mit

My GitHub account is located at https://github.com/crazycatlover98544
My MistWarp account is located at https://mistwarp.org/users/crazycatlover98544

Please note that this code is not written by an expert.
I am not responsible if this harms your computer.
'''

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from yesno import yesno
import json
import sys
import os

root = ctk.CTk()
root.title('Python3-powermenu Configuration')
root.geometry('600x390')
root.minsize(600,390)

root.update()
width = root.winfo_width()

ctk.set_appearance_mode('System') # CTk does this by default, but just to be sure
system_theme = ctk.get_appearance_mode()

user_path = f'{os.path.expanduser("~")}{"" if os.path.expanduser("~")[-1] == "/" else "/"}' # Needlessly complicated, but makes sure that the expanded user path has a '/' at the end; it usually does not (in my testing), but I don't know about other computers

if '.config' in os.listdir(user_path): # Check these so that way in case the error was due to lacking permissions, the program will not error later on
    if 'python3-powermenu' in os.listdir(f'{user_path}.config'):
        pass # The folder already exists
    else:
        messagebox.showerror('Configuration Missing','The configration for python3-powermenu is missing. If you have not ran it once yet, run it to generate a default configuration file.')
        sys.exit(1)
else:
    messagebox.showerror('Configuration Missing','The configration for python3-powermenu is missing. If you have not ran it once yet, run it to generate a default configuration file.')
    sys.exit(1)

try:
    with open(f'{user_path}.config/python3-powermenu/config.json','r') as file:
        try:
            configuration = json.load(file)
        except json.decoder.JSONDecodeError:
            messagebox.showerror('Configuration Invalid','The configration for python3-powermenu is invalid. You may have to manually fix it or delete it.')
            sys.exit(1)
except (FileNotFoundError, OSError):
    messagebox.showerror('Configuration Missing','The configration for python3-powermenu is missing. If you have not ran it once yet, run it to generate a default configuration file.')
    sys.exit(1)

color_theme = configuration.get('color',True) # True=dark, False=light
suspend_button = configuration.get('suspend',True)

if configuration.get('themepath',False):
    theme = configuration.get('themepath','')
    theme_path_ui_vals = [theme,'Use running directory']
else:
    theme_path_ui_vals = ['Use running directory']
    theme = ''

def reset_settings():
    global theme, theme_path_ui_vals
    if configuration.get('themepath',False):
        theme = configuration.get('themepath','')
        theme_path_ui_vals = [theme,'Use running directory']
    else:
        theme_path_ui_vals = ['Use running directory']
        theme = ''
    theme_path_ui.configure(values=theme_path_ui_vals)
    theme_path_ui.set(theme_path_ui_vals[0])
    color_button.set('Dark' if color_theme else 'Light')
    suspend_button_ui.set('Show' if suspend_button else 'Hide')

def update_settings():
    global theme, color_theme, suspend_button, configuration
    if yesno('Overwrite Configuration?','Do you want to overwrite the configuration?',theme=ctk.get_appearance_mode()):
        theme = theme_path_ui.get()
        color_theme = True if color_button.get() == 'Dark' else False
        suspend_button = True if suspend_button_ui.get() == 'Show' else False
        assembled_dict = {'themepath': '' if theme == 'Use running directory' else theme, 'color': color_theme, 'suspend': suspend_button}
        try:
            with open(f'{user_path}.config/python3-powermenu/config.json','w') as file:
                json.dump(assembled_dict,file,indent=4)
        except OSError as e: # File unwritable
            messagebox.showerror('Error Writing to Configuration',f'OSError while attempting write to configuration: {e}')
            sys.exit(1)
        configuration = assembled_dict
        del assembled_dict

def theme_change():
    ctk.set_appearance_mode(program_theme.get())

title = ctk.CTkLabel(root,text='Python3-powermenu Configuration',font=('Arial',20))
title.pack(pady=10)

theme_path_label = ctk.CTkLabel(root,text='Current Theme Path',font=('Arial',16))
theme_path_label.pack()

theme_path_ui = ctk.CTkComboBox(root,values=theme_path_ui_vals,font=('Arial',12),width=width-15,height=25)
theme_path_ui.pack(pady=10)

color_label = ctk.CTkLabel(root,text='Color Scheme',font=('Arial',16))
color_label.pack()

color_button = ctk.CTkSegmentedButton(root,values=['Light','Dark'],height=25)
color_button.pack(pady=10)
color_button.set('Dark' if color_theme else 'Light')

suspend_label = ctk.CTkLabel(root,text='Suspend Button',font=('Arial',16))
suspend_label.pack()

suspend_button_ui = ctk.CTkSegmentedButton(root,values=['Show','Hide'],height=25)
suspend_button_ui.pack(pady=10)
suspend_button_ui.set('Show' if suspend_button else 'Hide')

update = ctk.CTkButton(root,text='Update',command=update_settings,font=('Arial',14),width=width-20,height=30)
update.pack()

reset = ctk.CTkButton(root,text='Reset',command=reset_settings,font=('Arial',14),width=width-20,height=30,fg_color=('#979DA2','#4A4A4A'),text_color='white',hover_color=('#6E7174','#3B3B3B'))
reset.pack(pady=10)

program_theme = ctk.StringVar(value=system_theme)
program_theme_ui = ctk.CTkSwitch(root,text='Program Theme',command=theme_change,variable=program_theme,onvalue='Dark',offvalue='Light')
program_theme_ui.pack()

while True: # Probably a better way to do this; I am not bothering
    try:
        if not root.winfo_width() == width:
            width = root.winfo_width() # Configure the width of all the widgets
            theme_path_ui.configure(width=width-15)
            update.configure(width=width-20)
    except tk.TclError:
        pass # The width command keeps failing when I close the app with "application destroyed," this will prevent it from erroring when the app is closed.
    root.update()
sys.exit(0) # CTk has an issue where it will not terminate the program after the window is closed all the time, this forces the program to close