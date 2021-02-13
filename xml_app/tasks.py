from xml.etree import ElementTree as ET
import requests
import smtplib
from urllib.request import urlopen
from xml.etree.ElementTree import parse
from asgiref.sync import sync_to_async
from .models import XmlData
import fileinput
from celery import Celery

app = Celery('tasks', broker='amqp://localhost')


@app.task
def xml_function(URL,oldword,newword,receiver_email):
    returnType = False
    try:
        messagetext = ""
        isErrorFromXmlStructure = True


        # Save xml to file from url
        #URL = "https://www.w3schools.com/xml/cd_catalog.xml"
        response = requests.get(URL)
        with open('downloadedxml.xml', 'wb') as file:
            file.write(response.content)
        file.close()



        # In order to check if the xml is valid or not
        tree = ET.parse('downloadedxml.xml')

        root = tree.getroot()
        xmlstr = ET.tostring(root, encoding='utf8', method='xml')


        x = ET.fromstring(xmlstr)

        if x:
            isErrorFromXmlStructure = False
            
        # If it is valid, save to the database

        # Read from url without saving
        #var_url = urlopen('https://www.w3schools.com/xml/plant_catalog.xml')
        #xmldoc = parse(var_url)

        myList = [dict((attr.tag, attr.text) for attr in el) for el in ET.fromstring(xmlstr)]

        for item in myList:
            xml_data = XmlData(xml_attributes = item)
            xml_data.save()

        replaceCounter = 0
        changedElements = []
        indices = []
        counter = 0
        for el in ET.fromstring(xmlstr):
            isChanged = False
            tempDict = {}
            for attr in el:
                if oldword in attr.text:
                    isChanged = True
                    attr.text = attr.text.replace(oldword,newword)
                    replaceCounter+=1
                    
                tempDict[attr.tag] = attr.text
                

            if isChanged:
                indices.append(counter)
                changedElements.append(tempDict)
            counter += 1

        counter = 0
        if changedElements:
            for changedElement in changedElements:
                xmlData = XmlData.objects.filter(xml_attributes = myList[indices[counter]]).first()
             
                xmlData.xml_attributes = changedElement
                xmlData.save()
                
                counter += 1
            
            messagetext = oldword + " is replaced by "+ newword  + " in " + str(replaceCounter) + " fields of " + str(len(changedElements)) + " elements out of " + str(len(myList)) + " elements"
        else:
            messagetext = "There is not any field which includes " + oldword + ". "
        
        returnType = True
        raise KeyError



    except Exception as error:
        print(error)
        #print(error)
        # Send email to the user
        if isErrorFromXmlStructure:
            messagetext = "There is a problem in the xml structure. Is it possible for you to check it? "

        sender_email = "testuygulama665@gmail.com"
        rec_email = receiver_email
        password = "Testsifre123"

        SUBJECT = "Information about xml"
        TEXT = messagetext
        
        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()
        server.login(sender_email, password)

        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
        server.sendmail(sender_email, rec_email, message)
        server.quit()

        if returnType:
            return True
        return False



#xml_function("https://www.w3schools.com/xml/simple.xml")