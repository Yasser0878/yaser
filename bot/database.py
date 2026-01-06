import json

FILE = "groups.json"

def load():
    try:
        return json.load(open(FILE))
    except:
        return []

def save(data):
    json.dump(data, open(FILE, "w"))

def activate(group_id):
    data = load()
    if group_id not in data:
        data.append(group_id)
        save(data)

def active(group_id):
    return group_id in load()
