import time
from bs4 import BeautifulSoup as bs
import constants
from functions import check_hour, get_room_data, get_time_slots, get_times_between_xy, make_reservation

now = time.time()

# START_TIME = "2022-05-14 13:00:00" 
START_TIME = "16:00:00" # TODO Turn this time in argv[0]
START_TIME = f"{str(constants.TODAY)} {START_TIME}"

# END_TIME = "2022-05-14 16:00:00" 
END_TIME = "16:30:00" # TODO Turn this time in argv[1]
END_TIME = f"{str(constants.TODAY)} {END_TIME}"

TIMES = get_times_between_xy(start_time=START_TIME, end_time=END_TIME)[0:-1]

times_json = get_time_slots()["slots"]
room_to_check = constants.ROOMS[210]
print("Looking for room...")
for room_key, room_val in constants.ROOMS.items():
    room_data = get_room_data(times_json, room_val)
    time_info = check_hour(room_data, TIMES)     
    if len(time_info) == len(TIMES):
        make_reservation(time_info, TIMES, END_TIME, room_key)
        print(f"Booked room: {room_key} between {TIMES[0]} and {END_TIME}")
        break

end = time.time()
print(f"Time elapsed: {end - now}")
