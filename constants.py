from datetime import date, timedelta

ROOMS = {
        107: 128080,
        108: 128209,
        110: 128210, 
        111: 128212,
        112: 128213,
        113: 128211,
        123: 128214,
        210: 128215 
        }

COOKIES = None

DAYS = {0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
        }

TODAY = date.today()
TODAY_PLUS_THREE = TODAY + timedelta(days=3)