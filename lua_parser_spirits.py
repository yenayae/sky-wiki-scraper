import luadata
import json
import re


id_counter = 1

def add_spirits_metadata(data_dict, start_id = 1) :
    global id_counter
    id_counter = start_id

    """Tag spirits with type and unique IDs."""
    for key, item in data_dict.items():

        item["string_id"] = key

        # Assign unique ID
        item["id"] = id_counter
        id_counter += 1

    return data_dict


spirits_data = luadata.read("sky_wiki_module_data/spirit_data.lua", encoding="utf-8")

spirits_data = add_spirits_metadata(spirits_data)

with open ("lua_parse/spirits.json", "w", encoding="utf-8") as f:
    json.dump(spirits_data, f, indent=4, ensure_ascii=False)