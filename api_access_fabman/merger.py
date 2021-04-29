

class Merger_Charges:
    def get_short_list(self, charges_org):
        #print ('Merging Charges')
        #create a "list" of Invoice Numbers
        invoice_numbers = []
        for charge in charges_org:
            invoice_numbers.append(charge.purchaseOrder)

        #keep only unique Entries -> we have a list of uniqe Invoice Numbers!
        invoice_numbers = set(invoice_numbers)

        #sort charges_org to Invoice numbers
        shortInvoices=[]
        charge_buffer = charges_org[0]
        #try:
        for unique_invoice in invoice_numbers:
            invoiceX = []
            #sort charge Items within the same invoice an store them in invoiceX
            for charge in charges_org:
                if charge.purchaseOrder == unique_invoice:
                    #customer_charge[i].append(charge)
                    invoiceX.append(charge)
            #get a List of unique item Descriptions within invoiceX and store them in uniqueDescriptions. Remove double entries with "set"
            uniqueDescriptions = []
            for charge in invoiceX:
                uniqueDescriptions.append(charge.itemHeader)
            uniqueDescriptions = set(uniqueDescriptions)
            shortInvoice=[]
            for uniqueDescription in uniqueDescriptions:

                amount=0

                for charge in invoiceX:
                    #print('comp unique: '+uniqueDescription+' comp: '+charge.itemHeader)
                    if charge.itemHeader == uniqueDescription:
                        amount+=float(charge.netPrice)
                        short_charge=charge
                        short_charge.netPrice=round(amount,2)
                        #print(short_charge.itemHeader+' : '+str(short_charge.netPrice))
                shortInvoices.append(short_charge)
            #shortInvoices.append(shortInvoice)


        return shortInvoices