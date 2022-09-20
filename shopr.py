from hashlib import new
from multiprocessing.sharedctypes import Value
from urllib import response
from webbrowser import get
from wsgiref import headers
from mytoken import my_keys
from datetime import datetime
import requests

def set_up(keys):
    tickets = []
    today = str(datetime.today())
    today = today[:11]
    _key = keys
    i='2022-09-10'
    for j in range(1,10):
        my_url = 'https://allelectronics.repairshopr.com/api/v1/tickets?since_updated_at='+today+'&page='+str(j)
        global headers
        headers = {    
            'Accept': 'application/json',  
            'Content-Type': 'application/json',
            'Authorization': 'Token '+_key
            }
        response = requests.get(my_url, headers= headers, verify= True)
        ticket = response.json()
        tickets.extend(ticket.get('tickets'))
    return tickets
def ticket_id():
    id_list = []
    tickets = set_up(my_keys().get('_key'))
    for x,i in enumerate(tickets):
        id_list.append(i.get('id'))
    return id_list

def get_ticket():
    ids = ticket_id()
    hhp_data, dtv_data, home_data, bOffice_data, parts_data  = [], [], [], [],[]
    for x in range(len(ids)):
        my_url = 'https://allelectronics.repairshopr.com/api/v1/tickets/'+str(ids[x])
        response = requests.get(my_url, headers= headers, verify= True)
        ticket_data = response.json() 
        #print((len(ids)-x))
        print("/",end='')
        ticket_data = ticket_data.get('ticket')
        #print(ticket_data)
        ticket_data = ticket_data.values()
        ticket_data = list(ticket_data)
        #print(ticket_data)
        try:
            assets = list((ticket_data[31][0]).values())
            model, sn = assets[1], assets[8]
        except:
            model, sn = "None", "None"
        nums = (ticket_data[1])
        """ if nums == None:
            nums = (ticket_data[12]).get('Service Order No. ') #'Service Order No.'
            if nums == None:
                nums = (ticket_data[12]).get('Service Order No.') """
        status = ticket_data[11]
        Warr = ticket_data[38]
        cDate = ((ticket_data[3]))
        cDate = cDate.replace('T',' ')
        cDate = cDate[0:-10]
        #cDate = datetime.strptime(cDate, '%Y-%m-%d %H:%M:%S')
        uDate = ((ticket_data[14]))
        uDate = uDate.replace('T',' ')
        uDate = uDate[0:-10]
        #uDate = datetime.strptime(uDate, '%Y-%m-%d %H:%M:%S')
        dur = '=DAYS(TODAY(),INDIRECT(CONCAT("D", ROW())))'
        dep = ticket_data[10]
        Cust = ticket_data[5]
        try:
            Warr = Warr.get('name')
        except:
            Warr = 'None'
        tmpData = {          
            'Job_ID': nums,               #5
            'Model': model,
            'SN': sn,             
            'Date Created': cDate,      #3
            'Last Updated': uDate,      #14
            'Warranty' : Warr,          #
            'Department': dep,          #10
            'Status': status, 
            'Reason': '',
            'Duration': dur,
            'Customer' :  Cust
            #'Main Date' : ''       #11
                    
        }  
        tmp = tmpData.get('Department')
        if tmp[:3] == 'HHP' or (tmp[:3] == 'MTN'):
            hhp_data.append(tmpData)
        elif (tmp == 'In Home Appliances') or (tmp == 'Home Appliance'):
            home_data.append(tmpData)
            #print(tmpData.values())
        elif (tmp == 'Computer') or (tmp == 'Audio') or (tmp[:3] == 'DTV') or (tmp[-2:] == 'TV') or (tmp == 'Monitor'):
            dtv_data.append(tmpData)
        """ elif tmp == 'Part Sales':
            parts_data.append(tmpData)
        else:
            bOffice_data.append(tmpData)  """
    #print(tmp)
    return hhp_data, home_data, dtv_data, parts_data, bOffice_data
#get_ticket()
def my_departments():
    departments = get_ticket()
    return departments
