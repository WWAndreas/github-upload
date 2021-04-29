import xlsxwriter
import datetime
import charges
import json

import os
import errno

class Xlsx_creator:
    def __init__(self, charges):
        self.invoices=charges

    def create_xlsx(self, range=None):
        #invoices = charges
        # Create an new Excel file and add a worksheet.
        now = datetime.datetime.now()
        dir = "/logfiles"
        if range == None:
            filename = "logfiles/DW_" + now.strftime('%Y-%m-%d_%H%M%S') + ".xlsx"
        else:
            filename = "logfiles/DW_"
            filename += range
            filename +=".xlsx"
        #print(filename)

        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()

        row = 0;
        column = 0;
        columns_width = 5
        worksheet.write(row, column, 'Sales Organization')
        worksheet.set_column(row, column, columns_width)
        column += 1
        worksheet.write(row, column, 'Distribution Channel')
        worksheet.set_column(row, column, columns_width)
        column += 1
        worksheet.write(row, column, 'Division')
        worksheet.set_column(row, column, columns_width)
        column += 1
        worksheet.write(row, column, 'Sales Document Type')
        worksheet.set_column(row, column, columns_width)
        column += 1
        worksheet.write(row, column, 'Purchase order number')
        worksheet.set_column(row, column, columns_width)
        column += 1
        worksheet.write(row, column, 'Sold-to Party AG')
        worksheet.set_column(row, column, columns_width)
        column += 1
        worksheet.write(row, column, 'Ship-To Party WE')
        worksheet.set_column(row, column, columns_width)
        column += 1
        worksheet.write(row, column, 'Material')
        worksheet.set_column(row, column, columns_width)
        column += 1
        worksheet.write(row, column, 'Quantity')
        worksheet.set_column(row, column, columns_width)
        column += 1
        worksheet.write(row, column, 'ZW00')
        worksheet.set_column(row, column, columns_width)
        column += 1
        worksheet.write(row, column, 'ZWL3')
        worksheet.set_column(row, column, columns_width)
        column += 1
        worksheet.write(row, column, 'Item Description (PG95 only)')
        worksheet.set_column(row, column, columns_width)
        column += 1
        worksheet.write(row, column, 'TEXT3 VBBP-ZW25 Item line  Material-Sales text')
        worksheet.set_column(row, column, columns_width)
        column += 1
        worksheet.write(row, column, 'Cost Center')
        worksheet.set_column(row, column, columns_width)
        column += 1
        worksheet.write(row, column, 'Name 1')
        worksheet.set_column(row, column, columns_width)
        column += 1
        worksheet.write(row, column, 'Name 2')
        worksheet.set_column(row, column, columns_width)
        column += 1
        worksheet.write(row, column, 'City')
        worksheet.set_column(row, column, columns_width)
        column += 1
        worksheet.write(row, column, 'City postal code')
        worksheet.set_column(row, column, columns_width)
        column += 1
        worksheet.write(row, column, 'Street')
        worksheet.set_column(row, column, columns_width)
        column += 1
        worksheet.write(row, column, 'House Number')
        worksheet.set_column(row, column, columns_width)
        column += 1
        worksheet.write(row, column, 'Country Key')
        worksheet.set_column(row, column, columns_width)
        column += 1
        worksheet.write(row, column, 'Region')
        worksheet.set_column(row, column, columns_width)

        # write Invoice Data:
        for invoice in self.invoices:
            row += 1;
            column = 0;
            columns_width = 5
            #worksheet.write(row, column, 'Sales Organization')
            worksheet.write(row, column, '9330')
            column += 1
            #worksheet.write(row, column, 'Distribution Channel')
            worksheet.write(row, column, '01')
            column += 1
            #worksheet.write(row, column, 'Division')
            worksheet.write(row, column, '09')
            column += 1
            #worksheet.write(row, column, 'Sales Document Type')
            worksheet.write(row, column, str(invoice.salesDocumentType))
            column += 1
            #worksheet.write(row, column, 'Purchase order number')
            worksheet.write(row, column, str(invoice.purchaseOrder))
            column += 1
            #worksheet.write(row, column, 'Sold-to Party AG')
            worksheet.write(row, column, str(invoice.soldTo))
            column += 1
            #worksheet.write(row, column, 'Ship-To Party WE')
            worksheet.write(row, column, str(invoice.soldTo))
            column += 1
            #worksheet.write(row, column, 'Material')
            worksheet.write(row, column, str(invoice.materialNumber))
            column += 1
            #worksheet.write(row, column, 'Quantity')
            worksheet.write(row, column, str(invoice.quantity))
            column += 1
            #worksheet.write(row, column, 'ZW00')
            worksheet.write(row, column, str(invoice.netPrice))
            column += 1
            #worksheet.write(row, column, 'ZWL3')
            worksheet.write(row, column, '0')
            column += 1
            #worksheet.write(row, column, 'Item Description (PG95 only)')
            worksheet.write(row, column, str(invoice.itemHeader))
            column += 1
            #worksheet.write(row, column, 'TEXT3 VBBP-ZW25 Item line  Material-Sales text')
            worksheet.write(row, column, str(invoice.itemText)) #itemText not correct!
            column += 1
            #worksheet.write(row, column, 'Cost Center')
            worksheet.write(row, column, str(invoice.costCenter))
            column += 1
            #worksheet.write(row, column, 'Name 1')
            worksheet.write(row, column, str(invoice.company))
            column += 1
            #worksheet.write(row, column, 'Name 2')
            worksheet.write(row, column, str(invoice.name))
            column += 1
            #worksheet.write(row, column, 'City')
            worksheet.write(row, column, str(invoice.city))
            column += 1
            #worksheet.write(row, column, 'City postal code')
            worksheet.write(row, column, str(invoice.postalCode))
            column += 1
            #worksheet.write(row, column, 'Street')
            worksheet.write(row, column, str(invoice.street))
            column += 1
            #worksheet.write(row, column, 'House Number')
            column += 1
            #worksheet.write(row, column, 'Country Key')
            worksheet.write(row, column, str(invoice.country))
            column += 1
            #worksheet.write(row, column, 'Region')

        workbook.close()

#writer = Xlsx_creator()
#writer.create_xlsx("")
#print("done")