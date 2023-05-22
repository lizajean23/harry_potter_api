import requests
import sqlite3
import json
import win10toast
from datetime import datetime

#
# # 1
character = requests.get('https://hp-api.onrender.com/api/characters')
print(character.headers)
print(character.text)
print(character.content)
#
# # 2
characters = character.json()
with open('harry_potter.json', 'w') as file:
    json.dump(characters, file, indent=4)
#
# # 3
values = []
index = 0
for each in characters:
    name = characters[index]['name']
    species = characters[index]['species']
    gender = characters[index]['gender']
    house = characters[index]['house']
    date_of_birth = characters[index]['dateOfBirth']
    ancestry = characters[index]['ancestry']
    patronus = characters[index]['patronus']
    alive = characters[index]['alive']
    actor = characters[index]['actor']
    value = (name, species, gender, house, date_of_birth, ancestry, patronus, alive, actor)
    values.append(value)
    index += 1
    print(value)
#
# # 4 (მონაცემები ჰარი პოტერის პერსონაჟების შესახებ)
con = sqlite3.connect('harry_potter.sqlite3')
cursor = con.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS harry_potter
(id INTEGER PRIMARY KEY AUTOINCREMENT,
NAME VARCHAR(50),
SPECIES VARCHAR(50),
GENDER VARCHAR(50),
HOUSE VARCHAR(50),
DATE_OF_BIRTH DATE,
ANCESTRY VARCHAR(50),
PATRONUS VARCHAR(50),
ALIVE VARCHAR(50),
ACTOR VARCHAR(50))

''')

cursor.executemany(
    '''INSERT INTO harry_potter
    (NAME, SPECIES, GENDER, HOUSE,DATE_OF_BIRTH, ANCESTRY, PATRONUS, ALIVE, ACTOR)
    values (?,?,?,?,?,?,?,?,?)''',
    values)

con.commit()


# toast notification about holidays
def holiday():
    toast = win10toast.ToastNotifier()
    api_key = '9d88ff3357945c5bf1162ae5d5db6abd213e2d08'
    url = 'https://calendarific.com/api/v2/holidays'
    response = requests.get(f'https://calendarific.com/api/v2/holidays?&api_key={api_key}&country=GE&year=2023')
    # print(response.json())
    result = response.json()
    res = json.dumps(result, indent=4)
    current_date = str(datetime.now().date())
    current_date = str(datetime(2023, 5, 26).date())

    is_holiday = False
    for num in range(len(result['response']['holidays'])):
        date = result['response']['holidays'][num]['date']['iso']
        holiday_name = result['response']['holidays'][num]['name']
        if date == current_date:
            is_holiday = True
            toast.show_toast(title=f"YAAAAAY TODAY YOU CAN REST {current_date} and it is a {holiday_name}", msg=f"{holiday_name}",
                             duration=5)
            print(date, holiday_name)
            break
    if not is_holiday:
        toast.show_toast(title=f"today is {current_date} and it is not a holiday", msg=f"{current_date}", duration=5)

    # print(res)
    # print(type(current_date))


holiday()
