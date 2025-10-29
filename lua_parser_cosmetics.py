import luadata
import json
import re
import uuid

# Currency map
currency_map = {
    'H': 'hearts',
    'C': 'candles',
    'AC': 'ascended_candles',
    'SC': 'seasonal_candles',
    'SH': 'seasonal_hearts',
    'EH': 'event_tickets',
    'SP': 'season_pass'
}

def parse_price(price_str):
    """Normalize and parse price strings into structured info."""
    if not price_str or price_str.strip() == "":
        return {"raw": "", "type": "undefined"}

    price_str = price_str.strip()

    if price_str.lower() == "free":
        return {"raw": price_str, "type": "free"}

    if price_str.upper() in ["N/A", "?"]:
        return {"raw": price_str, "type": "unavailable"}

    if price_str.startswith("$"):
        try:
            return {"raw": price_str, "type": "real_money", "amount_usd": float(price_str[1:])}
        except ValueError:
            return {"raw": price_str, "type": "real_money", "amount_usd": None}

    match = re.match(r'(\d+)\s*([A-Z]+)', price_str)
    if match:
        amount, code = match.groups()
        currency = currency_map.get(code, code)
        return {
            "raw": price_str,
            "type": "currency",
            "amount": int(amount),
            "currency": currency
        }

    return {"raw": price_str, "type": "unknown"}

id_counter = 1

def add_cosmetic_metadata(data_dict, source_type, start_id=1):

    global id_counter
    id_counter = start_id

    """Tag cosmetics with type, price, and unique IDs."""
    for key, item in data_dict.items():
        # Determine cosmetic_type
        if source_type == "regular":
            item["cosmetic_type"] = "basic" if key.startswith("basic_") else "regular"
        else:
            item["cosmetic_type"] = source_type

        # Parse price
        if "price" in item:
            item["price"] = parse_price(item["price"])

        # Assign deterministic ID based on type + key
        item["item_id"] = key
        item["id"] = id_counter
        id_counter += 1
    return data_dict


# --- Load Lua tables ---
cosmetics_data = luadata.read("sky_wiki_module_data/cosmetics_data.lua", encoding="utf-8")
season_cosmetics_data = luadata.read("sky_wiki_module_data/season_cosmetics_data.lua", encoding="utf-8")
days_cosmetics_data = luadata.read("sky_wiki_module_data/days_item_data.lua", encoding="utf-8")

# --- Process and tag all ---
cosmetics_data = add_cosmetic_metadata(cosmetics_data, "regular")
season_cosmetics_data = add_cosmetic_metadata(season_cosmetics_data, "season")
days_cosmetics_data = add_cosmetic_metadata(days_cosmetics_data, "days")

# --- Combine into one dictionary ---
all_cosmetics = {**cosmetics_data, **season_cosmetics_data, **days_cosmetics_data}

# --- Write to JSON ---
with open("lua_parse/cosmetics.json", "w", encoding="utf-8") as f:
    json.dump(all_cosmetics, f, ensure_ascii=False, indent=4)
