# AUTOMATIC MOVIE BATTLES II RCON MODERATOR - PARSER
# CONTACT "devoidjk" ON DISCORD WITH ISSUES, SUGGESTIONS, ETC
# COMPATIBLE WITH BOTH VANILLA MBII AND BULLY'S LOG SCHEMA
# LAST EDITED 6/27/23, v0.1

import re

def parser(timestamp, content):
    timestamp = timestamp.strip()
    
    if re.search(r"^ClientConnect: \((.*)\) ID: ([0-9]{1,2}) \(IP: (.*):([0-9]*)\)$", content):
        client_connect_list = [timestamp, "ClientConnect"]

        client_connect_tuple = re.match(r"^ClientConnect: \((.*)\) ID: ([0-9]{1,2}) \(IP: (.*):([0-9]*)\)$", content).groups()

        for item in client_connect_tuple:
            client_connect_list.append(item)

        print(client_connect_list)

        return client_connect_list

    elif re.search(r"^ClientDisconnect: ([0-9]{1,2})$", content):
        client_disconnect_list = [timestamp, "ClientDisconnect"]

        client_disconnect_tuple = re.match(r"^ClientDisconnect: ([0-9]{1,2})$", content).groups()

        for item in client_disconnect_tuple:
            client_disconnect_list.append(item)

        print(client_disconnect_list)

        return client_disconnect_list

    elif re.search(r"^ClientUserinfoChanged: ([0-9]{1,2}) (.*)$", content):
        client_user_info_changed_list = [timestamp, "ClientUserInfoChanged"]

        client_user_info_changed_tuple = re.match(r"^ClientUserinfoChanged: ([0-9]{1,2}) (.*)$", content).groups()

        for item in client_user_info_changed_tuple:
            client_user_info_changed_list.append(item)

        try:
            client_user_info_changed_name = re.match(r"n\\([^\\]+)\\.*$", client_user_info_changed_list[3]).groups()[0]
            client_user_info_changed_list[3] = client_user_info_changed_name
        except AttributeError:
            pass

        print(client_user_info_changed_list)

        return client_user_info_changed_list

    elif re.search(r"^Player ([0-9]{1,2}) spawned with userinfo: (.*)$", content):
        client_spawned_list = [timestamp, "ClientSpawned"]

        client_spawned_tuple = re.match(r"^Player ([0-9]{1,2}) spawned with userinfo: (.*)$", content).groups()

        for item in client_spawned_tuple:
            client_spawned_list.append(item)

        try:
            client_spawned_team = re.search(r"(?<=\\team\\)(r|b)", client_spawned_list[3]).groups()[0]            
            client_spawned_list.append(client_spawned_team)
        except AttributeError:
            pass

        try:
            client_spawned_name = re.search(r"(?<=\\name\\)([^\\]+)", client_spawned_list[3]).groups()[0]
            client_spawned_list[3] = client_spawned_name
        except AttributeError:
            pass

        print(client_spawned_list)

        return client_spawned_list

    elif re.search(r"^Kill: ([0-9]+) ([0-9]+) ([0-9]+): .*by (.*)$", content):
        kill_list = [timestamp, "Kill"]

        kill_tuple = re.match(r"^Kill: ([0-9]+) ([0-9]+) ([0-9]+): .*by (.*)$", content).groups()

        for item in kill_tuple:
            kill_list.append(item)

        print(kill_list)

        return kill_list
    
    elif re.search(r"^ShutdownGame:", content):
        shutdown_game_list = [timestamp, "ShutdownGame"]

        shutdown_game_tuple = re.match(r"^ShutdownGame:", content).groups()

        for item in shutdown_game_tuple:
            shutdown_game_list.append(item)

        print(shutdown_game_list)

        return shutdown_game_list

    elif re.search(r"^([0-9]{1,2}): (say|sayteam): (.*?)\u0019?: \"(.*)\"$", content):
        say_list = [timestamp, "SayDetailed"]

        say_tuple = re.match(r"^([0-9]{1,2}): (say|sayteam): (.*?)\u0019?: \"(.*)\"$", content).groups()

        for item in say_tuple:
            say_list.append(item)

        print(say_list)

        return say_list

    elif re.search(r"^(say|sayteam): (.*?)\u0019?: (.*)$", content):
        say_list = [timestamp, "Say"]

        say_tuple = re.match(r"^(say|sayteam): (.*?)\u0019?: (.*)$", content).groups()

        for item in say_tuple:
            say_list.append(item)

        print(say_list)

        return say_list
    
    else:
        return [0, "Null"]
