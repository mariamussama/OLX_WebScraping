#################################################################
from tkinter import *
import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
import pymysql 
import sys
from tabulate import tabulate
from tkinter.messagebox import showinfo
from PyQt5.QtWidgets import QWidget,QScrollArea, QTableWidget, QVBoxLayout,QTableWidgetItem 

con = pymysql.connect(
host ='db4free.net',
user = 'mariamussama',
password='Mariam2000',
db="olx_database")


def exec_1(email,username, gender, birthdate_year, birthdate_month, birthdate_day):
    txt.delete('1.0', END)
    for ele in txt.winfo_children():
        ele.destroy()
    cur = con.cursor()
    # print('username', username)
    # print('email', email)
    if birthdate_year >1000 and birthdate_year < 2022 and birthdate_month>0 and birthdate_month< 13 and birthdate_day>0 and birthdate_day<32:
        birthdate = str(birthdate_year) + "-" + str(birthdate_month)+ "-" + str(birthdate_day)
        if gender == "M" or gender =="m":
            gender = "Male"
            cur.execute("INSERT INTO a_user VALUES ('{}', '{}', '{}', '{}');".format(email, username, gender, birthdate))
            rows = cur.fetchall()
            con.commit()
            # print("User added successfully")
            rows = "User added successfully"
        elif gender == "F" or gender == "f":
            gender = "Female"
            cur.execute("INSERT INTO a_user VALUES ('{}', '{}', '{}', '{}');".format(email, username, gender, birthdate))
            rows = cur.fetchall()
            con.commit()
            # print("User added successfully")
            rows = "User added successfully"
        else:
            # print("wrong input")
            rows = "wrong input"
    else:
        # print("wrong input")
        rows = "wrong input"
    class PrintToTXT(object): 
        def write(self, s): 
            txt.insert(END, s)
    sys.stdout = PrintToTXT()
    print (rows) 


def exec_2(email, ad_id, review, rating):
    txt.delete('1.0', END)
    for ele in txt.winfo_children():
        ele.destroy()
    cur = con.cursor()
    cur.execute("SELECT Email_address from a_user where Email_address = '{}';".format(email))
    rows = cur.fetchall()
    if rows.__len__() != 0:
        cur.execute("SELECT S.Review from sale as S where S.AD_ID = '{}';".format(ad_id))
        rows = cur.fetchall()
        if rows.__len__() == 0:
            cur.execute("SELECT Price from car where AD_ID = '{}';".format(ad_id))
            rows = cur.fetchall()
            i = 0
            if rows.__len__() != 0:
                for [i] in rows:
                    price = i
                if rating < 1 or rating > 5:
                    rows = "wrong rating"
                else :
                    cur.execute("INSERT INTO sale VALUES ('{}', '{}', '{}', '{}','{}');".format(price, review, rating , email, ad_id))
                    rows = cur.fetchall()
                    con.commit()
                    rows = "Sale added successfully"
            else:
                rows = "AD ID not found"
        else:
            rows = "Review already exists"
    else:
        rows = "Email not found"
    class PrintToTXT(object): 
        def write(self, s): 
            txt.insert(END, s)
    sys.stdout = PrintToTXT()
    print (rows)
        
        
def exec_3(ad_id):
    txt.delete('1.0', END)
    for ele in txt.winfo_children():
        ele.destroy()
    cur = con.cursor()
    cur.execute("SELECT Review from sale where AD_ID = '{}';".format(ad_id))
    rows = cur.fetchall()
    # rows = pd.DataFrame(rows,columns=['Review'])
    # class PrintToTXT(object): 
    #     def write(self, s): 
    #         txt.insert(END, s)
    # sys.stdout = PrintToTXT()
    # print(rows)
    trv=ttk.Treeview(txt, column=('Reviews'), show='headings')
    trv.grid(row=rows.__len__(),column=1,columnspan=3,padx=10,pady=20)
    trv.column('Reviews',width=150,anchor='c')
    trv.heading('Reviews',text='Reviews')
    for row in rows:
        trv.insert('', tk.END, values=row)
    return


def exec_4(phone_number):
    txt.delete('1.0', END)
    for ele in txt.winfo_children():
        ele.destroy()
    cur = con.cursor()
    cur.execute("""Select AVG(Rating) from sale as S 
                inner join car as C on S.AD_ID = C.AD_ID 
                inner join owner_agent as O
                on C.Owner_Phone_number = O.Phone_number
                where O.Phone_number = '{}';""".format(phone_number))
    rows = cur.fetchall()
    # rows = pd.DataFrame(rows,columns=['Aggregated Rating'])
    # class PrintToTXT(object): 
    #     def write(self, s): 
    #         txt.insert(END, s)
    # sys.stdout = PrintToTXT()
    # print(rows)
    trv=ttk.Treeview(txt, column=('Aggregated_Rating'), show='headings')
    trv.grid(row=rows.__len__(),column=1,columnspan=3,padx=10,pady=20)
    trv.column('Aggregated_Rating',width=150,anchor='c')
    trv.heading('Aggregated_Rating',text='Aggregated_Rating')
    for row in rows:
        trv.insert('', tk.END, values=row)
    return


def exec_5(make, body_type, location, year):
    location = "%" + location + "%"
    txt.delete('1.0', END)
    for ele in txt.winfo_children():
        ele.destroy()
    cur = con.cursor()
    cur.execute("""Select C.Model, AVG(C.Price), COUNT(C.Model) from car as C 
            where C.Make = '{}' and C.Body_type = '{}' and C.make_year = {} and C.Location LIKE '{}'
            group by 1;""".format(make, body_type, int(year), location))
    rows = cur.fetchall()
    # rows = pd.DataFrame(rows,columns=['Model', 'Average Price', 'Count'])
    # class PrintToTXT(object): 
    #     def write(self, s): 
    #         txt.insert(END, s)
    # sys.stdout = PrintToTXT()
    # print(rows)
    trv=ttk.Treeview(txt, columns=('Model', 'Average Price', 'Count'), show='headings')
    trv.grid(row=rows.__len__(),column=3,columnspan=3,padx=10,pady=20)
    col=('Model', 'Average Price', 'Count')
    for i in col:
        trv.column(i,width=150,anchor='c')
        trv.heading(i,text=i)
    for row in rows:
        trv.insert('', tk.END, values=row)
    return


def exec_6(location, min_price, max_price, features):
    location = "%" + location + "%"
    txt.delete('1.0', END)
    for ele in txt.winfo_children():
        ele.destroy()
    cur = con.cursor()
    feature_list = []
    feature_list = features.split(",")
    q_features = ""
    for feature in feature_list:
        q_features = q_features + "F.features like '%" + feature + "%' or "
    q_features = q_features[:-4]
    # print(q_features)
    query = "select C.AD_ID, Make, Model, Price, Owner_Phone_number from car as C inner join car_features as F on C.AD_ID = F.AD_ID where C.Cond = 'Used' and C.Price <{} and C.Price > {} and C.Location like '{}' and {} group by 1,2,3,4,5;".format(int(max_price), int(min_price), location, q_features) 
    cur.execute(query)
    rows = cur.fetchall()
    # rows = pd.DataFrame(rows,columns=['AD ID','Make','Model', 'Price', 'Owner Phone number'])
    # class PrintToTXT(object): 
    #     def write(self, s): 
    #         txt.insert(END, s)
    # sys.stdout = PrintToTXT()
    # print(rows)
    trv=ttk.Treeview(txt, columns=('AD ID','Make','Model', 'Price', 'Owner Phone number'), show='headings')
    trv.grid(row=rows.__len__(),column=5,columnspan=3,padx=10,pady=20)
    col=('AD ID','Make','Model', 'Price', 'Owner Phone number')
    for i in col:
        trv.column(i,width=150,anchor='c')
        trv.heading(i,text=i)
    for row in rows:
        trv.insert('', tk.END, values=row)
    return 


def exec_7(make, model):
    txt.delete('1.0', END)
    for ele in txt.winfo_children():
        ele.destroy()
    cur = con.cursor()
    cur.execute("""Select C.Location, AVG(C.Price), COUNT(C.AD_ID) from car as C 
                where C.Make = '{}' and C.Model = '{}' and C.Location like '%_airo%'
                group by 1
                order by 3 desc
                limit 5;""".format(make, model))
    rows = cur.fetchall()
    # rows = pd.DataFrame(rows,columns=['Location', 'Average Price', 'Count'])
    # class PrintToTXT(object): 
    #     def write(self, s): 
    #         txt.insert(END, s)
    # sys.stdout = PrintToTXT()
    # print(rows)
    trv=ttk.Treeview(txt, columns=('Location', 'Average Price', 'Count'), show='headings')
    trv.grid(row=rows.__len__(),column=3,columnspan=3,padx=10,pady=20)
    col=('Location', 'Average Price', 'Count')
    for i in col:
        trv.column(i,width=150,anchor='c')
        trv.heading(i,text=i)
    for row in rows:
        trv.insert('', tk.END, values=row)


def exec_8():
    txt.delete('1.0', END)
    for ele in txt.winfo_children():
        ele.destroy()
    cur = con.cursor()
    cur.execute("""Select O.Username, O.Phone_number, COUNT(C.AD_ID), AVG(C.Price) from car as C 
        inner join owner_agent as O
        on C.Owner_Phone_number = O.Phone_number
        group by 1,2
        order by 3 desc
        limit 5;""")
    rows = cur.fetchall()
    # rows = pd.DataFrame(rows,columns=['Name', 'Phone_number','Count', 'Average Price'])
    # rows = tabulate(rows, headers='keys', tablefmt='psql')

    trv=ttk.Treeview(txt, columns=('Name', 'Phone number','Count', 'Average Price'), show='headings')
    trv.grid(row=5,column=4,columnspan=3,padx=10,pady=20)
    col=('Name', 'Phone number','Count', 'Average Price')
    for i in col:
        trv.column(i,width=150,anchor='c')
        trv.heading(i,text=i)
    for row in rows:
        trv.insert('', tk.END, values=row)
    # class PrintToTXT(object): 
    #     def write(self, s): 
    #         txt.insert(END, s)
    # sys.stdout = PrintToTXT()
    # print (rows)


def exec_9_1(phone_number):
    txt.delete('1.0', END)
    for ele in txt.winfo_children():
        ele.destroy()
    cur = con.cursor()
    cur.execute("""select C.AD_ID, C.Make, C.Model, C.Price, C.make_year from car as C 
            where C.Owner_Phone_number = '{}';""".format(phone_number))
    rows = cur.fetchall()
    # rows = pd.DataFrame(rows,columns=['AD ID','Make','Model', 'Price', 'Owner Phone number'])
    # class PrintToTXT(object): 
    #     def write(self, s): 
    #         txt.insert(END, s)
    # sys.stdout = PrintToTXT()
    # print(rows)
    
    trv=ttk.Treeview(txt, columns=('AD ID','Make','Model', 'Price', 'Make Year'), show='headings')
    trv.grid(row=rows.__len__(),column=5,columnspan=3,padx=10,pady=20)
    col=('AD ID','Make','Model', 'Price', 'Make Year')
    for i in col:
        trv.column(i,width=150,anchor='c')
        trv.heading(i,text=i)
    for row in rows:
        trv.insert('', tk.END, values=row)
    return
def exec_9_2(name):
    txt.delete('1.0', END)
    for ele in txt.winfo_children():
        ele.destroy()
    cur = con.cursor()
    cur.execute("""select C.AD_ID, C.Make, C.Model, C.Price, C.make_year from car as C 
                        inner join owner_agent as O
                        on C.Owner_Phone_number = O.Phone_number
                        where O.username = '{}';""".format(name))
    rows = cur.fetchall()
    # rows = pd.DataFrame(rows,columns=['AD ID','Make','Model', 'Price', 'Owner Phone number'])
    # class PrintToTXT(object): 
    #     def write(self, s): 
    #         txt.insert(END, s)
    # sys.stdout = PrintToTXT()
    # print(rows)
    col=('AD ID','Make','Model', 'Price', 'Make Year')
    trv=ttk.Treeview(txt, columns=('AD ID','Make','Model', 'Price', 'Make Year'), show='headings')
    trv.grid(row=rows.__len__(),column=5,columnspan=3,padx=10,pady=20)
    for i in col:
        trv.column(i,width=150,anchor='c')
        trv.heading(i,text=i)
    for row in rows:
        trv.insert('', tk.END, values=row)
    return

def exec_10(F, T):
    txt.delete('1.0', END)
    for ele in txt.winfo_children():
        ele.destroy()
    cur = con.cursor()
    cur.execute("""Select Model, Make, Count(AD_ID), AVG(Price) from car as C
            where make_year > {} and make_year<{}
            group by 1,2
            order by 3 desc
            limit 5;""".format(int(F), int(T)))
    rows = cur.fetchall()
    # rows = pd.DataFrame(rows,columns=['Model','Make','Count', 'Average Price'])
    # class PrintToTXT(object): 
    #     def write(self, s): 
    #         txt.insert(END, s)
    # sys.stdout = PrintToTXT()
    # print(rows)
    col=('Model','Make','Count', 'Average Price')
    trv=ttk.Treeview(txt, columns=('Model','Make','Count', 'Average Price'), show='headings')
    trv.grid(row=rows.__len__(),column=4,columnspan=3,padx=10,pady=20)
    for i in col:
        trv.column(i,width=150,anchor='c')
        trv.heading(i,text=i)
    for row in rows:
        trv.insert('', tk.END, values=row)
def exec_11():
    root.destroy()
    
def disp_options():
    val=1
    opts=[]
    print(var.get())
    for query in Queries:
        opts.append(Radiobutton(root, text=query, variable=var, value=val, command=option))
        opts[val-1].pack( anchor = W )
        val+=1
    # execute_but = tk.Button(text="Execute Query", command=exec_1)
    # execute_but.pack(pady=10)

        

def del_buttons():
    for ele in root.winfo_children():
        if ele.winfo_class() == 'Button' or ele.winfo_class() == 'Frame':
            ele.destroy()
            
            
def Q_1():
    
    frame = Frame(master=root, width=1800, height=50)
    frame.pack()
    username_lab=Label(master=frame, text="Enter username: ")
    username_lab.place(x=0, y=0)
    # username_lab.pack()
    username = Entry(master=frame)
    username.focus_set()
    username.place(x=0, y=20)
    # username.pack()
    email_lab=Label(master=frame, text="Enter email: ")
    email_lab.place(x=170, y=0)
    # email_lab.pack()
    email = Entry(master=frame)
    email.focus_set()
    # email.pack()
    email.place(x=170, y=20)
    gender_lab = Label (master=frame, text="Enter Gender(F/M): ")
    # gender_lab.pack()
    gender_lab.place(x=340, y=0)
    gender = Entry(master=frame)
    gender.focus_set()
    gender.place(x=340, y=20)
    # gender.pack()
    birthdate_year_lab = Label(master=frame, text="Enter birthdate year(YYYY): ")
    birthdate_year_lab.place(x=510, y=0)
    # birthdate_year_lab.pack()
    birthdate_year = Entry(master=frame)
    birthdate_year.focus_set()
    # birthdate_year.pack()
    birthdate_year.place(x=510, y=20)
    birthdate_month_lab = Label(master=frame, text="Enter birthdate month(MM): ")
    birthdate_month_lab.place(x=680, y=0)
    # birthdate_month_lab.pack()
    birthdate_month = Entry(master=frame)
    birthdate_month.focus_set()
    # birthdate_month.pack()
    birthdate_month.place(x=680, y=20)
    birthdate_day_lab = Label(master=frame, text="Enter birthdate day(DD): ")
    birthdate_day_lab.place(x=850, y=0)
    # birthdate_day_lab.pack()
    birthdate_day = Entry(master=frame)
    birthdate_day.focus_set()
    # birthdate_day.pack()
    birthdate_day.place(x=850, y=20)
    execute_but = Button(root, text="Execute Query", command=lambda: exec_1(email.get(), username.get(), gender.get(), int(birthdate_year.get()),int(birthdate_month.get()), int(birthdate_day.get())))
    execute_but.pack(pady=10)
    

def Q_2():
    frame = Frame(master=root, width=1800, height=50)
    frame.pack()
    ad_id_lab=Label(master=frame, text="Enter ad id: ")
    ad_id_lab.place(x=0, y=0)
    ad_id = Entry(master=frame)
    ad_id.focus_set()
    ad_id.place(x=0, y=20)
    email_lab=Label(master=frame, text="Enter email: ")
    email_lab.place(x=170, y=0)
    email = Entry(master=frame)
    email.focus_set()
    email.place(x=170, y=20)
    review_lab = Label (master=frame, text="Enter review: ")
    review_lab.place(x=340, y=0)
    review = Entry(master=frame)
    review.focus_set()
    review.place(x=340, y=20)
    rating_lab = Label(master=frame, text="Enter rating(1-5): ")
    rating_lab.place(x=510, y=0)
    rating = Entry(master=frame)
    rating.focus_set()
    rating.place(x=510, y=20)
    execute_but = Button(root, text="Execute Query", command=lambda: exec_2(email.get(), ad_id.get(), review.get(), int(rating.get())))
    execute_but.pack(pady=10)
    return


def Q_3():
    frame = Frame(master=root, width=1800, height=50)
    frame.pack()
    ad_id_lab=Label(master=frame, text="Enter ad id: ")
    ad_id_lab.place(x=0, y=0)
    ad_id = Entry(master=frame)
    ad_id.focus_set()
    ad_id.place(x=0, y=20)
    execute_but = Button(root, text="Execute Query", command=lambda: exec_3(ad_id.get()))
    execute_but.pack(pady=10)
    return


def Q_4():
    frame = Frame(master=root, width=1800, height=50)
    frame.pack()
    phone_number_lab=Label(master=frame, text="Enter Phone number: ")
    phone_number_lab.place(x=0, y=0)
    phone_number = Entry(master=frame)
    phone_number.focus_set()
    phone_number.place(x=0, y=20)
    execute_but = Button(root, text="Execute Query", command=lambda: exec_4(phone_number.get()))
    execute_but.pack(pady=10)
    return  


def Q_5():
    frame = Frame(master=root, width=1800, height=50)
    frame.pack()
    make_lab=Label(master=frame, text="Enter make: ")
    make_lab.place(x=0, y=0)
    make = Entry(master=frame)
    make.focus_set()
    make.place(x=0, y=20)
    body_type_lab=Label(master=frame, text="Enter body type: ")
    body_type_lab.place(x=170, y=0)
    body_type = Entry(master=frame)
    body_type.focus_set()
    body_type.place(x=170, y=20)
    location_lab = Label (master=frame, text="Enter location: ")
    location_lab.place(x=340, y=0)
    location = Entry(master=frame)
    location.focus_set()
    location.place(x=340, y=20)
    year_lab = Label(master=frame, text="Enter year: ")
    year_lab.place(x=510, y=0)
    year= Entry(master=frame)
    year.focus_set()
    year.place(x=510, y=20)
    loc = location.get()
    execute_but = Button(root, text="Execute Query", command=lambda: exec_5(make.get(), body_type.get(), loc , year.get()))
    execute_but.pack(pady=10)
    return


def Q_6():
    frame = Frame(master=root, width=1800, height=50)
    frame.pack()
    location_lab = Label (master=frame, text="Enter location: ")
    location_lab.place(x=0, y=0)
    location = Entry(master=frame)
    location.focus_set()
    location.place(x=0, y=20)
    min_price_lab = Label(master=frame, text="Enter min price: ")
    min_price_lab.place(x=170, y=0)
    min_price = Entry(master=frame)
    min_price.focus_set()
    min_price.place(x=170, y=20)
    max_price_lab = Label(master=frame, text="Enter max price: ")
    max_price_lab.place(x=340, y=0)
    max_price = Entry(master=frame)
    max_price.focus_set()
    max_price.place(x=340, y=20)
    features_lab = Label(master=frame, text="Enter features separated by ',' : ")
    features_lab.place(x=510, y=0)
    features = Entry(master=frame)
    features.focus_set()
    features.place(x=510, y=20)
    execute_but = Button(root, text="Execute Query", command=lambda: exec_6(location.get(), min_price.get(), max_price.get(), features.get()))
    execute_but.pack(pady=10)  
    return


def Q_7():
    frame = Frame(master=root, width=1800, height=50)
    frame.pack()
    make_lab=Label(master=frame, text="Enter make: ")
    make_lab.place(x=0, y=0)
    make = Entry(master=frame)
    make.focus_set()
    make.place(x=0, y=20)
    model_lab=Label(master=frame, text="Enter model: ")
    model_lab.place(x=170, y=0)
    model = Entry(master=frame)
    model.focus_set()
    model.place(x=170, y=20)
    execute_but = Button(root, text="Execute Query", command=lambda: exec_7(make.get(), model.get()))
    execute_but.pack(pady=10)
    return


def Q_8():
    execute_but = Button(root, text="Execute Query", command=exec_8)
    execute_but.pack(pady=10)
    return


def Q_9():
    frame = Frame(master=root, width=1800, height=60)
    frame.pack()
    op1 = Radiobutton(master =frame, text='Using Phone numer', variable=var2, value=1, command=option)
    op1.place(x=0, y=0)
    op2 = Radiobutton(master =frame, text='Using Owner username', variable=var2, value=2, command=option)
    op2.place(x=300, y=0)
    return


def Q_9_1():
    frame = Frame(master=root, width=1800, height=60)
    frame.pack()
    op1 = Radiobutton(master =frame, text='Using Phone numer', variable=var2, value=1, command=option)
    op1.place(x=0, y=0)
    op2 = Radiobutton(master =frame, text='Using Owner username', variable=var2, value=2, command=option)
    op2.place(x=300, y=0)
    phone_number_lab=Label(master=frame, text="Enter Phone number: ")
    phone_number_lab.place(x=0, y=20)
    phone_number = Entry(master=frame)
    phone_number.focus_set()
    phone_number.place(x=0, y=40)
    execute_but = Button(root, text="Execute Query", command=lambda: exec_9_1(phone_number.get()))
    execute_but.pack(pady=10)
    return


def Q_9_2():
    frame = Frame(master=root, width=1800, height=60)
    frame.pack()
    op1 = Radiobutton(master =frame, text='Using Phone numer', variable=var2, value=1, command=option)
    op1.place(x=0, y=0)
    op2 = Radiobutton(master =frame, text='Using Owner username', variable=var2, value=2, command=option)
    op2.place(x=300, y=0)
    name_lab=Label(master=frame, text="Enter Owner username: ")
    name_lab.place(x=0, y=20)
    name = Entry(master=frame)
    name.focus_set()
    name.place(x=0, y=40)
    execute_but = Button(root, text="Execute Query", command=lambda: exec_9_2(name.get()))
    execute_but.pack(pady=10)
    return


def Q_10():
    frame = Frame(master=root, width=1800, height=50)
    frame.pack()
    F_lab = Label (master=frame, text="Range year from : ")
    F_lab.place(x=0, y=0)
    F = Entry(master=frame)
    F.focus_set()
    F.place(x=0, y=20)
    T_lab = Label (master=frame, text="Range year to : ")
    T_lab.place(x=170, y=0)
    T = Entry(master=frame)
    T.focus_set()
    T.place(x=170, y=20)
    execute_but = Button(root, text="Execute Query", command=lambda: exec_10(int(F.get()), int(T.get())))
    execute_but.pack(pady=10)
    return


def Q_11():
    execute_but = Button(root, text="Close", command=exec_11)
    execute_but.pack(pady=10)
    return   


def option():
    # print(var.get())
    # txt.delete('1.0', END)
    del_buttons()
    if (var.get() == 1):
        Q_1()
    elif (var.get() == 2):
        Q_2()
    elif (var.get() == 3):
        Q_3()
    elif (var.get() == 4):
        Q_4()
    elif (var.get() == 5):
        Q_5()
    elif (var.get() == 6):
        Q_6()
    elif (var.get() == 7):
        Q_7()
    elif (var.get() == 8):
        Q_8()
    elif (var.get() == 9) and (var2.get() == 0):
        Q_9()
    elif (var.get() == 9) and (var2.get() == 1):
        Q_9_1()
    elif (var.get() == 9) and (var2.get() == 2):
        Q_9_2()
    elif (var.get() == 10):
        Q_10()
    elif (var.get() == 11):
        Q_11()
    
    
def sel():
   selection = "You selected the option " + str(var.get())
   label.config(text = selection)


root = Tk()
root.geometry("1500x2000")
root.title('OLX Database')
var = IntVar()
var.set(0)
var2 = IntVar()
var2.set(0)
txt = Text(root, height=15) 
txt.pack()
# scrollbar = Scrollbar(root)
# scrollbar.pack( side = RIGHT, fill = Y )
Queries= [
        "1. Register a user",
        "2. Add a new user sale for an ad",
        "3. View existing reviews of a given ad",
        "4. View aggregated rating of a seller / owner",
        "5. Show all the ads for a given car make, body type and year in a specific location / area, along with the average price the number of listings for each model",
        "6. Show all the used cars in a certain location in a given price range, with a given set of features",
        "7. Show the top 5 areas in cairo by amount of inventory and average price a given make / model",
        "8. Show the top 5 sellers by the amount of listings they have, along with their avg price per year",
        "9. Show all the properties listed by a specific owner (given their first and last name and / or phone no)",
        "10. Show the top 5 make / models cars by the amount of inventory and their average price for a given year range",
        "11. exit"
    ]
disp_options()
label = Label(root)
label.pack()
root.mainloop()
