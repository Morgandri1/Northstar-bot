import json, os

server_data = {}
global DefData
DefData = {"mute_role": -1, "announcement": -1, "Welcome": -1, "pussies": [], "filter": [], "join_role": -1, "join_message": -1, "leave_message": -1, "money": {}, "publicroles":-1, "streamer": -1}  # use <@userid>

def Csave():
    with open(f"configs.json", 'w') as fl:
        json.dump(server_data, fl, indent=2)

def Cload(guild):
    DefData = {"mute_role": -1, "announcement": -1, "Welcome": -1, "pussies": [], "filter": [], "join_role": -1, "join_message": -1, "leave_message": -1, "money": {}, "publicroles":-1, "streamer": -1}  # use <@userid>
    if os.path.exists(f"configs.json"):
        with open(f'configs.json', 'r') as fl:
            loaded = json.load(fl)
            if f"{guild.id}" in loaded:
                DefData = loaded[f"{guild.id}"]
    else:
        with open(f'configs.json', 'w') as fl:
            json.dump(DefData, fl)

    return DefData