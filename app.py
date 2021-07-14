from flask import Flask, render_template, request
import sqlite3
import textwrap
import pyodbc
import time
import os
import redis
import hashlib
import pickle
from pymongo import MongoClient 

app = Flask(__name__)


driver = '{ODBC Driver 17 for SQL Server}'
server_name = 'assign1server'
database_name = 'assignment1'
server = 'tcp:database.windows.net,1433'
username = "saitheja"
password = "9705004946S@i"

client = MongoClient("mongodb+srv://theja:sai1234@cluster0.zkyxl.mongodb.net/Assignment3?retryWrites=true&w=majority")
collec = client.Assignment3.Collection3

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/search')
def search():
   return render_template('search.html')
@app.route('/searchrange')
def updatemain():
   return render_template('searchrange.html')


@app.route('/searchloc')
def deletemain():
   return render_template('searchloc.html')





@app.route('/mag', methods=['POST','GET'])
def list():
    field=request.form['mag']
    f=float(field)
    count=collec.find({"mag":{"$gt":f}}).count()
    print(count)
    
    return render_template("newlist.html",count=count)



@app.route('/rangesearch',methods=['POST','GET'])
def rangesearch():
    mag1=float(request.form['mag1'])
    mag2=float(request.form['mag2'])
   
    count=collec.find({"mag":{"$gt":mag1,"$lt":mag2}}).count()
    row_new=collec.find({"mag":{"$gt":mag1,"$lt":mag2}})
    rows=[]
    for row in row_new:
        arr1=[]
        arr1.append(row['place'])
        arr1.append(row['time'])
        arr1.append(row['mag'])
        rows.append(arr1)

    return render_template("list.html",rows = rows,count=count)



@app.route('/locsearch',methods=['POST','GET'])
def locsearch():
    place=request.form['place']
    kms=request.form['kms']
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    querry="SELECT id,time,latitude,longitude,depth,mag,place,type,magSource FROM all_month where place like '%"+place+"' and place like '%km%' and CAST(left(place, (charindex('k', place)-1)) AS int)<='"+kms+"'"
    crsr.execute(querry)
    rows = crsr.fetchall()
    q2="SELECT count(*) FROM all_month where place like '%"+place+"' and place like '%km%' and CAST(left(place, (charindex('k', place)-1)) AS int)<='"+kms+"'"
    crsr.execute(q2)
    count=crsr.fetchone()
    print(count)
    cnxx.close()
    return render_template("list.html",rows = rows,count=count)


@app.route('/cluster',methods=['POST','GET'])
def cluster():
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    querry="SELECT mag,COUNT(*) FROM all_month  group by mag"
    crsr.execute(querry)
    rows = crsr.fetchall()
    cnxx.close()
    return render_template("cluster.html",rows = rows)



@app.route('/nightdata',methods=['POST','GET'])
def nightdata():
    cnxx= pyodbc.Connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};''Server=tcp:assign1server.database.windows.net,1433;''Database=assignment1;Uid=saitheja;Pwd=9705004946S@i;')
    crsr = cnxx.cursor()
    crsr.execute('SELECT COUNT(*) FROM all_month where DATEPART(HOUR,time) >=18 or DATEPART(HOUR,time) <=6 ')
    count=crsr.fetchone()
    crsr.execute('SELECT COUNT(*) FROM all_month ')
    count2=crsr.fetchone()

    display=""

    if(count[0]>(count2[0]-count[0])):
        display="Earthqakes occur more at night(6pm to 6am) than in the day,out of "+str(count2[0])+" earth quakes "+str(count[0])+" occured in the night"
    else:
        display="Earthqakes occur more at day(6am to 6pm) than in the night,out of "+str(count2[0])+" earth quakes "+str(count2[0]-count[0])+" occured in the day time"
    cnxx.close()
    return render_template("newrecord.html",display = display)

if __name__ == '__main__':
    app.debug=True
    app.run()
    