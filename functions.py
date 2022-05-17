import time, requests, constants, os
from dotenv import load_dotenv
from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as bs

# DRIVER_PATH = f"{os.getcwd()}/chromedriver"
DRIVER_PATH = "/usr/bin/chromedriver"
URL = "https://pacific.libcal.com/spaces"

def get_time_slots():
    headers = {
        'authority': 'pacific.libcal.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://pacific.libcal.com',
        'referer': 'https://pacific.libcal.com/spaces',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'lid': '15370',
        'gid': '0',
        'eid': '-1',
        'seat': '0',
        'seatId': '0',
        'zone': '0',
        'accessible': '0',
        'powered': '0',
        'start': str(constants.TODAY),
        'end': str(constants.TODAY_PLUS_THREE),
        'pageIndex': '0',
        'pageSize': '18',
    }
    response = requests.post('https://pacific.libcal.com/spaces/availability/grid', headers=headers, data=data)
    json_object = response.json()
    return json_object

def get_room_data(time_slots_json: dict, room_number: int) -> dict:
    room_data = dict() 
    for i in range(len(time_slots_json)):
        if time_slots_json[i]['itemId'] == room_number:
            start_time = time_slots_json[i]['start']
            slot_info = time_slots_json[i]
            room_data[start_time] = slot_info 
    return room_data

def get_times_between_xy(start_time: str, end_time: str) -> list:
    # format: "yyyy-mm-dd hh:mm:ss"
    time_delta = 30 #? 30 minutes
    times_between = [start_time]
    date_format_str = "%Y-%m-%d %H:%M:%S" 

    temp_time = start_time
    dt_obj = datetime.strptime(temp_time, date_format_str)

    str_dt_obj = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
    while  str_dt_obj != end_time:
        dt_obj += timedelta(minutes=time_delta)
        str_dt_obj = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
        times_between.append(str_dt_obj)

    return times_between


def check_hour(room_data: dict, times_between:list) -> dict:
    slot_and_data = {}
    for key, val in room_data.items():
        for time in times_between:
            if time in key and len(val) == 4: #? Len=5 when there is a flag for already booked, len=4 otherwise
                slot_and_data[key] = val
    return slot_and_data 
    
def make_reservation(time_info:dict, TIMES:list, END_TIME, room):
    start_time, end_time = TIMES[0], TIMES[-1]

    xpath_row = 0 
    for i, val in enumerate(constants.ROOMS):
        xpath_row = i
        if room == val:
            xpath_row += 2
            break
    
    options = Options()
    # options.headless = True
    options.add_argument("--headless")
    options.add_argument("--window-size=1420,1080")
    options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
    # print(f"\n\n {DRIVER_PATH} \n\n")
    driver = webdriver.Chrome(DRIVER_PATH, chrome_options=options)
    # driver = webdriver.Chrome(DRIVER_PATH)

    driver.get(URL)
    html = driver.page_source
    print("Webdriver returned Source")

    soup = bs(html, 'lxml')
    title_html_tag = convert_time_to_xpath_readable(start_time, room)
    if int(title_html_tag[0:2]) >= 13: # changes 24 hour format to 12 hour format
        new_hour = int(title_html_tag[0:2]) - 12
        title_html_tag = str(new_hour) + title_html_tag[2:]
    

    element_to_xpath = soup.find('a', title=title_html_tag)
    xpath_to_click = xpath_soup(element_to_xpath)
    # print()
    # print('title_html_tag: ', title_html_tag)
    # print('element_to_xpath: ', element_to_xpath)
    # print('xpath_to_click: ', xpath_to_click)
    # print()
    driver.find_element_by_xpath(xpath_to_click).click()

    time.sleep(0.5)

    select = Select(driver.find_element_by_xpath('/html/body/div[2]/main/div/div/div/div[7]/form/fieldset/div[1]/div/div/div/div/select'))
    select.select_by_index(len(TIMES) - 1)
    
    print("Got past select drop-down for hours")
    time.sleep(0.5)

    # trash_button = "/html/body/div[2]/main/div/div/div/div[7]/form/fieldset/div[1]/div/div/div/div/div/button"
    # driver.find_element_by_xpath(trash_button).click()

    submit_times_button = "/html/body/div[2]/main/div/div/div/div[7]/form/fieldset/div[2]/button"
    driver.find_element_by_xpath(submit_times_button).click()
    
    print("Got past submit times")
    time.sleep(0.5)
    
    continue_button = "/html/body/div[2]/main/div/div/div/div[8]/div[2]/form/div[2]/button"
    driver.find_element_by_xpath(continue_button).click()
    
    print("Got past continue button")
    time.sleep(0.5)

    ###* Filling in personal info
    load_dotenv('info.env')
    print("Loaded dot_env")

    first_name_xpath = "/html/body/div[2]/main/div/div/div/div[8]/div[3]/form/div[2]/div[2]/input"
    driver.find_element_by_xpath(first_name_xpath).send_keys(os.getenv("first_name"))
    print("Entered first name")

    last_name_xpath = "/html/body/div[2]/main/div/div/div/div[8]/div[3]/form/div[2]/div[3]/input"
    driver.find_element_by_xpath(last_name_xpath).send_keys(os.getenv("last_name"))
    print("Entered last name")

    email_xpath = "/html/body/div[2]/main/div/div/div/div[8]/div[3]/form/div[3]/div/input"
    driver.find_element_by_xpath(email_xpath).send_keys(os.getenv("email"))
    print("Entered Email")

    univ_id_xpath = "/html/body/div[2]/main/div/div/div/div[8]/div[3]/form/div[4]/div/input"
    driver.find_element_by_xpath(univ_id_xpath).send_keys(os.getenv("univ_id"))
    print("Entered university id")
    
    select = Select(driver.find_element_by_xpath("/html/body/div[2]/main/div/div/div/div[8]/div[3]/form/div[6]/div/select"))
    select.select_by_index(7)
    print("Entered SOESCS")
    ###*^^^^^^^^^^^^^^^^^

    submit_booking_button = "/html/body/div[2]/main/div/div/div/div[8]/div[3]/form/div[9]/div/button"
    driver.find_element_by_xpath(submit_booking_button).click()
    driver.quit()

    
def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:  # type: bs4.element.Tag
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name if 1 == len(siblings) else '%s[%d]' % (
                child.name,
                next(i for i, s in enumerate(siblings, 1) if s is child)
                )
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

def convert_time_to_xpath_readable(time_info:str, room):
    """ Args:
        time (str): ex. 2022-05-14 10:00:00
        result (str): "10:00am Saturday, May 14, 2022 - Room 107 - Available"
    """
    split = time_info.split()
    inp_date, time = split[0], split[1]
    time = datetime.strptime(time, "%H:%M:%S").strftime("%H:%M%p").lower()
    d = datetime.strptime(inp_date, "%Y-%m-%d")
    day_of_week = date(d.year, d.month, d.day).weekday()
    return f"{time} {constants.DAYS[day_of_week]}, {d.strftime('%b %d, %Y')} - Room {room} - Available"

def get_todays_YMD():
    d = datetime.now()
    return f"{d.year}-{d.month}-{d.day}" 
