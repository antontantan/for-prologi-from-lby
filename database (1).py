import sqlite3

### DOWNLOAD SQLITE VIEWER FOR VSCODE to view database for easier visualization



#sets conn variable as this command (syntax reasons)
conn = sqlite3.connect('flights.db')
#creates a table with the ff columns if it does not exist
conn.execute('''CREATE TABLE IF NOT EXISTS PASSENGER
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             FIRSTNAME      TEXT NOT NULL,
             LASTNAME       TEXT NOT NULL,
             DOBIRTH        INTEGER NOT NULL,
             ADDRESS        CHAR(50) NOT NULL,
             PHONENUMB      INTEGER,
             EMAIL          CHAR(50),
             PASSWORD       TEXT NOT NULL)''')

conn.close()

from datetime import datetime, timedelta

# list of airports
airports = ['CEB', 'DVO', 'MNL', 'SIN', 'HND', 'ICN']

# approximate flight durations in hours for dictionary use
flightDurations = {
    ('CEB', 'DVO'): 1, ('DVO', 'CEB'): 1,
    ('CEB', 'MNL'): 1.5, ('MNL', 'CEB'): 1.5,
    ('CEB', 'SIN'): 3.5, ('SIN', 'CEB'): 3.5,
    ('CEB', 'HND'): 5.5, ('HND', 'CEB'): 5.5,
    ('CEB', 'ICN'): 7, ('ICN', 'CEB'): 7,
    ('DVO', 'MNL'): 2, ('MNL', 'DVO'): 2,
    ('DVO', 'SIN'): 5.5, ('SIN', 'DVO'): 5.5,
    ('DVO', 'HND'): 5, ('HND', 'DVO'): 5,
    ('DVO', 'ICN'): 7, ('ICN', 'DVO'): 7,
    ('MNL', 'SIN'): 3.5, ('SIN', 'MNL'): 3.5,
    ('MNL', 'HND'): 4, ('HND', 'MNL'): 4,
    ('MNL', 'ICN'): 4, ('ICN', 'MNL'): 4,
    ('SIN', 'HND'): 7, ('HND', 'SIN'): 7,
    ('SIN', 'ICN'): 6.5, ('ICN', 'SIN'): 6.5,
    ('HND', 'ICN'): 2, ('ICN', 'HND'): 2
}

# create a database and a table for the flights
conn = sqlite3.connect('flights.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS FLIGHTS (
        flight_id INTEGER PRIMARY KEY,
        scheduledDeparture TEXT NOT NULL,
        scheduledArrival TEXT NOT NULL,
        departureAirport TEXT NOT NULL,
        arrivalAirport TEXT NOT NULL);''')

# generate flight schedules for a day
flight_id = 1
for departureAirport in airports:
    for arrivalAirport in airports:
        if departureAirport != arrivalAirport:
            # start flights at 6:00
            scheduledDeparture = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
            while True:
                # the scheduled arrival is based on the flight duration
                flightDuration = flightDurations.get((departureAirport, arrivalAirport))
                if flightDuration is None:
                    # if there's no direct flight duration, assume a layover and double the longest direct flight duration (not used, for future use?)
                    flightDuration = max(flightDurations.values()) * 2
                scheduledArrival = scheduledDeparture + timedelta(hours=flightDuration)
                c.execute('''INSERT INTO flights (flight_id, scheduledDeparture, scheduledArrival, departureAirport, arrivalAirport)
                    VALUES (?, ?, ?, ?, ?)''', (flight_id, scheduledDeparture.strftime('%H:%M'), scheduledArrival.strftime('%H:%M'), departureAirport, arrivalAirport))
                flight_id+=1
                # schedule the next flight 30 minutes after the arrival of the current flight
                if 6 < scheduledArrival.hour < 21.5:
                    scheduledDeparture = scheduledArrival + timedelta(minutes=30)
                else: 
                    break

# Commit the changes and close the connection
conn.commit()
conn.close()

#create bookings table, maybe remove login function instead and have the user input name and details for easier use
conn.execute('''CREATE TABLE IF NOT EXISTS BOOKINGS
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             USERID            INT NOT NULL,
             FLIGHTCODE             TEXT NOT NULL,
             DOFLIGHT             INTEGER  NOT NULL,
             CLASS               INTEGER NOT NULL);''')

conn.close()
