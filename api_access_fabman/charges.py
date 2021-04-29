import json
import fablab_member
import datetime

class Invoice:
    #conver json data to Invoice data during Init
#   def __init__(self, charge_data, session, fabman_ID):
    def __init__(self, session, jsonfile=None, fabman_member=None, invoice=None, fabman_ID=None, charge_data=None):
        if charge_data is None and fabman_ID is None:

            self.charges=[]
            if float(jsonfile['netPrice'])>0:
                self.salesDocumentType="ZWDL"
            else:
                self.salesDocumentType="ZWG2"
            now = datetime.datetime.now()
            year = now.strftime("%Y")
            self.purchaseOrder = year
            self.purchaseOrder+= '0000'
            self.purchaseOrder+=invoice
            self.soldTo=fabman_member.sap
            self.fabmanID=fabman_member.id
            #Kostenstelle und Materialnummer
            if not jsonfile['resourceLog'] and not jsonfile['memberPackage']:
                self.materialNumber=3315004     #Materialien
                self.costCenter=810011          #FabStore
            elif jsonfile['resourceLog'] and not jsonfile['memberPackage']:
                self.materialNumber=3315000     #Miete
                self.costCenter=810012          #Maschinenstunden
            elif not jsonfile['resourceLog'] and jsonfile['memberPackage']:
                self.materialNumber=3315000     #Miete
                self.costCenter=81001          #Mitgliedschaft
            else:
                self.materialNumber = 3315004  # Materialien
                self.costCenter = 810011  # FabStore
            self.quantity=1
            self.netPrice=jsonfile['netPrice']
            #Split Item Description if longer than 40 char
            description=jsonfile['description']
            if '##' in description:
                splitstring=description.split('##')
                self.itemHeader=splitstring[0]
                self.itemText=splitstring[1]
            elif ':' in description:
                splitstring = description.split(':')
                self.itemHeader = splitstring[0]
                self.itemText = splitstring[1]
            elif '{' and '}' in description:
                #convert json to object Data
                try:
                    data = json.loads(description)
                    self.itemHeader=data['Header']
                    self.itemText=data['description']
                    self.costCenter=data['Kostenstelle']
                    self.materialNumber=data['Materialnummer']
                except:
                    if len(description) > 40:
                        self.itemHeader = description[0:39]
                        self.itemText = description[39:]
                    else:
                        self.itemHeader = description
                        self.itemText = ' '
            elif len(description) >40:
                self.itemHeader=description[0:39]
                self.itemText=description[39:]
            else:
                if 'm ' and 's' and ',' in description:
                    splitstring = description.split(',')
                    self.itemHeader = splitstring[0]
                    self.itemText=' '
                    #self.itemText = splitstring[1]
                else:
                    self.itemHeader=description
                    self.itemText = ' '
            #if self.materialNumber==3315000 and self.costCenter==810012:
            #    self.itemText+=' '
            #    self.itemText+=jsonfile['dateTime']

            if fabman_member.has_billingAddress:
                self.company=fabman_member.billingCompany
                self.name=str(fabman_member.billingFirstName) + " " + str(fabman_member.billingLastName)
                self.city=fabman_member.billingCity
                self.postalCode=fabman_member.billingZip
                self.street=fabman_member.billingAddress
                self.country=fabman_member.billingCountry
            else:
                self.company = fabman_member.company
                self.name = str(fabman_member.firstname) + " " + str(fabman_member.lastname)
                self.city = fabman_member.city
                self.postalCode = fabman_member.zip
                self.street = fabman_member.address
                self.country = fabman_member.country
        else:



            self.salesDocumentType=charge_data['salesDocumentType']
            self.purchaseOrder=charge_data['purchaseOrder']
            self.materialNumber=charge_data['materialNumber']
            self.costCenter=charge_data['costCenter']
            self.quantity=charge_data['quantity']
            self.netPrice=charge_data['netPrice']
            self.itemHeader=charge_data['itemHeader']
            #self.itemHeader+='!'
            self.itemText=charge_data['itemText']

            #Option to use Fabman_ID to get the Billing Informations
            if fabman_ID is not None:
                fabman_member = fablab_member.Member(session=session, fabman_id=fabman_ID)
                self.soldTo=fabman_member.sap
                self.fabmanID=fabman_member.id
                if fabman_member.has_billingAddress:
                    self.company = fabman_member.billingCompany
                    self.name = str(fabman_member.billingFirstName) + " " + str(fabman_member.billingLastName)
                    self.city = fabman_member.billingCity
                    self.postalCode = fabman_member.billingZip
                    self.street = fabman_member.billingAddress
                    self.country = fabman_member.billingCountry
                else:
                    self.company = fabman_member.company
                    self.name = str(fabman_member.firstname) + " " + str(fabman_member.lastname)
                    self.city = fabman_member.city
                    self.postalCode = fabman_member.zip
                    self.street = fabman_member.address
                    self.country = fabman_member.country
            else:
            #Billing Information is included in charge data
                self.soldTo = charge_data['soldTo']
                #self.fabmanID = fabman_member.id
                self.company = charge_data['company']
                self.name = charge_data['name']
                self.city = charge_data['city']
                self.postalCode = charge_data['postalCode']
                self.street = charge_data['street']
                self.country = charge_data['country']
                self.email = charge_data['emailAddress']


    def salesDocumentType(self, item):
        self.salesDocumentType=item

    def purchaseOrder(self, item):
        self.purchaseOrder=item

    def soldTo(self, item):
        self.soldTo=item
        self.shipTo=item

    def materialNumber(self, item):
        self.materialNumber=item

    def quantity(self, item):
        self.quantity=item

    def netPrice(self, item):
        self.netPrice=item

    def itemHeader(self, item):
        self.itemHeader=item

    def itemText(self, item):
        self.itemText=item

    def costCenter(self, item):
        self.costCenter=item

    def company(self, item):
        self.comapny=item

    def name(self, item):
        self.name=item

    def city(self, item):
        self.city=item

    def postalCode(self, item):
        self.postalCode=item

    def street(self, item):
        self.street=item

    def country(self, item):
        self.country=item







