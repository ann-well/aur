import tkinter as tk
import re, pyperclip, openpyxl
wb = openpyxl.Workbook()
sheet = wb.active
sheet.column_dimensions['A'].width = 40
sheet.column_dimensions['B'].width = 20
sheet.column_dimensions['C'].width = 20
sheet.column_dimensions['D'].width = 20
sheet.column_dimensions['E'].width = 30
sheet.column_dimensions['F'].width = 20


window = tk.Tk()
info = tk.Text(fg="white", bg="black", width=60, height=20)
info.pack()

def addInput():
    allLines = info.get('1.0', 'end').split('\n')
    num = int(len(allLines)) - 2
    info.insert('end', '\n')
    info.insert('end', num)
    
    for i in range(0, num, 3):
        patient = allLines[i]
        gp = allLines[i+1]
        patRegex = re.compile(r'(Contact not matched: )(.*?)(, )+(.*?)(, )+(\d\d/\d\d/\d\d\d\d)+(, .*?, )+([A-Z][A-Z]\d* \d*[A-Z][A-Z])+')

        pat = patRegex.search(patient)
        name = pat.group(2).title()
        lastname = pat.group(4).title()
        date = pat.group(6)
        code = pat.group(8)

        gpRegex = re.compile(r'(Prescribing Account does not match: )+(.*, )+([A-Z][A-Z]\d+ \d+[A-Z][A-Z])+')
        gpCode = gpRegex.search(gp)

        print(name, lastname, date, code)
        print(gpCode.group(2))
        print(gpCode.group(3))
        sheet.cell(row=i+1, column =1).value = 'Patient'
        sheet.cell(row=i+1, column =2).value = name
        sheet.cell(row=i+1, column =3).value = lastname
        sheet.cell(row=i+1, column =4).value = date
        sheet.cell(row=i+1, column =5).value = pat.group(7)
        sheet.cell(row=i+1, column =6).value = code

        sheet.cell(row=i+2, column =1).value = gpCode.group(2).title()
        sheet.cell(row=i+2, column =2).value = gpCode.group(3)
        
    wb.save('NPRS.xlsx')


addButton = tk.Button(window,
text = "ENTER", 
command = addInput)
addButton.pack()

window.mainloop()

