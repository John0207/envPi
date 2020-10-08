# Python program to read 
# json file 
import json

# Opening JSON file 
f = open('data.json', )

# returns JSON object as  
# a dictionary 
data = json.load(f)

# Iterating through the json 
# list
temp_from_json = []
humid_from_json = []
for i in data:
    temp_from_json.append(i[0])
    humid_from_json.append(i[1])

# Closing file
f.close()
