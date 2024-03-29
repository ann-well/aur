import tkinter as tk
import re, pyperclip, openpyxl
from tkinter import *
import tkinter.font as tkfont

# Create window for user interface
window = tk.Tk()
window.title('AUR')
info = tk.Text(fg="white", bg="black", width=70, height=15)
info.configure(font=('Times New Roman', 12))
info.pack()

# Create lists for new patient registrations
npr_name = []
npr_lastname = []
npr_date = []
npr_address = []
npr_postcode = []

npr_gp = []
npr_gp_code = []

def createNpr():
"""Function to create standardized format of patient information and insert it into previously created lists"""
    try:
        allLines = info.get('1.0', 'end').split('\n')
        patRegex = re.compile(r'(Contact not matched: )(.*?)(, )+(.*?)(, )+(\d\d/\d\d/\d\d\d\d)+(, .*?, )?([A-Za-z]{1,2}\d\d? \d[A-Za-z][A-Za-z])?')

        pat = patRegex.search(', '.join([item for item in allLines if item.startswith('Contact')]))
        npr_name.append(pat.group(2).title())
        npr_lastname.append(pat.group(4).title())
        npr_date.append(pat.group(6))
        npr_address.append(pat.group(7))
        if pat.group(8) is not None:
            npr_postcode.append(pat.group(8).upper())
        else:
            npr_postcode.append(' ')

        gpRegex = re.compile(r'(Prescribing Account does not match: )+(.*, )+([A-Z][A-Z]\d+ \d+[A-Z][A-Z])+')
        account = gpRegex.search(', '.join([item for item in allLines if item.startswith('Prescribing') or item.startswith('\rPrescribing')]))
        if account is not None:
            npr_gp.append(account.group(2))
            if account.group(3) is not None:
                npr_gp_code.append(account.group(3).upper())
            else:
                npr_gp.append(' ')
        else:
            prescribing = ', '.join([item for item in allLines if item.startswith('Prescribing') or item.startswith('\rPrescribing')])
            noPres = prescribing.replace('Prescribing Account does not match:', '')
            npr_gp.append(noPres)
            npr_gp_code.append('')

        info.delete('1.0', END)
        info.insert('end', '\nSENT TO NPR LIST')
    except:
        info.insert('end', '\n\n')
        info.insert('end', 'INCORRECT INPUT')  
        

def pullInfo():
"""Function to pull relevant information from pasted text and copy the main part to clipboard"""
    try:
        noCode = False
        allLines = info.get('1.0', 'end').split('\n')
        try:
            codeRegex = re.compile(r'[A-Za-z]{1,2}\d\d? \d[A-Za-z][A-Za-z]')
            pat = codeRegex.search(', '.join([item for item in allLines if item.startswith('Contact')]))
            pyperclip.copy(pat.group().upper())
        except AttributeError:
            info.insert('end', '\n\n---No code found---')
            noCode = True

        nameRegex = re.compile(r'(, )([A-Z])')
        dateRegex = re.compile(r'\d\d/\d\d/\d\d\d\d')
        name = nameRegex.search(', '.join([item for item in allLines if item.startswith('Contact')]).title())
        nameLet = str(name.group(2)).upper() + '*'
        date = dateRegex.search(', '.join([item for item in allLines if item.startswith('Contact')]))
        if noCode == True:
            pyperclip.copy(date.group())

        info.insert('end', '\n\n')
        info.insert('end', nameLet)
        info.insert('end', '\n\n')
        info.insert('end', date.group())
    except:
        info.insert('end', '\n\n')
        info.insert('end', 'INCORRECT INPUT')        


# Create a window frame with two buttons, one for each function
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

# After closing the window, create a file
wb = openpyxl.Workbook()
sheet = wb.active

# Set column dimensions
sheet.column_dimensions['A'].width = 40
sheet.column_dimensions['B'].width = 20
sheet.column_dimensions['C'].width = 20
sheet.column_dimensions['D'].width = 15
sheet.column_dimensions['E'].width = 30
sheet.column_dimensions['F'].width = 15

# Populate the file with information of new patient registrations
where = 1
for n in range(len(npr_name)):
    sheet.cell(row=where, column=1).value = 'Patient'
    sheet.cell(row=where, column=2).value = npr_name[n]
    sheet.cell(row=where, column=3).value = npr_lastname[n]
    sheet.cell(row=where, column=4).value = npr_date[n]
    sheet.cell(row=where, column=5).value = npr_address[n]
    sheet.cell(row=where, column=6).value = npr_postcode[n]

    sheet.cell(row=where + 2, column=1).value = npr_gp[n]
    sheet.cell(row=where + 2, column=2).value = npr_gp_code[n]
    where = where + 4

wb.save('NPRS.xlsx')
wb.close()

