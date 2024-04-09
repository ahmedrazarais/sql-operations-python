import mysql.connector
from config import DB_HOST, DB_PASSWORD, DB_USER


# creating a class for basic operations
class Sql_Operations:
    def __init__(self):
        try: # make connection with server
            self.connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD)
            # make a pointer for further use
            self.cursor = self.connection.cursor()
            print("Connection Succeed.")
        except mysql.connector.Error as e:
            print(f"Error In connection : {e}")
            print("Getting Error in connection.Make sure you update config.py file")
            exit()

    def create_database(self):
        try:
            # Check if the database 'operations' exists
            self.cursor.execute("SHOW DATABASES LIKE 'operations'")
            database_exists = self.cursor.fetchone()
            if not database_exists:
                # Create the database only if it doesn't exist
                self.cursor.execute("CREATE DATABASE operations")
                print("Database Created successfully.")
            else:
                print("Database already exists.")
        except mysql.connector.Error as e:
            print(f"Error in creation of database {e}")

    def create_table(self):
        try:
            # Using the 'college' database
            self.cursor.execute("USE operations")

            # Check if the 'students' table exists
            self.cursor.execute("SHOW TABLES LIKE 'admin'")
            table_exists = self.cursor.fetchone()
            if not table_exists:
                # Create the 'students' table only if it doesn't exist
                query = """CREATE TABLE admin (
                            id INT PRIMARY KEY,
                            name VARCHAR(20),
                            city VARCHAR(30),
                            subject VARCHAR(50)
                        )"""
                self.cursor.execute(query)
                print("Table created successfully")
            else:
                print("Table already exists.")
        except mysql.connector.Error as e:
            print(f"Error in table creation: {e}")
    
    # Mehtoid to close connection
    def close_connection(self):
        # Close database connection
        try:
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
                print("Connection to MySQL database closed.")
        except mysql.connector.Error as e:
            print(f"Error closing connection: {e}")

    # Make a mehtod to retrieve data details from table
    def retrieve_data(self):

        try: # retrieve data from students table
             # Using the 'operations' database
            self.cursor.execute("USE operations")
            self.cursor.execute("SELECT * FROM admin")
            data=self.cursor.fetchall()
            return data
        except mysql.connector.Error as e:
            print(f"Error in retrieving data : {e}")

    # mehtod to view data-details
    def display_data(self):
        data=self.retrieve_data() # calling mehtod to get data list from table
        # check if data contains any value
        if data:
            try:
                print()
                print("ID\t\tName\t\tCity\t\tSubject")
                print("---------------------------------------------------------------")   
                for id,name,city,subject in data:
                        print(f"{id}\t\t{name}\t\t{city}\t\t{subject}")
                print()
                return
            except mysql.connector.Error as e:
                print(f"Error In Display data: {e}")
        else:
            print("\nSorry!The database  is empty at this moment.No data to display.\n")
    

    # mehtod to delete any data:
    def delete_row(self):

        data=self.retrieve_data() # calling mehtod to get data list from table
        # check if data contains any value
        if data:
            self.display_data()
            print()
            while True:
                try:
                    row_id=int(input("Enter id of row you want to delete (enter 0 to go back):"))
                    if row_id==0:   # want to go back
                        print("Return to previous menu..")
                        return
                  
                    # Search for the row with the provided ID
                    found = False
                    for row in data:
                        if row_id==row[0]:  # If id matches
                            found=True
                            break
                    # if id found
                    if found:
                            print("Wait..Id Found wait for a moment to delete..\n")
                            query="DELETE FROM admin WHERE id=%s"
                            self.cursor.execute(query,(row_id,))
                            self.connection.commit()  # commit query
                            print("Row Deleted Successfully.For more check View data.\n")
                            return # return after deletion
                    else: # if id not matches
                        print("Id Not matches Please Give appropiate id.\n")

                except ValueError:
                    print("Error: Id must be integer\n")
        # if table is empty
        else:
            print("\nSorry!The database  is empty at this moment.Can't Delete Anything rightnow!.\n")

    

    # mehtod to take id (primary key) input
    def id_input(self):
        data=self.retrieve_data() # calling mehtod to get data list from table
        # taking id input
        while True:
            try:
                id_input=int(input("Enter Id to assign to employee (enter 0 to back):"))
                if id_input==0:   # if want to go back
                    print("Return To previous Options..\n")
                    return
                
                # check id must not be repeated beacuse of primary key
                if data:
                    found = False
                    for row in data:
                        if id_input==row[0]:  # If id matches
                            found=True
                            break
                    if found:
                        print("Please Select another Id This id alraedy exists.\n")
                    # if id not matches
                    else:
                        print("Id assign successfully\n")
                        return id_input
                # for initial when no data enter
                else:
                    print("Id assign successfully\n")
                    return id_input
    
            # if getting id rather than in number
            except ValueError:
                print("Please Enter In Digit Id must be in digit")

    # mehtod to take input employee name 
    def name_input(self):
            while True:
                name=input("Enter Employee name (enter 0 to go back):").strip()
                if name=="0":  # if he want to go back
                    print("Going back To previous Menu...\n")
                    return    
                # Checking not be empty
                if not name:
                    print("Name is compulsory to set..\n")
                    continue
                # condition only alphabets allowed
                if not all(char.isalpha() for char in name):
                    print("Only alphabets allowed in name\n")
                    continue
                # after all fullfilled results
                print("Name added successfully\n")
                return name
            
    # mehtod to take input city-name 
    def city_input(self):
            while True:
                city_name=input("\nEnter Employee City name (enter 0 to go back):").strip()
                if city_name=="0":  # if he want to go back
                    print("Going back To previous Menu...\n")
                    return    
                # Checking not be empty
                if not city_name:
                    print("City-Name is compulsory to set..\n")
                    continue
                # condition only alphabets allowed
                if not all(char.isalpha() for char in city_name):
                    print("Only alphabets allowed in city-name\n")
                    continue
                # after all fullfilled results
                print("\nCity Added Successfully.\n")
                return city_name
            



    # mehtod to take input subject
    def subject_input(self):
            while True:
                subject=input("Enter Employee Subject (enter 0 to go back):").strip()
                if subject=="0":  # if he want to go back
                    print("Going back To previous Menu...\n")
                    return    
                # Checking not be empty
                if not subject:
                    print("Subject is compulsory to set..\n")
                    continue
                # condition only alphabets allowed
                if not all(char.isalpha() for char in subject):
                    print("Only alphabets allowed in Subject\n")
                    continue
                # after all fullfilled results
                print("\nSubject Added successfully.")
                return subject

    # mehtod to insert daat in table
    def insert_data(self,id,name,city,subject):
        try:
            self.cursor.execute("USE operations ")
            query="INSERT INTO admin (id,name,city,subject) VALUES (%s,%s,%s,%s)"
            self.cursor.execute(query,(id,name,city,subject))
            self.connection.commit()
            print("Congratulations Data Added Successfully.")
        
        except mysql.connector.Error as e:
            print(f"Error as {e}")


    # process for adding data in table
    def adding_data_process(self):
        id=self.id_input()
        # check to get all input correctly
        if id:
            name=self.name_input()
            if name:
                city=self.city_input()
                if city:
                    subject=self.subject_input()
                    if subject:
                        # calling insert data mehtod to insert data in table
                        self.insert_data(id,name,city,subject)

                    else:
                        print("Not get subject..return from here..\n")
                else:
                    print("Not get city..return from here..\n")
            else:
               print("Not get name..return from here..\n")
        else:
            print("Not get Id..return from here..\n")
                        # If get all inputs then insert data into table



    # mehtod for update details
    def update_data(self):
        data=self.retrieve_data() # calling mehtod to get data list from table
        # taking id input
        # check if data contains any value
        if data:
            self.display_data()
            print()
            while True:
                try:
                    row_id=int(input("Enter id of row you want to Update Its Details (enter 0 to back) :"))
                    if row_id==0:
                        print("Return to previous menu..")
                        return
                    # match with databse id
                    # Search for the row with the provided ID
                    found = False
                    for row in data:
                        if row_id==row[0]:  # If id matches
                            found=True
                            break
                    # if id found
                    if found:
                        print(f"Now what you update is update for employee with id {row_id}")
                        print("\t\tWelcome To update Details Area\n")
                        # When ifd found then display choices
                        while True:
                            print("\t1.Update Employee Name.")
                            print("\t2.Update Employee City-Name.")
                            print("\t3.Update Employee Subject.")
                            print("\t4.Exit From Update Area\n.")
                        # taking input of choice in update area
                            update_choice=input("Enter Your Choice In Update area:").strip()
                            if update_choice=="1":
                                  name=self.name_input()
                                  if name:
                                      self.cursor.execute("UPDATE admin SET name=%s WHERE id=%s", (name,row_id))
                                      self.connection.commit()
                                      print("Upadte has been done successfully.\n")
                                      self.display_data()

                            elif update_choice=="2":
                                city=self.city_input()
                                if city:
                                      self.cursor.execute("UPDATE admin SET city=%s WHERE id=%s", (city, row_id))
                                      self.connection.commit()
                                      print("Upadte has been done successfully.\n")
                                      self.display_data()
                            elif update_choice=="3":
                                subject=self.subject_input()
                                if subject:
                                      self.cursor.execute("UPDATE admin SET subject=%s WHERE id=%s", (subject,row_id))
                                      self.connection.commit()
                                      print("Upadte has been done successfully.\n")
                                      self.display_data()
                                
                            elif update_choice=="4":
                                print("Return from Update Area..\n")
                                return
                            else:
                                print("Invalid Choice.Please Select From Given Choices\n")
                        
                    else:
                        print("Id Not Match.Please Enter Valid Id.\n")

                except ValueError:
                    print("Please Enter In Digits.\n")
        
        else:
           print("\nSorry!The database  is empty at this moment.Can't Update Anything rightnow!.\n")


        # Admin login
    def admin_login(self):
        admin_username = "admin"    # Admin username
        admin_password = "admin123"   # admin password

        # Ask the user for the username and password
        while True:
            username = input("Enter Admin Username (enter 0 to back): ")
            if username == "0":
                return
            # Check if the username is correct
            if username == admin_username:
                break
            else:
                print("Incorrect Username")
                print()
        # when username is correct then ask for password
        while True:
                password = input("Enter Admin Password (enter 0 to back): ")
                if password == "0":
                    return
                
                # Check if the password is correct
                if password == admin_password:
                    print("Login Successful!!")
                    print()
                    return "login"
                else:
                    print("Incorrect Password")
                    print()
        # open panel when username and password both are correct


    # mehtod mainpage control for user
    def main_page(self):
            print("\n\t\tWelcome To Sql Operations\n")
            print("Enter Admin Credentials To Unlock the system.\n")
            login=self.admin_login()
            if login:
                # loop to stuck him in choices untill he want to go back
                while True:
                    # display details 
                    print("\t1.View Data From Database.")
                    print("\t2.Insert Data In Database.")
                    print("\t3.Delete Data From Database.")
                    print("\t4.Update Database in Database.")
                    print("\t5.Exit from sql opertaions.\n\n")
                # taking user choice
                    get_choice=input("Enter Your Choice In sql-operations:").strip()
                    # calling respective mehtiods on choices
                    if get_choice=="1":
                        self.display_data()
                    elif get_choice=="2":
                        self.adding_data_process()
                    elif get_choice=="3":
                        self.delete_row()
                    elif get_choice=="4":
                        self.update_data()

                    elif get_choice=="5":
                        print("Exiting From Sql-Opeartions..")
                        print("Good Bye .See You Soon")
                        return  # If he want to exit
                    else: # if invalid choice
                        print("Invalid Choice.Please Select From Given Choice.\n")
            else:
                print("login is mandatory to enter in system.")


# Create an instance of Sql_Operations class
operation = Sql_Operations()
# Call the methods to create the database and table
# operation.create_database()
# operation.create_table()

# calling main page
operation.main_page()
operation.close_connection()