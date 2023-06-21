import json

f = open('email_address.json')
json_data = json.load(f)
ar = ['duy', 'lam', 'nam']
for x in json_data:
    # print(json_data[x]['name'])
    if json_data[x]['name'] in ar:
        print(json_data[x]['name'])

# for y in ar:
#     print(y)