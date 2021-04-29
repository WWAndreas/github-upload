import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from string import Template
import sys


class email:

    sap_namelist = []
    email_attachment_list = []

    def __init__(self, config="config/email.json", message_path="config/message.txt"):
        self.config=config
        self.message_path=message_path
        self.read_config()
        self.read_message()

    def read_config(self):
        self.names = []
        self.emails = []
        with open(self.config, mode='r', encoding='utf-8') as contacts_file:
            json_contacts = json.load(contacts_file)
            for item in json_contacts['email']:
                self.names.append(item)
                self.emails.append(json_contacts['email'][item])

    def read_message(self):
        with open(self.message_path, mode='r', encoding='utf-8') as message_file:
            self.message = message_file.read()

    def add_attachment (self, attachment):
        self.email_attachment_list.append(attachment)

    def send_email(self):
        #read contacts from file
        try:
            s = smtplib.SMTP(host='smtp.office365.com', port='587')
            s.ehlo()
            s.starttls()
            s.login('host@destination-wattens.at', 'Fafu4446')
            #mailserver.sendmail('user@company.co', 'user@company.co', 'python email')
            print("SMTP OK")

            for item in self.emails:
                print("item: "+item)
                msg = MIMEMultipart()
                message = self.message
                msg['From'] = 'host@destination-wattens.at'
                msg['To'] = item
                msg['Subject'] = "Aktuelle Buchungen"
                msg.attach(MIMEText(message, 'plain'))
                if len(self.email_attachment_list)>0:
                    for xls_filepath in self.email_attachment_list:
                        with open(xls_filepath, "rb") as fil:
                            print("file is open")
                            part = MIMEApplication(
                                fil.read(),
                                Name="xls_filepath"
                            )
                        # After the file is closed
                        part['Content-Disposition'] = 'attachment; filename='+xls_filepath
                        print("Adding ",xls_filepath," to email")
                        msg.attach(part)

                #print("Message to "+item)
                s.send_message(msg)
                #s.sendmail('host@destination-wattens.at', item, 'Hi Chris')
                #print("sent to: "+item)
                del msg
            if len(self.sap_namelist) > 0:
                print('sending SAP request')
                self.send_SAP_request()
            s.quit()
        except Exception as e:
            print("error sending email")
            print ('error: ',str(e))



    def send_SAP_request(self):
        try:
            s = smtplib.SMTP(host='smtp.office365.com', port='587')
            s.ehlo()
            s.starttls()
            s.login('host@destination-wattens.at', 'Fafu4446')
            #mailserver.sendmail('user@company.co', 'user@company.co', 'python email')
            print("SMTP OK")
            #print(member_data['firstName'])
            #print(member_data['lastName'])


            for item in self.emails:
                print("item: "+item)
                msg = MIMEMultipart()
                message = "Missing SAP number - please add in fabman.io: \n"
                for member_data in self.sap_namelist:

                    message+= 'First Name: '
                    message+= str(member_data['firstName'])
                    message+= '\nLastName: '
                    message+= str(member_data['lastName'])
                    message += '\nemail: '
                    message += str(member_data['email'])
                    message += '\nCompany: '
                    message += str(member_data['company'])
                    message += '\nAddress: '
                    message += str(member_data['address'])
                    message += '\nCity: '
                    message += str(member_data['city'])
                    message += '\nZIP: '
                    message += str(member_data['zip'])
                    message += '\nCountry: '
                    message += str(member_data['country'])
                    message += '\n-----------------------------\n'
                msg['From'] = 'host@destination-wattens.at'
                msg['To'] = item
                msg['Subject'] = "SAP Number required"
                msg.attach(MIMEText(message, 'plain'))
                # After the file is closed
                print("Message to "+item)
                s.send_message(msg)
                #s.sendmail('host@destination-wattens.at', item, 'Hi Chris')
                print("sent to: "+item)
                del msg

            s.quit()
        except:
            print("error sending SAP email")
            print("Unexpected error:", sys.exc_info()[0])

    def add_sap_request(self, data):
        self.sap_namelist.append(data)
        #print("Name added to namelist")

