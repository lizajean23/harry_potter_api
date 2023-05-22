import requests
import sqlite3
import json

# 1
character = requests.get('https://hp-api.onrender.com/api/characters')
print(character.headers)
print(character.text)
print(character.content)

# 2
characters = character.json()
with open('harry_potter.json', 'w') as file:
    json.dump(characters, file, indent=4)

# 3
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

# 4 (მონაცემები ჰარი პოტერის პერსონაჟების შესახებ)
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
