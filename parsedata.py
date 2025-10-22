import os
import json
import mwparserfromhell
from glob import glob

INPUT_DIR = "sky_wiki_dump"
OUTPUT_FILE = "parsed_guides.json"

def clean_text(value):
    """Remove MediaWiki markup like [[...]], {{...}}, excessive whitespace, etc."""
    if not value:
        return ""
    text = str(value)
    text = text.replace("[[", "").replace("]]", "")
    text = text.replace("{{", "").replace("}}", "")
    text = text.replace("\n", " ").strip()
    return text

def parse_spirit_items(value):
    """Extract list of spirit items from nested templates like {{Spirit Item|...}}"""
    items = []
    code = mwparserfromhell.parse(value)
    for template in code.filter_templates():
        if template.name.strip().lower() == "spirit item":
            item_data = {
                "name": clean_text(template.get(1).value) if len(template.params) > 1 else None,
                "type": clean_text(template.get(2).value) if len(template.params) > 2 else None,
                "link": clean_text(template.get("link").value) if template.has("link") else None,
                # "source": template
            }
            items.append(item_data)
    return items

def parse_infobox(wikitext):
    """Parses a Guide Infobox and returns a dict of values"""
    code = mwparserfromhell.parse(wikitext)
    templates = code.filter_templates()
    infobox = next((t for t in templates if "guide infobox" in t.name.lower()), None)

    if not infobox:
        return {}

    result = {}
    for param in infobox.params:
        key = param.name.strip().lower()
        raw_value = param.value.strip()

        if key in ["ultimates", "cosmetics"]:
            result[key] = parse_spirit_items(raw_value)
        else:
            result[key] = clean_text(raw_value)

    return result

def parse_all_files():
    parsed_entries = []

    for filepath in glob(os.path.join(INPUT_DIR, "*.txt")):
        with open(filepath, "r", encoding="utf-8") as f:
            raw_text = f.read()

        infobox_data = parse_infobox(raw_text)

        if infobox_data:
            infobox_data["_source_file"] = os.path.basename(filepath)
            parsed_entries.append(infobox_data)

    return parsed_entries

def save_to_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    all_data = parse_all_files()
    print(f"Parsed {len(all_data)} infoboxes.")
    save_to_json(all_data, OUTPUT_FILE)
    print(f"Saved output to {OUTPUT_FILE}")
