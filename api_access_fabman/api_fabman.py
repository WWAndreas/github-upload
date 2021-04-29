import requests
import json
import sys
import calendar
import fablab_member
import random
from merger import Merger_Charges
import time
import parpams
import charges
import datetime
from exceptions import Charge_exceptions
import send_email
from xlsx_creator import Xlsx_creator as creator

config = 'config/data.json'
log='config/consoleLogs/'

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

login_params = {
    "emailAddress": "christian.perfler@destination-wattens.at",
    "password": "xKt72dzofgia75"
}

resource_params = {
    'account': '16',
    #'member': '354',
    'order': 'desc',
    #'limit': '',
    'status': 'all'
}

member_params = {
    'account': '16',
    'embed': 'activePackages',
    'limit': '1000',
}
#https://fabman.io/api/v1/charges?limit=50&fromDateTime=2019-11-28T00%3A00&untilDateTime=2019-12-28T00%3A00&order=asc
#limit=30&fromDateTime=2019-11-28T00%3A00&untilDateTime=2019-12-27T23%3A59&order=asc
invoice_params= {
    'limit': '30',
    'fromDate':'',
    'untilDate': '',
    'order': 'asc'
}

create_charge_params={
    'account': '16',
    'untilDate': '',
    'invoiceDate': '',
    'dueDate': ''
}


data={}
randomID= str(random.randint(0,101))
#load config File (last update Date)
with open(config) as json_file:
    data = json.load(json_file)

if data['storage']['storeOutput']=='TRUE':
    log += data['storage']['lastDate']
    log += 'id'
    log += randomID
    log += '.txt'
    try:
        sys.stdout =  open(log, 'w')
    except:
        print('error creating log')

lasttime=data['storage']['lastDate']
print("last update:"+lasttime)



#create a random ID for this process, for now only used in the filename


#open session with credentials
s = requests.Session()
response = s.post('https://fabman.io/api/v1/user/login', data=login_params)


#check when was the last time we did an update
last_update=lasttime.split('-')
last_update_year=last_update[0]
last_update_month=last_update[1]
last_update_day=last_update[2]

#check until when the updates should be made
now = datetime.datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")

#Invoices should only be created once a month for the last month!
#We will create a list of month_to_invoice

list_of_month_to_invoice = []               #that's the list!
year_to_invoice = int(last_update_year)     #int year
month_to_invoice = int(last_update_month)   #init month

#create email instance
sender=send_email.email()

while year_to_invoice < int(year):
    if month_to_invoice > 12:
        month_to_invoice = 1
    while month_to_invoice <= 12:
        text=str(year_to_invoice)
        text+='-'
        if len(str(month_to_invoice)) <= 1:
            text \
                += '0'
        text+=str(month_to_invoice)
        text+='-'
        text+=str(calendar.monthrange(year_to_invoice, month_to_invoice)[1])
        list_of_month_to_invoice.append(text)
        month_to_invoice+=1
    year_to_invoice+=1

#month_to_invoice=1
while month_to_invoice < int(month):
    text = str(year_to_invoice)
    text += '-'
    if len(str(month_to_invoice)) <=1:
        text \
            += '0'
    text += str(month_to_invoice)
    text += '-'
    text += str(calendar.monthrange(year_to_invoice, month_to_invoice)[1])
    list_of_month_to_invoice.append(text)
    month_to_invoice += 1

for datum in list_of_month_to_invoice:
    print(datum)


for datum in list_of_month_to_invoice:
    print("Creating Charges for: ",datum)
    create_charge_params['untilDate']=datum
    create_charge_params['invoiceDate'] = datum
    create_charge_params['dueDate'] = now.strftime("%Y-%m-%d")
    url=str("https://fabman.io/api/v1/members/uninvoiced-charges/convert/")
    result = s.post(url, data=create_charge_params)
    #print(create_charge_params)
    job=result.json()
    #print("Answer from Server: ",job)
    datum_split=datum.split('-')
    datum_year=datum_split[0]
    datum_month = datum_split[1]
    datum_day = datum_split[2]
    fromDate  =datum_year
    fromDate +='-'
    fromDate += datum_month
    fromDate += '-01'

    untilDate  = datum
    print('FromDate: ',fromDate)
    invoice_params['fromDate']=fromDate
    invoice_params['untilDate']=untilDate
    if data['storage']['enableStorno']!='TRUE':
         invoice_params['state']='unpaid'
    invoice_params['limit']=500
    url=str("https://fabman.io/api/v1/invoices")
    time.sleep(5)
    result = s.get(url, params=invoice_params)
    invoices=result.json()
    jprint(invoices)


    #loop through the invoices and get details for each invoice
    
    invoice = []
    if len(invoices) != 0:
        for item in invoices:
            url = 'https://fabman.io/api/v1/invoices/'+str(item['id'])+'/details'
            result = s.get(url, params=invoice_params)
            jsondata=result.json()
            fabmanID = jsondata['charges'][0]['member']
            memberdata = fablab_member.Member(session=s, fabman_id=fabmanID)
            #print("Invoice "+item['number']+" of customer "+str(fabmanID))
            invoiceNumber=item['number']
            for charge in jsondata['charges']:
                invoice.append(charges.Invoice(session=s, jsonfile=charge, fabman_member=memberdata, invoice=invoiceNumber))

        #Create XLSX File, each charge is a separate Row
        #exceptor = Charge_exceptions(invoice, session=s)
        exceptor=Charge_exceptions()
        new_list=exceptor.get_excepted_list(charges_org=invoice, session=s)

        #print('###################Shortening########################')


        filename = fromDate
        filename += " until "
        filename += untilDate
        filename += " id"
        filename += randomID

        if data['storage']['shorterInvoices']=='TRUE':
            shortener = Merger_Charges()
            short_list = shortener.get_short_list(charges_org=new_list)
            writer = creator(short_list)
        else:
            writer = creator(new_list)
        writer.create_xlsx(filename)
        sender = send_email.email()
        text = "logfiles/DW_" + filename + ".xlsx"
        sender.add_attachment(text)

        #sender.send_email("logfiles/DW_2019-12-10_165132.xlsx")

#finally - check this months charges and send an xls as well (maybe there is something urgent
untilDate  = year
untilDate +='-'
untilDate += month
untilDate += '-'
untilDate += day
fromDate  = year
fromDate +='-'
fromDate += month
fromDate += '-01'
print('Only grabbing already created charges')
print('FromDate: ', fromDate)
invoice_params['fromDate'] = fromDate
invoice_params['untilDate'] = untilDate
invoice_params['limit']=500
if data['storage']['enableStorno'] != 'TRUE':
    invoice_params['state'] = 'unpaid'
url = str("https://fabman.io/api/v1/invoices")
time.sleep(5)
result = s.get(url, params=invoice_params)
invoices = result.json()
jprint(invoices)
# loop through the invoices and get details for each invoice

invoice = []
if len(invoices) != 0:
    for item in invoices:
        url = 'https://fabman.io/api/v1/invoices/' + str(item['id']) + '/details'
        result = s.get(url, params=invoice_params)
        jsondata = result.json()
        fabmanID = jsondata['charges'][0]['member']
        memberdata = fablab_member.Member(session=s, fabman_id=fabmanID)
        # print("Invoice "+item['number']+" of customer "+str(fabmanID))
        invoiceNumber = item['number']

        for charge in jsondata['charges']:
            #print(charge)
            invoice.append(
                charges.Invoice(session=s, jsonfile=charge, fabman_member=memberdata, invoice=invoiceNumber))

    # Create XLSX File, each charge is a separate Row
    # exceptor = Charge_exceptions(invoice, session=s)
    #print('###################Exceptions########################')
    exceptor = Charge_exceptions()
    new_list = exceptor.get_excepted_list(charges_org=invoice, session=s)
    # short_list
    #print('###################Shortening########################')

    # writer = creator(invoice)
    filename = fromDate
    filename += " until "
    filename += untilDate
    filename += " id"
    filename += randomID
    if data['storage']['shorterInvoices'] == 'TRUE':
        shortener = Merger_Charges()
        short_list = shortener.get_short_list(charges_org=new_list)
        writer = creator(short_list)
    else:
        writer = creator(new_list)
    writer.create_xlsx(filename)
    text = "logfiles/DW_"+filename+".xlsx"
    sender.add_attachment(text)
if data['storage']['enableEmail']=='TRUE':
    sender.send_email()
else:
    print('email disabled')


data['storage']['lastDate']=year+'-'+month+'-'+day
print(data['storage']['lastDate'])

#write Data to File (DateTime)
try:
    with open(config, 'w') as outfile:
        json.dump(data, outfile)
    print('file OK')
except:
    print('error writing File')


#todo email für alles senden!


