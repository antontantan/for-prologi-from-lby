import sqlite3
import login
import pwinput
from tabulate import tabulate #tabulate module enables the tabulate() function
from datetime import date

bookings = []

def LogInSystem():
    LogIn = True
    while LogIn == True: #account login/creation function loop
        account = input("Do you have a PySkyFlight account? (Yes/No)\n").lower()
        if account.lower() == 'yes':
            print("\nPlease enter your email and name to log in:")
            accID = login.login() #login function that checks if account exists and matches details provided by user
            if accID == None:
                continue
            else:
                LogIn = False
        elif account.lower() == 'no':
            print("\nCreate an account through personal details:")
            accID = login.create() #creates an entry into the database that contains all the information needed
            LogIn = False
        elif accID == None:
            continue
        else:
            continue


def mainMenu():
    print("\n= = = = PySkyFlight = = = =")
    print("Welcome to PySkyFlight!")
    print("Select action:")
    print("[1] Flight Booking")
    print("[2] Flight Status")
    print("[3] Flight Cancellation") 
    print("[4] Quit the Program")
    print("[5] Log Out")
    
def passportDetails():
    print("\nPassport Details (if international flight)")
    passportNumber = input("Passport Number: ")
    passportName = input("Name on Passport: ")
    passportDateIssued = input("Date Issued: ")
    passportExpiryDate = input("Expiry Date: ")
    passportPlaceIssued = input("Place Issued: ")
    return passportNumber, passportName, passportDateIssued, passportExpiryDate, passportPlaceIssued

def paymentDetails():
    print("\nPayment")
    paymentLastName = input("Last Name: ")
    paymentFirstName = input("First Name: ")
    paymentMiddleName = input("Middle Name: ")
    creditCardNumber = input("Credit Card Number: ")
    creditCardExpiry = input("Expiry Date: ")
    securityCode = input("Security Code: ")
    return paymentLastName, paymentFirstName, paymentMiddleName, creditCardNumber, creditCardExpiry, securityCode

def passengerInfo():
    print("\nPassenger Details")
    lastName = input("Last Name: ")
    firstName = input("First Name: ")
    middleName = input("Middle Name: ")
    emailAddress = input("Email Address: ")
    contactNumber = input("Contact Number: ")
    return lastName, firstName, middleName, emailAddress, contactNumber

def flighttimes(departureLocation, returnLocation):
    flightdb = sqlite3.connect('flights.db') #connects to flight database, where all flightids and schedules with the correct departure and arrival locations are returned
    cursor = flightdb.execute("SELECT flight_id, scheduledDeparture, scheduledArrival FROM flights WHERE departureAirport = ? AND arrivalAirport = ?", (departureLocation, returnLocation))
    flightSchedule = cursor.fetchall()
    return flightSchedule

def selection(flightSchedule, flight1, flight2): #for printing the formatted flightschedule with the proper date and time and choosing the schedule wanted
    print("\nPlease select your preferred time slot for your flight from "+ flight1 +" to "+ flight2 + ".") #prints formatted schedule with timeslot
    flightScheduleData = []
    for i, flight in enumerate(flightSchedule, 1):
        flightScheduleData.append([f"{i}.", f"SKY{flight[0]}", f"{flight[1]}", f"{flight[2]}"])
    print(tabulate(flightScheduleData, headers=["Flight Number", "Flight ID", "Departure Time", "Arrival Time"], tablefmt="grid"))
        
    
    while True:
        userInput = str(input("Please select the flight number: "))
        if userInput.isdigit() == True:
            userInput = int(userInput)
            if 1 <= userInput <= len(flightSchedule): #checks if user input is within the range offered by the schedule, if not repeats the selection
                flightChoice = flightSchedule[userInput - 1] #sets flight choice as the array that matches the selected schedule
                print(f"You have selected Flight ID: PSF{flightChoice[0]}")
                break
            else:
                 print("Invalid selection. Please choose a valid flight number.")
        else:
            print("Invalid selection. Please choose a valid flight number.")
            quit = print("")
    return flightChoice

def bookFlight():
    print("===========================================================")
    print("\nPySkyFlight - Flight Booking")

    locationDict = {
        '1': 'MNL',
        '2': 'CEB', 
        '3': 'DVO',
        '4': 'SIN',
        '5': 'ICN',
        '6': 'HND'
    }

    while True:
        while True:
            print(tabulate([["Number","Location"],["1.", "Manila(MNL)"], ["2.", "Cebu(CEB)"], ["3.", "Davao(DVO)"], ["4.", "Singapore(SIN)"], ["5", "South Korea(ICN)"], ["6", "Japan(HND)"]], headers="firstrow", tablefmt="github"))
            depin = str(input("\nPlease choose the number of your departure location: \n"))
            while (depin.isdigit() == False) or (int(depin) < 1) or (int(depin) > 6):
                depin = input("Please Enter a Valid Location): ")
            else:
                departureLocation = locationDict[depin]
                break
        

        while True:
            print(tabulate([["Number","Location"],["1.", "Manila(MNL)"], ["2.", "Cebu(CEB)"], ["3.", "Davao(DVO)"], ["4.", "Singapore(SIN)"], ["5", "South Korea(ICN)"], ["6", "Japan(HND)"]], headers="firstrow", tablefmt="github"))
            retin = str(input("\nPlease choose the number of your return location: \n"))
            while (retin.isdigit() == False) or (int(retin) < 1) or (int(retin) > 6):
                retin = input("Please Enter a Valid Location: ")
            else:
                returnLocation = locationDict[retin]
                break
        if departureLocation == returnLocation:
            print("The Departure and Return Locations are the same")
            continue
        else:
            break

    flightSchedule = flighttimes(departureLocation, returnLocation)

    flight1Date = input("Select Departure Flight Date (MM/DD/YY): ")
    flight1 = selection(flightSchedule, departureLocation, returnLocation)
    flight2Date = input("Select Return Flight Date (MM/DD/YY): ")
    flight2 = selection(flightSchedule, returnLocation, departureLocation)

    lastName, firstName, middleName, emailAddress, contactNumber = passengerInfo()

    isInternational = ""
    while isInternational.lower() not in ['yes', 'no']:
        isInternational = input("Is this an international flight? (yes/no): ").lower()
        if isInternational == 'yes':
            passportNumber, passportName, passportDateIssued, passportExpiryDate, passportPlaceIssued = passportDetails()
            paymentLastName, paymentFirstName, paymentMiddleName, creditCardNumber, creditCardExpiry, securityCode = paymentDetails()
        elif isInternational == 'no':
            paymentLastName, paymentFirstName, paymentMiddleName, creditCardNumber, creditCardExpiry, securityCode = paymentDetails()
    
    confirmBooking=""
    while confirmBooking.lower() not in ['yes', 'no']:
        confirmBooking = input("\nConfirm Booking? (yes/no): ")
        if confirmBooking.lower() == 'yes':
            bookingInfo = {
                "DepartureLocation": departureLocation,
                "Flight1Date": flight1Date,
                "Flight1": flight1,
                "ReturnLocation": returnLocation,
                "Flight2Date": flight2Date,
                "Flight2": flight2,
                "\nLastName": lastName,
                "FirstName": firstName,
                "MiddleName": middleName,
                "EmailAddress": emailAddress,
                "ContactNumber": contactNumber,
                "\nIsInternational": isInternational,
                "\nPaymentLastName": paymentLastName,
                "PaymentFirstName": paymentFirstName,
                "PaymentMiddleName": paymentMiddleName,
                "CreditCardNumber": creditCardNumber,
                "CreditCardExpiry": creditCardExpiry,
                "SecurityCode": securityCode
            }
            
            if isInternational.lower() == 'yes':
                bookingInfo["\nPassportName"] = passportName
                bookingInfo["PassportDateIssued"] = passportDateIssued
                bookingInfo["PassportExpiryDate"] = passportExpiryDate
                bookingInfo["PassportPlaceIssued"] = passportPlaceIssued
        
            bookings.append(bookingInfo)
        
            print("\nBooking confirmed!")
            print("Booking Details:")
            for key, value in bookingInfo.items():
                print(f"{key}: {value}")
            quit = input("Enter any key to return to the main menu.")
        
        elif confirmBooking.lower() == 'no':
            print("\nBooking canceled.")
            quit = input("Enter any key to return to the main menu.")


def checkFlightStatus(bookings):
    print("===========================================================")
    print("\nPySkyFlight - Flight Status")
    if not bookings:
        print("No bookings found. Return to the main menu and select the booking option.")
        quit = input("Enter any key to return to the main menu.")
    else:
        print("Flight Status:")

        for idx, booking in enumerate(bookings, start=1):
            print(f" \t Booking {idx}:")    
            flight1Data =[[f"{booking['DepartureLocation']} - {booking['ReturnLocation']}", f"{booking['Flight1Date']}", f"PSF{booking['Flight1'][0]}", f" {booking['Flight1'][1]} - {booking['Flight1'][2]}"]]
            print(tabulate(flight1Data, headers=["Flight 1 Itinerary", "Flight Date", "Flight Number", "Flight Time"], tablefmt="grid"))

            flight2Data = [[ f"{booking['ReturnLocation']} - {booking['DepartureLocation']}", f"{booking['Flight2Date']}",  f" PSF{booking['Flight2'][0]}",  f" {booking['Flight2'][1]} - {booking['Flight2'][2]}"]]
            print(tabulate(flight2Data, headers=["Flight 2 Itinerary", "Flight Date", "Flight Number", "Flight Time"], tablefmt="grid"))
          
       
        print( "\n \t STATUS: CONFIRMED")
        quit = input("Enter any key to return to the main menu.")

def cancelFlight(bookings):
    print("===========================================================")
    print("\nPySkyFlight - Flight Cancellation")
    if not bookings:
        print("No bookings found. Make sure you have booked a flight.")
        quit = input("Enter any key to return to the main menu.")
    else:
        print("Your Bookings:")
        for idx, booking in enumerate(bookings, start=1):
            CancelData = [[f"Booking {idx}", f"{booking['DepartureLocation']} - {booking['ReturnLocation']}", f"{booking['Flight1Date']} - {booking['Flight2Date']}"]]
            print(tabulate(CancelData, headers=["Booking Number", "Flight Departure and Return", "Flight Date"], tablefmt="grid"))

    cancelStart = True
    while cancelStart == True:
        cancelChoice = str(input("Enter the number of the booking you want to cancel (or type 'cancel' to exit): "))
        if cancelChoice.lower() == 'cancel':
                print("Cancellation aborted.")
                break
        elif cancelChoice.lower() != "cancel":
            if cancelChoice.isdigit() == False:
                print("Invalid booking number. Enter another number.")   
            elif cancelChoice.isdigit() == True:
                cancelIndex = int(cancelChoice) - 1
                if cancelIndex < 0 or cancelIndex >= len(bookings): 
                    print("Invalid booking number. Enter another number.")
                else:
                    cancelledBooking = bookings.pop(cancelIndex)
                    print("\n\t Flights Cancelled Successfully:")
                    DeletedData = [[f"{cancelledBooking['DepartureLocation']} - {cancelledBooking['ReturnLocation']} --- {cancelledBooking['Flight1Date']}", f"{cancelledBooking['ReturnLocation']} - {cancelledBooking['DepartureLocation']} --- {cancelledBooking['Flight2Date']}"]]
                    print(tabulate(DeletedData, headers=["Flight 1 Details", "Flight 2 Details"], tablefmt="grid"))
                    cancelStart = False
                    break
               
        
    quit = input("Enter any key to return to the main menu.")
                
def main():
    flightdb = flightdb = sqlite3.connect('flights.db')
    userpassword = "yay"
    passwordSystem = True

    print("Welcome to PySkyFlight!")

    LogInSystem()
    
    initiate = True
                
    while initiate:
        mainMenu()
        choice = input("Enter choice (1, 2, 3, 4, or 5): ")
        
        if choice.isdigit() == True:
            choice = int(choice)
            if (choice) == 1:
                bookFlight()
            elif (choice)  == 2:
                checkFlightStatus(bookings)
            elif (choice)  == 3:
                cancelFlight(bookings)
            elif (choice)  == 4:
                print("Thank you for using PySkyFlight. We hope to see you again!")
                initiate = False
            elif (choice)  == 5:
                confirm = input("Are you sure you want to log out of your account? (Yes/No)")
                if confirm.lower() == "yes":
                    LogInSystem()
                elif confirm.lower == "no":
                    continue
                else:
                    print("Invalid choice. Enter yes or no only.")
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
