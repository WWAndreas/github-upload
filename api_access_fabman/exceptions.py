import json

from charges import Invoice
config = 'config/exception.json'

#wichtige Variablen:
# customer_charges [[],[]] - ["Customer" - {0,1,2,... not an ID String][charges]
# customer_exception {'customer':'Exception'} - aus "data"
# data - json import aus config/exception data['DSW']['package'][0],...
class Charge_exceptions:



    #def __init__(self, charges_org, session):

    def get_excepted_list(self, charges_org, session):
        data = {}
        #charges_new=charges_org
        charges_new=[]
        # load config File (last update Date)
        with open(config) as json_file:
            data = json.loads(json_file.read())

        #create a "list" of Customers
        customer = []
        for charge in charges_org:
            customer.append(charge.fabmanID)

        #keep only unique Entries -> we have a list of uniqe Customers!
        customer = set(customer)

        #sort charges_org to unique customers
        customer_charge=[]
        charge_buffer = charges_org[0]
        #try:
        for unique_customer in customer:
            customerX = []
            for charge in charges_org:
                if charge.fabmanID == unique_customer:
                    #customer_charge[i].append(charge)
                    customerX.append(charge)

            customer_charge.append(customerX)
        #except Exception as e:
        #    print('Exception after Customer ',i)
        #    print(str(e))
        #    print(charge_buffer)

        #let's do something with this list....
        customer_exception = {}
        for customer in customer_charge:
            exception_type=''
            #check if this Customer qualifies for an exception
            for charges_org in customer:
                description = charges_org.itemHeader
                description+= charges_org.itemText
                #Iterate Execptions ("ex") aus der Exception.json File
                for ex in data:
                    #Iterate Exception Data (DSW,...)
                    for ex_packages in data[ex]['package']:
                        #Vergleiche alle Buchungszeilen
                        if ex_packages in description:
                            #print('exception!')
                            exception_type=ex
            #create a dictionary with all Customers with exceptions and the type of the exception
            if exception_type is not '':
                customer_exception[customer[0].fabmanID]=str(exception_type)

        counter=0
        for customer, exception in customer_exception.items():
            #print("Counter: ",counter," Customer: ",customer," Paid for: ",exception)
            counter+=1
            #invoice_exceptions.append(customer)

        #Move charges_org of exception customers from the original to a temporary storage and remove them from the original list
        invoice_exceptions = []

        i=0
        for customer in list(customer_charge):      #iterating over a copy of the list, otherwise changing the original is not possible
            exception=False
            j=0
            k=0
            customerX = []
            for charge in customer:

                if charge.fabmanID in customer_exception:
                    #If Customer is excepted move charge to storage for further processing
                    exception=True
                    #invoice_exceptions[i].append(charge)
                    customerX.append(charge)
                    k+=1
                else:
                    #Or move it in the new export container
                    charges_new.append(charge)
                    j+=1
            if len(customerX) > 0:
                invoice_exceptions.append(customerX)
            #print("excepted charges: ", k)
            #print("unexcepted charges: ", j)
            if exception:
                customer_charge.remove(customer)
                i += 1

        #print("---------------")
        #print("separating Costs")
        #Aufteilen der Kosten
        #invoice_number_payer=invoice_exceptions[0][0].purchaseOrder
        invoice_number_payer={}
        #print('Invoicenumber for Payer:', invoice_number_payer)


        for customer in invoice_exceptions:
            #print('Customer: ', customer)
            id=customer[0].fabmanID
            #print("ID: ", id)
            customer_name = customer[0].name
            customer_sap = customer[0].soldTo
            customer_company = customer[0].company
            customer_city = customer[0].city
            customer_postalCode = customer[0].postalCode
            customer_street = customer[0].street
            customer_country = customer[0].country
            customer_purchaseOrder = customer[0].purchaseOrder

            ex=customer_exception[id]
            if ex not in invoice_number_payer:
                invoice_number_payer[ex]=customer[0].purchaseOrder
            payable_membership_amount = data[ex]['amountformembership']
            payable_booking_amount = data[ex]['amountforbookings']
            charged_membership_amount = 0
            charged_booking_amount=0
            booking_text=[]
            membership_text=[]
            for charge in list(customer):
                customer_name=charge.name
                #id=charge.fabmanID
                #print('CostCenter ',charge.costCenter, ' Material ',charge.materialNumber, ' Item Text: ',charge.itemHeader)
                # -------------------------------------
                # Check if costtype is a membership
                membership = False
                for paid_package in data[ex]['package']:
                    if charge.costCenter == 81001 and charge.materialNumber == 3315000 and paid_package in charge.itemHeader:
                        #print('this is a membership')
                        membership = True
                        #text= customer_name
                        #text+=' '
                        text=charge.itemHeader
                        text+=charge.itemText
                        #print('####',charge.itemHeader)
                        #print('####', charge.itemText)
                        membership_text.append(text)
                if membership:
                    charged_membership_amount += float(charge.netPrice)
                    customer.remove(charge)
                #-------------------------------------
                #Check if costtype is a booking
                if charge.costCenter == 810012 and charge.materialNumber == 3315000:
                    #print('this is a booking')
                    charged_booking_amount += float(charge.netPrice)
                    #text = customer_name
                    text = charge.itemHeader
                    text += charge.itemText
                    text+=' '
                    booking_text.append(text)
                    customer.remove(charge)
                #-------------------------------------

                #Was passiert mit den Übrigen Buchungen?
                #Wie kann der Buchungstext erhalten bleiben

            #print('Customer: ',customer_name,' ',id,' charged Memberships:', charged_membership_amount)
            #print('Customer: ',customer_name,' ', id, ' charged Bookings:', charged_booking_amount)
            #print('---------------------------------------')
            #-------------------------------------------
            #split the amount between payer and customer
            #case 1 membership is cheaper than max amount -> all is paid by "payer"
            charge_to_payer=0
            charge_to_customer=0
            header_customer=''
            header_payer=''

            charge_data={}
            #print(customer)
            if float(charged_membership_amount) <= float(payable_membership_amount):
                #Payer is paying the (Membership-) bill alone
                text_customer = ''
                text_payer = ''
                charge_to_payer=charged_membership_amount
                header_payer='Membership(s) of '
                header_payer+=customer_name
                for item in membership_text:
                    text_payer+=item
                    text_payer+=' '
                charge_data['salesDocumentType']='ZWDL'
                charge_data['soldTo']           = data[ex]['charge_to']['costCenter']
                charge_data['purchaseOrder']    =invoice_number_payer[ex]
                charge_data['materialNumber']   ='331500'
                charge_data['costCenter']       ='81001'
                charge_data['quantity']         ='1'
                charge_data['netPrice']         =round(charge_to_payer,2)
                charge_data['itemHeader']       =header_payer
                charge_data['itemText']         =text_payer
                charge_data['company']          =data[ex]['charge_to']['company']
                charge_data['name']             =data[ex]['charge_to']['name']
                charge_data['city']             =data[ex]['charge_to']['city']
                charge_data['postalCode']       =data[ex]['charge_to']['ZIP']
                charge_data['street']           =data[ex]['charge_to']['address']
                charge_data['country']          =data[ex]['charge_to']['country']
                charge_data['emailAddress']     =data[ex]['charge_to']['email']
                charges_new.append(Invoice(session=session, fabman_ID=None, fabman_member=None, charge_data=charge_data))

            else:
                #Customer and Payer split the membership fee
                text_customer = ''
                text_payer = ''
                charge_to_payer = float(payable_membership_amount)
                charge_to_customer = charged_membership_amount - charge_to_payer
                header_payer = 'Membership(s) of '
                header_payer += customer_name
                header_customer = 'Membership (not paid by '
                header_customer +=ex
                header_customer +=")"

                for item in membership_text:
                    text_payer += item
                    text_payer += ' '
                #Payer charge:
                charge_data['salesDocumentType'] = 'ZWDL'
                charge_data['soldTo'] = data[ex]['charge_to']['costCenter']
                charge_data['purchaseOrder'] = invoice_number_payer[ex]
                charge_data['materialNumber'] = '331500'
                charge_data['costCenter'] = '81001'
                charge_data['quantity'] = '1'
                charge_data['netPrice'] = round(charge_to_payer,2)
                charge_data['itemHeader'] = header_payer
                charge_data['itemText'] = text_payer
                charge_data['company'] = data[ex]['charge_to']['company']
                charge_data['name'] = data[ex]['charge_to']['name']
                charge_data['city'] = data[ex]['charge_to']['city']
                charge_data['postalCode'] = data[ex]['charge_to']['ZIP']
                charge_data['street'] = data[ex]['charge_to']['address']
                charge_data['country'] = data[ex]['charge_to']['country']
                charge_data['emailAddress'] = data[ex]['charge_to']['email']
                charges_new.append(Invoice(session=session, fabman_ID=None, fabman_member=None, charge_data=charge_data))
                #customer charge:
                # customer charge:
                charge_data = {}
                charge_data['salesDocumentType'] = 'ZWDL'
                charge_data['purchaseOrder'] = customer_purchaseOrder
                charge_data['soldTo'] = customer_sap
                charge_data['materialNumber'] = '331500'
                charge_data['costCenter'] = '81001'
                charge_data['quantity'] = '1'
                charge_data['netPrice'] = round(charge_to_customer,2)
                charge_data['itemHeader'] = header_customer
                charge_data['itemText'] = text_customer
                charge_data['company'] = customer_company
                charge_data['name'] = customer_name
                charge_data['city'] = customer_city
                charge_data['postalCode'] = customer_postalCode
                charge_data['street'] = customer_street
                charge_data['country'] = customer_country
                charge_data['emailAddress'] = ' '
                charges_new.append(Invoice(session=session, charge_data=charge_data))
            #Here starte the bookings!
            if float(charged_booking_amount) <= float(payable_booking_amount) and float(charged_booking_amount) > 0:
                # Payer is paying the (Booking-) bill alone
                text_payer=''
                text_customer=''
                for item in booking_text:
                    text_payer+=item
                    text_payer+=' '
                charge_to_payer = charged_booking_amount
                header_payer = 'Bookings of '
                header_payer += customer_name
                charge_data['salesDocumentType'] = 'ZWDL'
                charge_data['soldTo'] = data[ex]['charge_to']['costCenter']
                charge_data['purchaseOrder'] = invoice_number_payer[ex]
                charge_data['materialNumber'] = '331500'
                charge_data['costCenter'] = '81001'
                charge_data['quantity'] = '1'
                charge_data['netPrice'] = round(charge_to_payer,2)
                charge_data['itemHeader'] = header_payer
                charge_data['itemText'] = text_payer
                charge_data['company'] = data[ex]['charge_to']['company']
                charge_data['name'] = data[ex]['charge_to']['name']
                charge_data['city'] = data[ex]['charge_to']['city']
                charge_data['postalCode'] = data[ex]['charge_to']['ZIP']
                charge_data['street'] = data[ex]['charge_to']['address']
                charge_data['country'] = data[ex]['charge_to']['country']
                charge_data['emailAddress'] = data[ex]['charge_to']['email']
                charges_new.append(
                    Invoice(session=session, fabman_ID=None, fabman_member=None, charge_data=charge_data))
                charge_data={}

            if float(charged_booking_amount) > float(payable_booking_amount):
                #Customer and Payer split the booking fee
                text_customer = ''
                text_payer = ''
                charge_to_payer = float(payable_booking_amount)
                charge_to_customer = charged_booking_amount - charge_to_payer
                header_payer = 'Booking(s) of '
                header_payer += customer_name
                header_customer = 'Bookings (not paid by '
                header_customer +=ex
                header_customer +=")"

                for item in booking_text:
                    text_payer += item
                    text_payer += ' '
                #Payer charge:
                charge_data['salesDocumentType'] = 'ZWDL'
                charge_data['soldTo'] = data[ex]['charge_to']['costCenter']
                charge_data['purchaseOrder'] = invoice_number_payer[ex]
                charge_data['materialNumber'] = '331500'
                charge_data['costCenter'] = '81001'
                charge_data['quantity'] = '1'
                charge_data['netPrice'] = round(charge_to_payer,2)
                charge_data['itemHeader'] = header_payer
                charge_data['itemText'] = text_payer
                charge_data['company'] = data[ex]['charge_to']['company']
                charge_data['name'] = data[ex]['charge_to']['name']
                charge_data['city'] = data[ex]['charge_to']['city']
                charge_data['postalCode'] = data[ex]['charge_to']['ZIP']
                charge_data['street'] = data[ex]['charge_to']['address']
                charge_data['country'] = data[ex]['charge_to']['country']
                charge_data['emailAddress'] = data[ex]['charge_to']['email']
                charges_new.append(Invoice(session=session, fabman_ID=None, fabman_member=None, charge_data=charge_data))
                #customer charge:
                # customer charge:
                charge_data = {}
                charge_data['salesDocumentType'] = 'ZWDL'
                charge_data['purchaseOrder'] = customer_purchaseOrder
                charge_data['soldTo'] = customer_sap
                charge_data['materialNumber'] = '331500'
                charge_data['costCenter'] = '81001'
                charge_data['quantity'] = '1'
                charge_data['netPrice'] = round(charge_to_customer,2)
                charge_data['itemHeader'] = header_customer
                charge_data['itemText'] = text_customer
                charge_data['company'] = customer_company
                charge_data['name'] = customer_name
                charge_data['city'] = customer_city
                charge_data['postalCode'] = customer_postalCode
                charge_data['street'] = customer_street
                charge_data['country'] = customer_country
                charge_data['emailAddress'] = ' '
                charges_new.append(Invoice(session=session, charge_data=charge_data))
        #print('done')
        #print (invoice_number_payer)
        return charges_new

    #todo item text - Bookings appear in Membership charges (Item Description)

