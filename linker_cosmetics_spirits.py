import json

# Load previously exported JSON files
with open("lua_parse/cosmetics.json", "r", encoding="utf-8") as f:
    cosmetics = json.load(f)

with open("lua_parse/spirits.json", "r", encoding="utf-8") as f:
    spirits = json.load(f)

# --- Build helper maps ---
# Map spirit name → spirit object
spirit_name_map = {
    v["name"]: v
    for k, v in spirits.items()
    if not k.startswith("basic_") and "name" in v
}

# Map spirit string_id → numeric id, skip keys starting with "basic_"
spirit_id_map = {
    v["string_id"]: v["id"]
    for k, v in spirits.items()
    if not k.startswith("basic_") and "string_id" in v and "id" in v
}

# Initialize empty list of cosmetics in each spirit
for spirit in spirits.values():
    spirit["cosmetics"] = []

# --- Link cosmetics to spirits ---
for cosmetic_key, cosmetic in cosmetics.items():
    spirit_name = cosmetic.get("spirit")
    if not spirit_name:
        continue  # cosmetic has no associated spirit

    # Try matching by name first
    spirit_obj = spirit_name_map.get(spirit_name)

    # If not found, try matching by converting to string_id format (e.g. "Tiptoeing Tea Brewer" → "tiptoeing_tea_brewer")
    if not spirit_obj:
        possible_id = spirit_name.lower().replace(" ", "_").replace("-", "_")
        for s in spirits.values():
            if s.get("string_id") == possible_id:
                spirit_obj = s
                break

    if not spirit_obj:
        print(f"Warning: Cosmetic '{cosmetic_key}' references unknown spirit '{spirit_name}'")
        continue

    # Add spirit id to cosmetic
    cosmetic["spirit_id"] = spirit_obj["id"]

    # Add cosmetic id to spirit
    spirit_obj["cosmetics"].append(cosmetic["id"])

# --- Save back to JSON ---
with open("lua_parse/cosmetics_linked.json", "w", encoding="utf-8") as f:
    json.dump(cosmetics, f, indent=4, ensure_ascii=False)

with open("lua_parse/spirits_linked.json", "w", encoding="utf-8") as f:
    json.dump(spirits, f, indent=4, ensure_ascii=False)
