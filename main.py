import json
import time
from bs4 import BeautifulSoup as bs
import constants
from functions import check_hour, get_room_data, get_time_slots, get_times_between_xy, make_reservation
from sys import argv

now = time.time()
if len(argv) != 4:
    print("\nUSAGE: python3 [start time] [end time] [user name]\n")
    print("NOTE: Times in 24 hour format")
    exit()

START_TIME = argv[1]
END_TIME = argv[2]
USER = argv[3]
START_TIME = f"2022-05-30 {START_TIME}"
END_TIME = f"2022-05-30 {END_TIME}"
# START_TIME = f"{str(constants.TODAY)} {START_TIME}"
# END_TIME = f"{str(constants.TODAY)} {END_TIME}"

# START_TIME = "2022-05-18 13:00:00" 
# print('START_TIME: ', START_TIME)

# END_TIME = "2022-05-18 16:00:00" 
# print('END_TIME: ', END_TIME)
TIMES = get_times_between_xy(start_time=START_TIME, end_time=END_TIME)[0:-1]

user_data = None
with open("users.json") as f:
    user_data = json.load(f)

if USER in user_data:
    times_json = get_time_slots()["slots"]
    room_to_check = constants.ROOMS[210]
    print("Looking for room...")
    print("\t", START_TIME)
    print("\tconstants.TODAY", constants.TODAY)
    for room_key, room_val in constants.ROOMS.items():
        room_data = get_room_data(times_json, room_val)
        time_info = check_hour(room_data, TIMES)     
        if len(time_info) == len(TIMES):
            make_reservation(time_info, TIMES, END_TIME, room_key, USER)
            print(f"Booked room: {room_key} between {TIMES[0]} and {END_TIME}")
            break
else: 
    print("User not in database") 
    

end = time.time()
print(f"Time elapsed: {end - now}")
