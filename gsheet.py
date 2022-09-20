from dataclasses import dataclass
from email.header import Header
from fileinput import filename
import time
from typing import Counter
import pygsheets
from turtle import pd
import pandas as pds
from shopr import my_departments
while True:
    global data
    data = my_departments()
    s_account = pygsheets.authorize(service_account_file= 'service_account.json')
    def gsUpdate(gBook,li):
        l = []
        Rows = "=COUNTA(Data!D$2:D)"
        iDupl = "=(COUNTA(Data!$D$2:$D))-(COUNTA(UNIQUE(Data!$D$2:$D)))"
        print('\n',gBook)
        global book
        book = s_account.open(gBook)
        sheet = book[0]
        book[1].update_value("M4",iDupl)
        book[1].update_value("N2",Rows)
        Rows = int(book[1].get_value("N2"))
        l = sheet.get_values('A2',"A"+str(Rows+1))
        #file = open('Debug.txt', 'a')
        new_matrix = []
        x = (data[li])
        for values in x:
            n = list(values.values())
            new_matrix.append(n)
        for k, j in enumerate(new_matrix):
            v = []
            v.append(str(new_matrix[k][0]))
            if v in l:
                deb ='In '+ v[0]+' - '+ str(k)
                #file.write(deb)
                f = l.index(v)
                sheet.update_row(f+2,new_matrix[k])
        for k, j in enumerate(new_matrix):
            v = []
            v.append(str(new_matrix[k][0]))
            if v not in l:
                deb ='Out '+ v[0]+' - '+ str(k)
                #file.write(deb)
                sheet.insert_rows(1, number= 1, values=None, inherit=False)
                sheet.update_row(2,new_matrix[k])
                sheet.update_row(2,new_matrix[k])
        #file.close()
        dashboard()
    #Update dashboard on Color Code sheet    
    def dashboard():
        book[1].update_value("Z1",'=FILTER(Data!A2:J, Data!F2:F = "In Warranty", Data!H2:H <> "Resolved", Data!H2:H <> "Completed")')
        book[1].update_value("D11","=COUNTA(Z1:Z)")
        book[1].update_value("D18",'=E10-D11')
        book[1].update_value("E10",'=SUBTOTAL(3,Data!F$2:F)')
        book[1].update_value("E15",'=COUNTIF(Data!H$2:H, "New")')
        book[1].update_value("F15",'=COUNTIF(Data!H$2:H, "Quote Pending")')
        book[1].update_value("G15",'=COUNTIF(Data!H$2:H, "Waiting for Parts")')
        book[1].update_value("E18",'=COUNTIF(Data!H$2:H, "Waiting on Customer")')
        book[1].update_value("F18",'=COUNTIF(Data!H$2:H, L7)')
        book[1].update_value("G18",'=Sum(COUNTIF(Data!$H$2:H, L10),COUNTIF( Data!$H$2:H, L21))')
        book[1].update_value("E21",'=Sum(COUNTIF(Data!H$2:H, L23), COUNTIF(Data!H$2:H, L14))')
        book[1].update_value("F21",'=COUNTIF(Data!H$2:H, L12)')
        book[1].update_value("G21",'=COUNTIF(Data!H$2:H, L9)')

    def to_sheet():
        gsUpdate("HHP",0)
        gsUpdate("DHA",1)
        gsUpdate("DTV",2)
    if __name__ == '__main__':
        to_sheet() 
