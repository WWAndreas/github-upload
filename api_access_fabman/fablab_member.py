from send_email import email


class Member:

    kind = 'Maker'         # class variable shared by all instances

    def __init__(self, id, firstname, lastname):
        self.id = id   # instance variable unique to each instance
        self.firstname = firstname
        self.lastname = lastname

    def __init__(self, session, fabman_id):
        sender = email()
        self.has_billingAddress=False
        url = str("https://fabman.io/api/v1/members/" + str(fabman_id))
        result = session.get(url)
        memberdata = result.json()
        self.id = fabman_id
        self.email = memberdata['emailAddress']
        self.address  = str(memberdata['address'])
        if memberdata['address2']:
            self.address+=' '
            self.address += str(memberdata['address2'])
        self.city = memberdata['city']
        self.zip = memberdata['zip']
        self.country = memberdata['countryCode']
        self.firstname = memberdata['firstName']
        self.lastname = memberdata['lastName']

        self.company = memberdata['company']
        if not self.company:
            self.company=' '
        self.billingAddress= str(memberdata['billingAddress'])
        if memberdata['billingAddress2']:
            self.billingAddress+= ' '
            self.billingAddress += str(memberdata['billingAddress2'])
        self.billingCity = memberdata['billingCity']
        self.billingZip = memberdata['billingZip']
        self.billingCompany = memberdata['billingCompany']
        if not self.billingCompany:
            self.billingCompany=' '
        self.billingEmail = memberdata['billingEmailAddress']
        self.billingFirstName = memberdata['billingFirstName']
        self.billingLastName = memberdata['billingLastName']
        self.billingCountry = memberdata['billingCountryCode']
        if self.billingFirstName and self.billingLastName:
            self.has_billingAddress=True

        try:
            self.sap = memberdata['metadata']['SAP']
        except:
            if self.has_billingAddress:
                namelist = {
                    'firstName': memberdata['billingFirstName'],
                    'lastName': memberdata['billingLastName'],
                    'address': self.billingAddress,
                    'city': self.billingCity,
                    'ZIP': self.billingZip,
                    'country': self.billingCountry,
                    'email': self.email,
                    'company': self.company
                }
            else:
                namelist={
                    'firstName':memberdata['firstName'],
                    'lastName': memberdata['lastName'],
                    'address':self.address,
                    'city': self.city,
                    'zip': self.zip,
                    'country': self.country,
                    'email': self.email,
                    'company': self.company
                }
            #sender.send_SAP_request(namelist)
            sender.add_sap_request(namelist)
            self.sap = ' '

    def add_email(self, email):
        self.email = email

    def add_address(self, address):
        self.address = address

    def add_city(self, city):
        self.city = city

    def add_zip(self, zip):
        self.zip = zip

    def add_country(self, country):
        self.country = country

    def add_company(self, company):
        self.company = company

    def add_phone(self, phone):
        self.phone = phone

    def add_sap(self, sap):
        self.sap = sap

    def add_dataset(self, data):
        self.dataset = data

    def add_charges(self, charges):
        self.charges = charges

#-------------------------

    def has_billingAddress(self, hasBillingAddress):
        self.hasBillingAdress = hasBillingAddress

    def add_billingemail(self, email):
        self.billingemail = email

    def add_billingFirstName(self, firstname):
        self.billingFirstName = firstname

    def add_billingLastName(self, lastname):
        self.billingLastName = lastname

    def add_billingaddress(self, address):
        self.billingAddress = address

    def add_billingcity(self, city):
        self.billingCity = city

    def add_billingzip(self, zip):
        self.billingZip = zip

    def add_billingEmail(self, email):
        self.billingEmail = email

    def __str__(self):
        return self