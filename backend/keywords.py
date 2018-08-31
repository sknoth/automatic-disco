# -*- coding: utf-8 -*-

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

for row in range(5, sheet.nrows-68): 

    db.child("keywords").child(row).set({
            "keywords": sheet.row(row)[4].value,
            "time": datetime.datetime.strptime(sheet.row(row)[0].value.split(',')[0], '%Y-%m-%d').strftime('%m/%d/%y')
            }, user['idToken'])

print("keyword parsing done")

