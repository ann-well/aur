import tkinter as tk
import re, pyperclip
from tkinter import *

window = tk.Tk()
info = tk.Text(fg="white", bg="black", width=70, height=20)
info.pack()

def createNpr():
    pass

def pullInfo():
    noCode = False
    allLines = info.get('1.0', 'end').split('\n')
    copy = allLines[0]
    try:
        codeRegex = re.compile(r'[A-Za-z]{1,2}\d\d? \d[A-Za-z][A-Za-z]')
        pat = codeRegex.search(copy)
        print(pat.group())
        pyperclip.copy(pat.group().upper())
    except AttributeError:
        print('----No code found----')
        noCode = True

    nameRegex = re.compile(r'(, )([A-Z])')
    dateRegex = re.compile(r'\d\d/\d\d/\d\d\d\d')
    name = nameRegex.search(copy)
    nameLet = str(name.group(2)) + '*'
    date = dateRegex.search(copy)
    if noCode == True:
        pyperclip.copy(date.group())

    info.insert('end', '\n\n')
    info.insert('end', nameLet)
    info.insert('end', '\n\n')
    info.insert('end', date.group())
    #if len(allLines) >= 2:
        #gpRegex = re.compile(r'(Prescribing Account does not match: )+(.*)+([A-Za-z]{1,2}\d\d? \d[A-Za-z][A-Za-z])+')
        #allLinesStr = ' '.join(allLines)
        #gpInfo = gpRegex.search(allLinesStr)
        #if gpInfo is not None:
            #gpCode = gpInfo.group(3)
            # info.insert('end', '\n\n\n')
            # info.insert('end', gpCode)


frame = Frame(window)
frame.pack(side=BOTTOM, fill=BOTH, expand=True)

addButton = tk.Button(window,
                      text="ENTER",
                      command=pullInfo)
nprButton = tk.Button(window,
                      text="NPR",
                      bg='black', fg='white',
                      command=createNpr)
nprButton.pack(in_=frame, side=RIGHT, padx=30, pady=7)
addButton.pack(in_=frame, side=RIGHT, padx=172, pady=7)


window.mainloop()
