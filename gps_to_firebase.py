from gps import *
import time
import pyrebase

firebaseConfig = {
    "apiKey": "xxxx",
    "authDomain": "xxxx",
    "databaseURL": "xxxx",
    "projectId": "xxxx",
    "storageBucket": "xxxx",
    "messagingSenderId": "xxxx",
    "appId": "xxxx",
    "measurementId": "xxxx"}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

running = True
n = 0

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

try:
    print("Application started!")
    while running:
        nx = gpsd.next()
        if nx['class'] == 'TPV':
            n += 1
            loc = "Location" + str(n)
            latitude = getattr(nx, 'lat', "Unknown")
            longitude = getattr(nx, 'lon', "Unknown")
            print("Car's current location: lon = " + str(longitude) + ", lat = " + str(latitude))
            latlng = str(latitude) + ',' + str(longitude)
            db.child("Thief").child(loc).set(latlng)
        time.sleep(1.0)

except KeyboardInterrupt:
    running = False
    print("Applications closed!")
