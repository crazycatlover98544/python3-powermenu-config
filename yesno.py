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
import customtkinter as ctk

_rv = None

def yesno(title,contents,theme='System',values=['Yes','No']):
    global _rv
    _rv = None
    
    root = ctk.CTk()
    root.title(title)
    root.overrideredirect(True) # Disable the window bar

    screen_width = root.winfo_screenwidth() # Get width/height to center the window
    screen_height = root.winfo_screenheight()
    root.geometry(f'250x120+{(screen_width//2)-125}+{(screen_height//2)-60}')
    
    ctk.set_appearance_mode(theme)
    
    title_ui = ctk.CTkLabel(root,text=title,font=('Arial',16))
    title_ui.pack(pady=10)
    
    contents_ui = ctk.CTkLabel(root,text=contents,font=('Arial',12))
    contents_ui.pack()
    
    def return_val(root): # Yes, I know a function inside a function is not recommended, but it works
        global _rv
        if values_ui.get() == values[0]:
            _rv = True
        else:
            _rv = False
        root.quit()
        root.destroy()
    
    values_ui = ctk.CTkSegmentedButton(root,values=values,height=25,command=lambda _: return_val(root)) # likely a better way to do that, but it works
    values_ui.pack(pady=10)
    
    root.mainloop()
    
    return _rv # This is the only way to return the value, as putting return in return_val would just close the dialogue and not return anything