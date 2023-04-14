import pandas as pd
from tabulate import tabulate
import pymysql 

con = pymysql.connect(
host ='db4free.net',
user = 'mariamussama',
password='Mariam2000',
db="olx_database")

exit=False

cur = con.cursor()
while not exit:
    print ("""
            1- Register a user.
            2- Add a new user sale for an ad.
            3- View existing reviews of a given ad.
            4- View aggregated rating of a seller / owner.
            5- Show all the ads for a given car make, body type and year in a specific location / area, along with the average price the number of listings for each model.
            6- Show all the used cars in a certain location in a given price range, with a given set of featurows.
            7- Show the top 5 areas in cairo by amount of inventory and average price a given make / model.
            8- Show the top 5 sellers by the amount of listings they have, along with their avg price per year.
            9- Show all the properties listed by a specific owner (given their first and last name and / or phone no). 
            10- Show the top 5 make / models cars by the amount of inventory and their average price for a given year range.
            11- exit
            """)
    choice = input("Enter choice:")
    if choice == '1':
        username = input("Enter username: ")
        email = input("Enter email: ")
        gender = input("Enter Gender: ")
        birthdate_year = input("Enter birthdate year(YYYY): ")
        birthdate_month = input("Enter birthdate month(MM): ")
        birthdate_day = input("Enter birthdate day(DD): ")
        if birthdate_year >1000 and birthdate_year < 2022 and birthdate_month>0 and birthdate_month< 13 and birthdate_day>0 and birthdate_day<32:
            birthdate = birthdate_year + "-" + birthdate_month + "-" + birthdate_day
            if gender == "Male" or gender =="male":
                gender = "Male"
                cur.execute("INSERT INTO a_user VALUES ('{}', '{}', '{}', '{}');".format(email, username, gender, birthdate))
                rows = cur.fetchall()
                con.commit()
                print("User added successfully")
            elif gender == "Female" or gender == "female":
                gender = "Female"
                cur.execute("INSERT INTO a_user VALUES ('{}', '{}', '{}', '{}');".format(email, username, gender, birthdate))
                rows = cur.fetchall()
                con.commit()
                print("User added successfully")
            else:
                print("wrong input")
        else:
            print("wrong input")
    elif choice == '2':
        ad_id = input("Enter ad id: ")
        email = input("Enter email: ")
        review = input("Enter review: ")
        rating = input("Enter rating(1-5): ")
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
                    if int(rating) < 1 or int(rating) > 5:
                        print("wrong rating")
                    else :
                        cur.execute("INSERT INTO sale VALUES ('{}', '{}', '{}', '{}','{}');".format(price, review, rating , email, ad_id))
                        rows = cur.fetchall()
                        con.commit()
                        print("Sale added successfully")
                else:
                    print("AD ID not found")
            else:
                print("Review already exists")
        else:
            print("Email not found")
    elif choice == '3':
        ad_id = input("Enter ad id: ")
        cur.execute("SELECT Review from sale where AD_ID = '{}';".format(ad_id))
        rows = cur.fetchall()
        rows = pd.DataFrame(rows,columns=['Review'])
        rows = tabulate(rows, headers='keys', tablefmt='psql')
        print(rows)
    elif choice == '4':
        phone_number = input("Enter Phone number: ")
        cur.execute("""Select AVG(Rating) from sale as S 
                    inner join car as C on S.AD_ID = C.AD_ID 
                    inner join owner_agent as O
                    on C.Owner_Phone_number = O.Phone_number
                    where O.Phone_number = '{}';""".format(phone_number))
        rows = cur.fetchall()
        rows = pd.DataFrame(rows,columns=['Aggregated Rating'])
        rows = tabulate(rows, headers='keys', tablefmt='psql')
        print(rows)
    elif choice == '5':
        make = input("Enter make: ")
        body_type = input("Enter body type: ")
        location = input("Enter location: ")
        location = "%" + location + "%"
        year = input("Enter year: ")
        cur.execute("""Select C.Model, AVG(C.Price), COUNT(C.Model) from car as C 
                    where C.Make = '{}' and C.Body_type = '{}' and C.make_year = {} and C.Location LIKE '{}'
                    group by 1;""".format(make, body_type, int(year), location))
        rows = cur.fetchall()
        rows = pd.DataFrame(rows,columns=['Model', 'Average Price', 'Count'])
        rows = tabulate(rows, headers='keys', tablefmt='psql')
        print(rows)
    elif choice == '6':
        location = input("Enter location: ")
        location = "%" + location + "%"
        min_price = input("Enter min price: ")
        max_price = input("Enter max price: ")
        no_features = input("Enter number of features: ")
        q_features = ""
        for i in range(int(no_features)):
            feature= input("Enter feature: ")
            q_features = q_features + "F.features like '%" + feature + "%' or "
        q_features = q_features[:-4]
        print(q_features)
        query = "select C.AD_ID, Make, Model, Price, Owner_Phone_number from car as C inner join car_features as F on C.AD_ID = F.AD_ID where C.Cond = 'Used' and C.Price <{} and C.Price > {} and C.Location like '{}' and {} group by 1,2,3,4,5;".format(int(max_price), int(min_price), location, q_features)
        # print(query)
        # print(query_2)
        cur.execute(query)
        rows = cur.fetchall()
        rows = pd.DataFrame(rows,columns=['AD ID','Make','Model', 'Price', 'Owner Phone number'])
        rows = tabulate(rows, headers='keys', tablefmt='psql')
        print(rows)
    elif choice == '7':
        make = input("Enter make: ")
        model = input("Enter model: ")
        cur.execute("""Select C.Location, AVG(C.Price), COUNT(C.AD_ID) from car as C 
                    where C.Make = '{}' and C.Model = '{}'and C.Location like '%_airo%'
                    group by 1
                    order by 3 desc
                    limit 5;""".format(make, model))
        rows = cur.fetchall()
        rows = pd.DataFrame(rows,columns=['Location', 'Average Price', 'Count'])
        rows = tabulate(rows, headers='keys', tablefmt='psql')
        print(rows)
    elif choice == '8':
        cur.execute("""Select O.Username, O.Phone_number, COUNT(C.AD_ID), AVG(C.Price) from car as C 
                    inner join owner_agent as O
                    on C.Owner_Phone_number = O.Phone_number
                    group by 1,2
                    order by 3 desc
                    limit 5;""")
        rows = cur.fetchall()
        rows = pd.DataFrame(rows,columns=['Name', 'Phone number','Count', 'Average Price'])
        rows = tabulate(rows, headers='keys', tablefmt='psql')
        print(rows)
    elif choice == '9':
        ch = input("1- select using Phone number\t2- select using Owner name : ")
        if ch == '1':
            phone_number = input("Enter Phone number: ")
            cur.execute("""select C.AD_ID, C.Make, C.Model, C.Price, C.make_year from car as C 
                        where C.Owner_Phone_number = '{}';""".format(phone_number))
        elif ch == '2':
            name = input("Enter Owner name: ")
            cur.execute("""select C.AD_ID, C.Make, C.Model, C.Price, C.make_year from car as C 
                        inner join owner_agent as O
                        on C.Owner_Phone_number = O.Phone_number
                        where O.username = '{}';""".format(name))
        rows = cur.fetchall()
        rows = pd.DataFrame(rows,columns=['AD ID','Make','Model', 'Price', 'Year'])
        rows = tabulate(rows, headers='keys', tablefmt='psql')
        print(rows)
    elif choice == '10':
        F = input("Range year from : ")
        T = input("Range year to : ")
        cur.execute("""Select Model, Make, Count(AD_ID), AVG(Price) from car as C
                    where make_year > {} and make_year<{}
                    group by 1,2
                    order by 3 desc
                    limit 5;""".format(int(F), int(T)))
        rows = cur.fetchall()
        rows = pd.DataFrame(rows,columns=['Model','Make','Count', 'Average Price'])
        rows = tabulate(rows, headers='keys', tablefmt='psql')
        print(rows)
    elif choice == '11':
        exit = True
    else:
        print("wrong input, re-enter choice") 