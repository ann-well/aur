import tkinter as tk
import re, pyperclip

window = tk.Tk()
info = tk.Text(fg="white", bg="black", width=60, height=20)
info.pack()

def addInput():
    allLines = info.get('1.0', 'end').split('\n')

    patient = allLines[0]
    gp = allLines[2]
    siebel = allLines[3]
    patRegex = re.compile(r'(Contact not matched: )(.*?)(, )+(.*?)(, )+(\d\d/\d\d/\d\d\d\d)+(, .*?, )+([A-Z][A-Z]\d* \d*[A-Z][A-Z])+')

    pat = patRegex.search(patient)
    name = pat.group(2).title()
    lastname = pat.group(4).title()
    date = pat.group(6)
    code = pat.group(8)

    info.insert('end', '\n\n')
   
    email = 'Hi,\nwe would like to confirm that the GP details for ' + name + ' ' + lastname + ' dob ' + date + ' are ' + siebel + '. Please update the data on your system.\nMany thanks'
    info.insert('end', email)
    pyperclip.copy(email)

addButton = tk.Button(window,
text = "ENTER", 
command = addInput)
addButton.pack()

window.mainloop()

