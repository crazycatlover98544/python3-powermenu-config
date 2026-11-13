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

Most of this code is from a part of my project "python3-powermenu", found at the following URL: https://github.com/crazycatlover98544/python3-powermenu
You can also run that to make a default configuration (though this does not require a GUI)
'''

import json
import sys
import os

configfile = False
for item in sys.argv:
    if item[:13] == '--configfile=':
        configfile = item[13:]

overwrite_warn = True
if '--no-warn-overwrite' in sys.argv:
    overwrite_warn = False

if configfile:
    configfile = configfile.replace('\n','').replace('\r','').replace('\t','').replace('"','').replace("'",'') # Needlessly complicated; quotes added if someone had a path with a space or other disallowed character in it

user_path = f'{os.path.expanduser('~')}{"" if os.path.expanduser('~')[-1] == "/" else "/"}' # Needlessly complicated, but makes sure that the expanded user path has a '/' at the end; it usually does not (in my testing), but I don't know about other computers

if not configfile:
    try:
        os.makedirs(f'{user_path}.config/python3-powermenu/')
    except (FileExistsError, OSError): # I doubt it will raise OSError, but just in case.
        if '.config' in os.listdir(user_path): # Check these so that way in case the error was due to lacking permissions, the program will not error later on
            if 'python3-powermenu' in os.listdir(f'{user_path}.config'):
                pass # The folder already exists
            else:
                sys.stderr.write(f'The folder {user_path}.config/python3-powermenu does not exist.\n')
                sys.exit(1)
        else:
            sys.stderr.write(f'The folder {user_path}.config does not exist.\n')
            sys.exit(1)

if configfile:
    split_cf_path = os.path.split(configfile)
if configfile:
    try:
        if split_cf_path[0] == '':
            split_cf_path = ('.',split_cf_path[1]) # Handles if a person passes it as a relative directory
        elif split_cf_path[1] == '':
            split_cf_path = ('.',split_cf_path[0])
        if split_cf_path[1] in os.listdir(split_cf_path[0]):
            if overwrite_warn:
                if not input('Error: The configuration file already exists. Overwrite it? [Y/N]: ').lower() == 'y': # Not just doing == 'n' because otherwise, if someone put an invalid character, it would be seen as yes
                    print('Quitting...')
                    sys.exit(0)
    except OSError as e:
        sys.stderr.write(f'An error occured attempting to verify the path: {e}\n')
        sys.exit(1)
else:
    if 'config.json' in os.listdir(f'{user_path}.config/python3-powermenu'):
        if overwrite_warn:
            if not input('Error: The configuration file already exists. Overwrite it? [Y/N]: ').lower() == 'y': # Not just doing == 'n' because otherwise, if someone put an invalid character, it would be seen as yes
                print('Quitting...')
                sys.exit(0)

placeholder_data = {'themepath': False, 'color': True, 'suspend': True}
if configfile:
    try:
        with open(configfile,'w') as file:
            json.dump(placeholder_data,file,indent=4)
    except (FileExistsError, OSError) as e: # I doubt it will raise FileExistsError, but just to be sure.
        sys.stderr.write(f'Failed to write defaults to configuration file: {e}.\n')
        sys.exit(1)
else:
    try:
        with open(f'{user_path}.config/python3-powermenu/config.json','w') as file:
            json.dump(placeholder_data,file,indent=4)
    except (FileExistsError, OSError) as e: # I doubt it will raise FileExistsError, but just to be sure.
        sys.stderr.write(f'Failed to write defaults to configuration file: {e}.\n')
        sys.exit(1)
del placeholder_data # Free that RAM

if configfile:
    print(f'Configuration wrote to {configfile}')
else:
    print(f'Configuration wrote to {user_path}.config/python3-powermenu/config.json')
sys.exit(0)