import tkinter as tk
import re, pyperclip

window = tk.Tk()
info = tk.Text(fg="white", bg="black", width=70, height=20)
info.pack()


def addInput():
    noCode = False
    allLines = info.get('1.0', 'end').split('\n')
    copy = allLines[0]
    try:
        codeRegex = re.compile(r'[A-Z]{1,2}\d\d? \d[A-Z][A-Z]')
        pat = codeRegex.search(copy)
        print(pat.group())
        pyperclip.copy(pat.group())
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
    if len(allLines) >= 2:
        gpRegex = re.compile(r'(Prescribing Account does not match: )+(.*)+([A-Z]{1,2}\d\d? \d[A-Z][A-Z])+')
        allLinesStr = ' '.join(allLines)
        gpInfo = gpRegex.search(allLinesStr)
        if gpInfo is not None:
            gpCode = gpInfo.group(3)
            # info.insert('end', '\n\n\n')
            # info.insert('end', gpCode)


addButton = tk.Button(window,
                      text="ENTER",
                      command=addInput)
addButton.pack()

window.mainloop()
