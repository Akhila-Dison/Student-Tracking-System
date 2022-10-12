from tkinter import ttk
from tkinter import Message ,Text
import tkinter.ttk as ttk
import tkinter.font as font
from tkinter import *

import csv
from PIL import Image, ImageTk
from PIL import Image

from PIL import Image, ImageFont
import numpy as np
import os
import speech_recognition as sr
from twilio.rest import Client
import cv2
from datetime import datetime

from tkinter import ttk,messagebox
import pymysql

import mysql.connector

con=mysql.connector.connect(host='localhost',database='phpmyadmin',user='root',password='')
cursor=con.cursor()

def his():
    class Student:
        def __init__(self, root):
            self.root=root
            self.root.title("Portal")
            self.root.geometry("1250x680")

            title = Label(self.root,text="Late Attendance History",bd=10,relief=GROOVE,font=("caviar dreams",40,"bold"),bg="orchid3",fg="white")
            title.pack(side=TOP,fill=X)

            #---------------All Variables------------------
            
            self.day_var=StringVar()
            self.m_var=StringVar()
            self.d_var=StringVar()
            self.search_by=StringVar()
            self.search_txt=StringVar()


            #########_________________Details Frame_________________###########
            Detail_Frame = Frame(self.root,bd=4,relief=RIDGE,bg="plum1")
            Detail_Frame.place(x=00,y=83,width=1800,height=570)
##
##            lbl_search=Label(Detail_Frame,text="Search By",bg="plum1",fg="black",font=("times new roman",20,"bold"))
##            lbl_search.grid(row=0,column=0,padx=20,pady=10)
##
##            combo_search=ttk.Combobox(Detail_Frame,textvariable=self.search_by,width=15,font=("time new roman",13,"normal"),state="readonly")
##            combo_search['values']=("name")
##            combo_search.grid(row=0,column=1,pady=20,padx=10)
##
##            txt_search=Entry(Detail_Frame,textvariable=self.search_txt,font=("time new roman",14,"normal"))
##            txt_search.grid(row=0,column=2,pady=10,padx=20)
##
##            searchbtn=Button(Detail_Frame,text="Search",width=10,command=self.search_data).grid(row=0,column=3,padx=20,pady=10)
##            showallbtn=Button(Detail_Frame,text="Show All",width=10,command=self.fetch_data).grid(row=0,column=4,padx=20,pady=10)

            ##########_________table Frame____________________

            Table_Frame = Frame(Detail_Frame,bd=4,relief=RIDGE,bg="black")
            Table_Frame.place(x=10,y=70,width=950,height=480)

            scroll_x=Scrollbar(Table_Frame,orient=HORIZONTAL)
            scroll_y=Scrollbar(Table_Frame,orient=VERTICAL)
            self.student_table=ttk.Treeview(Table_Frame,columns=("name","time","des"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
            
            scroll_x.pack(side=BOTTOM,fill=X)
            scroll_y.pack(side=RIGHT,fill=Y)
            scroll_x.config(command=self.student_table.xview)
            scroll_y.config(command=self.student_table.yview)

            self.student_table.heading("name",text="name")
            self.student_table.heading("time",text="time")
            self.student_table.heading("des",text="des")
            self.student_table['show']='headings'

            self.student_table.column("name",width=100)
            self.student_table.column("time",width=150)
            self.student_table.column("des",width=100)
            self.student_table.pack(fill=BOTH,expand=1)
            self.student_table.bind("<ButtonRelease-1>",self.get_data)
            self.fetch_data()
        def fetch_data(self):
            con=pymysql.connect(host="localhost",user="root",password="",database="phpmyadmin")
            cur=con.cursor()
            cur.execute("select * from late ")
            rows=cur.fetchall()
            if len(rows)!=0:
                self.student_table.delete(*self.student_table.get_children())
                for row in rows:
                    self.student_table.insert('',END,values=row)
                con.commit()
            con.close()
        def get_data(self,ev):
            curosor_row=self.student_table.focus()
            contents=self.student_table.item(curosor_row)
            row=contents['values']

            self.day_var.set(row[0])
            self.m_var.set(row[1])
            self.d_var.set(row[2])
    ##        self.n_var.set(row[3])
    ##        self.o_var.set(row[4])
        def search_data(self):
            con=pymysql.connect(host="localhost",user="root",password="",database="phpmyadmin")
            cur=con.cursor()
            cur.execute("select * from late where "+str(self.search_by.get())+" LIKE '%"+str(self.search_txt.get())+"%'")
            rows=cur.fetchall()
            if len(rows)!=0:
                self.student_table.delete(*self.student_table.get_children())
                for row in rows:
                    self.student_table.insert('',END,values=row)
                con.commit()
            con.close()


    root=Tk()
    ob=Student(root)
    root.mainloop()

def msgs():
    def voice():
        
        global a,txt,d
        recognizer = sr.Recognizer()



        with sr.Microphone() as source:
            print("Adjusting noise ")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Recording for 4 seconds")
            recorded_audio = recognizer.listen(source, timeout=4)
            print("Done recording")

        
        try:
            print("Recognizing the text")
            a = recognizer.recognize_google(
                    recorded_audio, 
                    language="en-US"
                )
            print("Decoded Text : {}".format(a))
            #print(a)
            n=datetime.now()
            n1=n.strftime("%I:%M")
            d=txt.get()
            s="INSERT INTO late(name,time,des) VALUES (%s,%s,%s)"
            
            attend=d,n1,a
            
            #attend=val7
            cursor.execute(s,attend)
            con.commit()

            lbl2 = Label(window, text=a ,bg="white"  ,fg="black"  ,width=20  ,height=3,font=('calibri', 30, 'bold')) 
            lbl2.place(x=500, y=400)
            track1 = Button(window, text="Send", command=msg  ,fg="black"  ,bg="plum1"  ,width=20  ,height=3, activebackground = "plum1" ,font=('caviar dreams', 15, ' bold '))
            track1.place(x=100, y=500)

        except Exception as ex:
            print(ex)

                        
                    
    def msg():
        a1=txt.get()
        print(a1)
        account_sid = 'ACbaadc7874b93d459210411cf7622f9a6'
        auth_token = 'bb72997b221a56d00537662153e9cf36'
        client = Client(account_sid, auth_token)
        message = client.messages \
                      .create(
                          body=" '"+a1+"' send you a message... ' "+a+"'",
                          from_='+15138029644',
                          to='+919633681496'
                       )
        print(message.sid)

    global txt
    window = Tk()
    #helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
    window.title("voice conversion")
     
    window.attributes('-fullscreen',True)
    window.configure(background='white')


    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    lblll = Label(window, text="Message To Teacher" ,bg="orchid3"  ,fg="black"  ,width=60  ,height=2,font=('caviar dreams', 30, 'bold')) 
    lblll.place(x=40, y=5)

    lbl = Label(window, text="Enter Name",width=20  ,height=2  ,fg="black"  ,bg="plum1" ,font=('caviar dreams', 15, ' bold ') ) 
    lbl.place(x=100, y=200)

    txt = Entry(window,width=20  ,bg="plum1" ,fg="black",font=('caviar dreams',15,'bold'))
    txt.place(x=550, y=215)
    
    d=txt.get()
    print(d)
    

    track1 = Button(window, text="Send", command=msg  ,fg="black"  ,bg="plum1"  ,width=20  ,height=2, activebackground = "plum1" ,font=('caviar dreams', 15, ' bold '))
    track1.place(x=100, y=500)

    trackImg = Button(window, text="Talk", command=voice  ,fg="black"  ,bg="plum1"  ,width=20  ,height=2, activebackground = "plum1" ,font=('caviar dreams', 15, ' bold '))
    trackImg.place(x=100, y=350)
def stevents2():
    win = Tk()
    win.geometry('520x520')
    win.title("college erp1")
    win.configure(bg="white")
    Label(win,text="*** Attendance ***", bg="orchid3", fg="white", width="300", height="2", font=("caviar dreams",19,"bold")).pack()
    Label(win,text="",bg="white").pack()
    Button(win,text="Late Report", height="2", width="30",bg='orchid3',command=msgs).pack()
    Label(win,text="",bg="white").pack()
    
    
   
    win.mainloop()
    
def one():
    a=n1.get()
    b=n2.get()
    c=s2.get()
    d=s3.get()
    e=s1.get()
    f=g1.get()
    g=w1.get()
    val1=str(a)
    val2=str(b)
    val3=str(c)
    val4=str(d)
    val5=str(e)
    val6=str(f)
    val7=str(g)
    sql="INSERT INTO `users`(`Name`, `Regno`, `dept`, `Phone`, `Email`, `Username`, `Password`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    attend=(val1,val2,val3,val4,val5,val6,val7)
    cursor.execute(sql,attend)
    con.commit()
    n1.delete(first=0,last=22)
    n2.delete(first=0,last=22)
    s2.delete(first=0,last=22)
    s3.delete(first=0,last=22)
    s1.delete(first=0,last=22)
    g1.delete(first=0,last=22)
    w1.delete(first=0,last=22)    

def signup():
     global n1,n2,s2,s3,s1,g1,w1,k2
     sig1=Tk()
     sig1.attributes('-fullscreen',True)
     sig1.configure(bg="orchid3")
     k1=Label(sig1,text="Registration form",font=("Times New Roman bold",19),fg="white",bg="orchid3").grid (row=0,column=3)
     
     k2=Label(sig1,text="",bg="orchid3").grid (row=0,column=1)
     m1=Label(sig1,text="Name:",fg="black",bg="orchid3").grid (row=1,column=2)
     n1=Entry(sig1)
     n1.grid(row=1,column=3)
     m2=Label(sig1,text="RegNo:",fg="black",bg="orchid3").grid (row=2,column=2)
     n2=Entry(sig1)
     n2.grid(row=2,column=3)
     r2=Label(sig1,text="Department:",fg="black",bg="orchid3").grid (row=3,column=2)
     s2=Entry(sig1)
     s2.grid(row=3,column=3)
     r3=Label(sig1,text="Phone:",fg="black",bg="orchid3").grid (row=4,column=2)
     s3=Entry(sig1)
     s3.grid(row=4,column=3)
     r1=Label(sig1,text="Email:",fg="black",bg="orchid3").grid (row=5,column=2)
     s1=Entry(sig1)
     s1.grid(row=5,column=3)
     f1=Label(sig1,text="Username:",fg="black",bg="orchid3").grid (row=6,column=2)
     g1=Entry(sig1)
     g1.grid(row=6,column=3)
     v1=Label(sig1,text="Password:",fg="black",bg="orchid3").grid (row=7,column=2)
     w1=Entry(sig1,show="*")
     w1.grid(row=7,column=3)
     k1=Label(sig1,text="",bg="orchid3").grid (row=9,column=2)
     j=Button(sig1,text="Register",fg="black",command=one).grid (row=10,column=2)
     j1=Button(sig1,text="Exit",fg="black",command=sig1.destroy).grid (row=10,column=3)
     sig1.mainloop()

def studlogin ():
    window2=Tk()
    window2.title("login")
    window2.geometry("500x300")
    window2.configure(bg="orchid3")
    fr=Label(window2,text="ENTER LOGIN DETAILS",fg="black",bg="orchid3",height="2",width="20", font=("caviar dreams",12)).grid (column=1,row=0)
    lbl=Label(window2,text=" USERNAME",bg="orchid3",height="2",width="20")
    lbl.grid(column=0,row=1)
    lb2=Label(window2,text="PASSWORD",bg="orchid3",height="2",width="20")
    lb2.grid(column=0,row=2) 
    ent1=Entry(window2)
    ent1.grid(row=1,column=3)
    ent2=Entry(window2,show="*")
    ent2.grid(row=2,column=3)
    lbl=Label(window2,text=" ",bg="orchid3",height="2",width="20")
    lbl.grid(column=0,row=3)
    def log1():
        list1=[]
        list2=[]
        x=ent1.get()
        y2=ent2.get()
        val=str(x)
        sql1="select username from users"
        cursor.execute(sql1)
        a=cursor.fetchall()
        for a in a:
            print(a)
            if val in a:
                sql="select Password from users where Username='"+val+"'   "
                cursor.execute(sql)
                y1=cursor.fetchall()
                for y in y1:
                    x=format(y[0])
                    list1.append(x)
                    print(x)
                a=list1[0]
                #print(a)
                #print(y2)
                if a==y2:
                    lbl=Label(window2,text="success",bg="orchid3",height="3",width="20")
                    lbl.grid(column=1,row=8)
                    stevents2()
                else:
                    lbl=Label(window2,text="password incorrect",bg="orchid3",height="3",width="20")
                    lbl.grid(column=1,row=8)
            else:
                lbl=Label(window2,text="invalid username",bg="orchid3",height="3",width="20")
                lbl.grid(column=1,row=8)
    btn5=Button(window2,text="  login  ",bg="plum1",fg="black",command=log1)
    btn5.grid(row=5,column=1)
    lbl=Label(window2,text="",bg="orchid3",height="3",width="20")
    lbl.grid(column=1,row=6)
    btn5=Button(window2,text="  back  ",bg="plum1",fg="black",command=window2.destroy)
    btn5.grid(row=6,column=1)
    window2.mainloop()
    window2.destroy()
def stevents3():
    win = Tk()
    win.geometry('520x520')
    win.title("college erp1")
    win.configure(bg="white")
    Label(win,text="*** Attendance ***", bg="orchid3", fg="black", width="300", height="2", font=("caviar dreams",19,"bold")).pack()
    Label(win,text="",bg="white").pack()
   
    Button(win,text="History", height="2", width="30",bg='orchid3',command=his).pack()
    Label(win,text="",bg="white").pack()
    
    
    win.mainloop()
def two():
    a=n1.get()
    b=s2.get()
    c=g1.get()
    d=w1.get()
    
    val1=str(a)
    val2=str(b)
    val3=str(c)
    val4=str(d)
    
    sql="INSERT INTO `teacher`(`name`, `department`, `username`, `password`) VALUES (%s,%s,%s,%s)"
    attend=(val1,val2,val3,val4)
    cursor.execute(sql,attend)
    con.commit()
    n1.delete(first=0,last=22)
    s2.delete(first=0,last=22)
    g1.delete(first=0,last=22)
    w1.delete(first=0,last=22)
         

def signup2():
     global n1,s2,g1,w1,k2
     sig1=Tk()
     sig1.geometry("400x400")
     sig1.configure(bg="orchid3")
     k1=Label(sig1,text="Registration form",font=("Times New Roman bold",19),fg="white",bg="orchid3").grid (row=0,column=3)
     k2=Label(sig1,text="",bg="orchid3").grid (row=0,column=1)
     m1=Label(sig1,text="Name:",fg="black",bg="orchid3").grid (row=1,column=2)
     n1=Entry(sig1)
     n1.grid(row=1,column=3)
     
     r2=Label(sig1,text="Department:",fg="black",bg="orchid3").grid (row=2,column=2)
     s2=Entry(sig1)
     s2.grid(row=2,column=3)
     
     f1=Label(sig1,text="Username:",fg="black",bg="orchid3").grid (row=3,column=2)
     g1=Entry(sig1)
     g1.grid(row=3,column=3)
     v1=Label(sig1,text="Password:",fg="black",bg="orchid3").grid (row=4,column=2)
     w1=Entry(sig1,show="*")
     w1.grid(row=4,column=3)
     k1=Label(sig1,text="",bg="orchid3").grid (row=6,column=2)
     j=Button(sig1,text="Register",fg="black",command=two).grid (row=7,column=2)
     j1=Button(sig1,text="Exit",fg="black",command=sig1.destroy).grid (row=7,column=3)
     sig1.mainloop()
     
def studlogin2 ():
    window2=Tk()
    window2.title("login")
    window2.geometry("500x300")
    window2.configure(bg="orchid3")
    fr=Label(window2,text="ENTER LOGIN DETAILS",fg="white",bg="orchid3",height="2",width="20", font=("caviar dreams",12,"bold")).grid (column=1,row=0)
    lbl=Label(window2,text=" USERNAME",bg="orchid3",height="2",width="20")
    lbl.grid(column=0,row=1)
    lb2=Label(window2,text="PASSWORD",bg="orchid3",height="2",width="20")
    lb2.grid(column=0,row=2) 
    ent1=Entry(window2)
    ent1.grid(row=1,column=3)
    ent2=Entry(window2,show="*")
    ent2.grid(row=2,column=3)
    lbl=Label(window2,text=" ",bg="orchid3",height="2",width="20")
    lbl.grid(column=0,row=3)
    def log2():
        list1=[]
        list2=[]
        x=ent1.get()
        y2=ent2.get()
        val=str(x)
        sql1="select username from teacher"
        cursor.execute(sql1)
        a=cursor.fetchall()
        for a in a:
            print(a)
            if val in a:
                sql="select password from teacher where username='"+val+"'  "
                cursor.execute(sql)
                y1=cursor.fetchall()
                for y in y1:
                    x=format(y[0])
                    list1.append(x)
                    print(x)
                a=list1[0]
                print(a)
                print(y2)
                if a==y2:
                    lbl=Label(window2,text="success",bg="orchid3",height="3",width="20")
                    lbl.grid(column=1,row=8)
                    his()
                else:
                    lbl=Label(window2,text="password incorrect",bg="orchid3",height="3",width="20")
                    lbl.grid(column=1,row=8)
            else:
                lbl=Label(window2,text="invalid username",bg="orchid3",height="3",width="20")
                lbl.grid(column=1,row=8)
    btn5=Button(window2,text="  login  ",bg="plum1",fg="black",command=log2)
    btn5.grid(row=5,column=1)
    lbl=Label(window2,text="",bg="orchid3",height="3",width="20")
    lbl.grid(column=1,row=6)
    btn5=Button(window2,text="  back  ",bg="plum1",fg="black",command=window2.destroy)
    btn5.grid(row=6,column=1)
    window2.mainloop()
def main_account():
    global main_screen0
    
    main_screen0 = Tk()
    main_screen0.attributes('-fullscreen',True)
    main_screen0.title("college erp")
    main_screen0.configure(bg="white")
    Label(text="ST. Joseph's College (Autonomous), Irinjalakuda", fg="black", width="300", height="2", font=("Times New Roman bold",19)).pack()
    Label(text="",bg="white").pack() 
    Button(text="Talk To Me", height="2", width="30",bg='orchid3',command=msgs).pack()
    Label(text="",bg="white").pack()
    Label(text="TEACHER LOGIN", fg="black", width="300", height="2", font=("Times New Roman bold",19)).pack()
    Label(text="",bg="white").pack()
    Button(text="Login", height="2", width="30",bg='orchid3',command=studlogin2).pack()
    Label(text="",bg="white").pack()
    Button(text="Register", height="2", width="30",bg='orchid3',command=signup2).pack()
    Label(text="",bg="white").pack()
    image = Image.open('ts.jpeg')
    photo_image = ImageTk.PhotoImage(image)
    
    Label(image = photo_image,width='15000',height='500').pack()
    Label(text="",bg="white").pack()
    main_screen0.mainloop()
    
 
 
main_account()

