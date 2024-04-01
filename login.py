import sqlite3
import pwinput

def create(): #create account, uses sqlite3
    firstName = input("Account Details\nFirst Name: ").upper() #input all personal data
    lastName = input("Last Name: ").upper()
    dOBirth = input("Date of birth (MM/DD/YY): ")
    address = input("Input address: ")
    phoneNumber = input("Phone Number: ")
    emailAdd = input("Email: ").upper()
    password = pwinput.pwinput(prompt='Password: ', mask='*')

    conn = sqlite3.connect('flights.db') #connect to database, then insert inputted information above into the passengers table
    conn.execute("INSERT INTO PASSENGER (FIRSTNAME, LASTNAME, DOBIRTH, ADDRESS, PHONENUMB, EMAIL, PASSWORD) VALUES (?, ?, ?, ?, ?, ?, ?)", (firstName, lastName, dOBirth, address, phoneNumber, emailAdd, password))

    conn.commit() #saves the data that was inputted into the database
    print("Account created successfully!") #success message
    ID = conn.execute("SELECT last_insert_rowid()").fetchone()[0] #fetches the ID of the account that was just created, to be used for assigning flight to IDs
    conn.close() #closes the connection with the database
    return ID #returns the ID to be used


def login(): #login account, accesses database and checks if user exists
    emailAdd = input("Email: ").upper()
    firstName = input("Passenger Name\nFirst Name: ").upper()
    lastName = input("Last Name: ").upper()
    password = pwinput.pwinput(prompt='Password: ', mask='*')

    conn = sqlite3.connect('flights.db') #connects to database, then selects the ID that has the information that matches with the user inputted firstname, lastname, and email address
    
    cursor = conn.execute("SELECT ID FROM PASSENGER WHERE FIRSTNAME=? AND LASTNAME=? AND EMAIL=? AND PASSWORD=?", (firstName, lastName, emailAdd, password))
    user = cursor.fetchone() #fetches the id

    if user is None: #if there is no id that matches, then returns this error message
        print("No user found with the corresponding data. Please make sure you entered the correct data and try again.")
        return None
    else: #if there is a user, it logs in and returns the ID
        ID = user[0]
        print("\nLogged in successfully!")
    
    conn.close() #closes the connection to database
    return ID



