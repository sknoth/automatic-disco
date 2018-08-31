# -*- coding: utf-8 -*-
import json
import pyrebase 
import xlrd
import datetime
    
config = {  
    "apiKey": "AIzaSyAAKwkmfHfHMDBUq4pIZpdEBR3kAfF5HUc",  
    "authDomain": "automatic-disco.firebaseapp.com",  
    "databaseURL": "https://automatic-disco.firebaseio.com", 
    "storageBucket": "automatic-disco.appspot.com", 
    "serviceAccount": "data/My Project 96139-d056a3c80700.json",
    "projectId": "automatic-disco",
    "messagingSenderId": "473031467657"
} 

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("stefanie.knoth@gmail.com", "passForThisApp123")
db = firebase.database()

workbook = xlrd.open_workbook('data/diabetes_august_2017.xlsx')
sheet = workbook.sheet_by_index(0)

def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False
    
results = []
dates = []
keys = []
for row1 in range(5, sheet.nrows-68): 

    date = datetime.datetime.strptime(sheet.row(row1)[0].value.split(',')[0], '%Y-%m-%d').strftime('%m/%d/%y')

    for row2 in range(5, sheet.nrows-68):
        
        if date == datetime.datetime.strptime(sheet.row(row2)[0].value.split(',')[0], '%Y-%m-%d').strftime('%m/%d/%y'):
            
            dates.append(date)
            keyw = sheet.row(row2)[4].value
            keys.append(keyw)

            for row3 in range(5, sheet.nrows-68):
                
                value = 1
               
                if date == datetime.datetime.strptime(sheet.row(row3)[0].value.split(',')[0], '%Y-%m-%d').strftime('%m/%d/%y') and keyw == sheet.row(row3)[4].value:                    
                
                    item = next((item for item in results if item["key"] == keyw and item["date"] == date), None)
                    
                    if item == None:
                        results.append({"date":date,"key":keyw,"value":value})
                    else:
                        item["value"] = item["value"] + 1

dates = set(dates)
keys = set(keys)
print(dates)
print(keys)
print('------------------------')


for k in keys:
    print(k)
    
    for d in dates:
        print(d,k)
        
        item = next((item for item in results if item["key"] == k and item["date"] == d), None)
        
        if item == None:
            results.append({"date":d,"key":k,"value":0})


with open('data/parsedkeywords.json', 'w') as fp:
   json.dump(results, fp)

#db.child("parsedkeywords").child(row).set({
#    "keywords": sheet.row(row)[4].value,
#    "time": date

print("keyword parsing done")

