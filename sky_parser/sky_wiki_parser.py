# sky_parser/parser.py

import os
import json
import re
import shutil
import mwparserfromhell
from glob import glob

INPUT_DIR = "sky_wiki_dump"

def clean_text(value):
    if not value:
        return ""
    
    # Parse the wikitext
    code = mwparserfromhell.parse(value)
    
    # Handle specific templates that should extract text
    for template in code.filter_templates():
        if template.name.strip().lower() == "spirit item":
            # Extract the item name (parameter 2, index 1)
            if len(template.params) >= 2:
                item_name = template.get(2).value.strip()
                # Replace the template with just the item name
                code.replace(template, item_name)
        elif template.name.strip().lower() == "emote":
            # Extract the emote name (parameter 2, index 1)
            if len(template.params) >= 2:
                emote_name = template.get(2).value.strip()
                code.replace(template, emote_name)
    
    # Now strip the remaining code and clean up
    return " ".join(code.strip_code().split())

def parse_spirit_items(value):
    items = []
    code = mwparserfromhell.parse(value)
    for template in code.filter_templates():
        if template.name.strip().lower() == "spirit item":
            item = {
                "name": clean_text(template.get(1).value) if len(template.params) > 1 else None,
                "type": clean_text(template.get(2).value) if len(template.params) > 2 else None,
                "link": clean_text(template.get("link").value) if template.has("link") else None,
            }
            items.append(item)
    return items

def extract_infobox_template(wikitext):
    code = mwparserfromhell.parse(wikitext)
    for template in code.filter_templates():
        name = template.name.strip().lower()
        if name in ["guide infobox", "spirit infobox", "skyevent"]:
            return name, template
    return None, None

def parse_gallery(value):
    if "<gallery>" not in value.lower():
        return []

    inside = value.split("<gallery>")[-1].split("</gallery>")[0]
    lines = inside.strip().splitlines()
    images = []
    for line in lines:
        parts = line.split("|", 1)
        filename = clean_text(parts[0])
        caption = clean_text(parts[1]) if len(parts) == 2 else ""
        images.append({"file": filename, "caption": caption})
    return images

def extract_sections(wikitext):
    sections = {}
    # Match exactly two = signs on each side, allowing optional spaces around and after
    # ^\s*==\s*(.*?)\s*==\s*$ ensures:
    #   - line may start/end with spaces
    #   - only 2 equals on each side (not 3 or more)
    pattern = r"^\s*==([^=].*?)==\s*$"

    matches = list(re.finditer(pattern, wikitext, flags=re.MULTILINE))
    if not matches:
        return sections

    for i, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(wikitext)
        content = wikitext[start:end].strip()
        sections[title] = content

    return sections

def parse_memory_section(text):
    # Extract file name and alt text from [[File:...]] links
    file_match = re.search(r'\[\[File:([^|]+)', text)
    file_name = None
    alt_text = None
    
    if file_match:
        file_name = file_match.group(1).strip()
        
        # Extract alt text (the last parameter after the last |)
        # Pattern: [[File:filename|param1|param2|alt_text]]
        alt_match = re.search(r'\[\[File:[^\]]+\|([^|]+)\]\]', text)
        if alt_match:
            alt_text = alt_match.group(1).strip()
    
    # Remove the entire [[File:...]] link from the text before cleaning
    cleaned_text = re.sub(r'\[\[File:[^\]]+\]\]', '', text)
    
    result = {"text": clean_text(cleaned_text)}
    
    if file_name:
        result["file_name"] = file_name
    if alt_text:
        result["alt_text"] = alt_text
    
    return result

def parse_expression_section(text):
    result = {"levels": [], "gallery": [], "costs": []}
    
    # Parse level descriptions
    for line in text.splitlines():
        if line.strip().startswith("*Level"):
            # Try with colon first, then without
            match = re.match(r"\*Level (\d+).*?: (.*)", line.strip())
            if not match:
                match = re.match(r"\*Level (\d+)\s+(.*)", line.strip())
            if match:
                result["levels"].append({
                    "level": int(match.group(1)),
                    "description": match.group(2).strip()
                })
    
    # Parse gallery and map to levels
    gallery_match = re.search(r"<gallery.*?>(.*?)</gallery>", text, re.DOTALL)
    if gallery_match:
        for line in gallery_match.group(1).strip().splitlines():
            if "|" in line:
                file, caption = line.split("|", 1)
                file_clean = clean_text(file)
                caption_clean = clean_text(caption)
                
                # Try to extract level number from caption (e.g., "Level 1", "Level 2")
                level_match = re.search(r'Level (\d+)', caption_clean)
                level = int(level_match.group(1)) if level_match else None
                
                gallery_item = {
                    "file": file_clean,
                    "caption": caption_clean
                }
                if level is not None:
                    gallery_item["level"] = level
                
                result["gallery"].append(gallery_item)
    
    # Parse costs from {{Cost|X C}} format
    cost_matches = re.findall(r'\{\{Cost\|([^}]+)\}\}', text)
    for cost in cost_matches:
        normalized_cost = normalize_price(clean_text(cost))
        if normalized_cost:
            result["costs"].append(normalized_cost)
    
    return result


def parse_cosmetics_section(text):
    cosmetics = {}

    # Match exactly 3 equal signs for subsections (=== ...)
    # Allow variable spacing, e.g. ===Hair=== or === Hair ===
    subsection_pattern = r"^\s*===\s*(.*?)\s*===\s*$"
    matches = list(re.finditer(subsection_pattern, text, flags=re.MULTILINE))

    if not matches:
        return cosmetics

    for i, match in enumerate(matches):
        raw_title = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()

        # --- Handle <span> in title ---
        # Examples:
        #   ===Neck Accessory <span id="Necklace"></span>===
        #   ===<span id="Hairpiece">Hair Accessory</span> ===
        span_match = re.search(r'<span[^>]*id="([^"]+)"[^>]*>(.*?)</span>', raw_title)
        if span_match:
            span_id = span_match.group(1).strip()
            inner_text = span_match.group(2).strip()
            # Use inner text if available, else fallback to outer text
            cosmetic_type = inner_text if inner_text else re.sub(r"<.*?>", "", raw_title).strip()
        else:
            span_id_match = re.search(r'id="([^"]+)"', raw_title)
            span_id = span_id_match.group(1).strip() if span_id_match else None
            cosmetic_type = re.sub(r"<.*?>", "", raw_title).strip()

        # --- Extract description ---
        desc_match = re.split(r"{{#tag:gallery|<gallery|{{Collapse", content, 1, flags=re.IGNORECASE)
        description = desc_match[0].strip() if desc_match else content.strip()

        # --- Extract gallery filenames ---
        gallery_files = []

        for m in re.finditer(r"{{Icon Name\|\|([^|}]+)\|([^}|]+)}}", content):
            base_name = m.group(1).strip()
            variant = m.group(2).strip()
            gallery_files.append(f"{base_name} ({variant})")

        for m in re.finditer(r"{{Icon Name\|\|([^|}]+)\|([^}|]+)}}.*?\|\s*(.*?)$", content, flags=re.MULTILINE):
            base_name = m.group(1).strip()
            variant = m.group(2).strip()
            caption = m.group(3).strip()
            gallery_files.append(f"{base_name} ({variant}) — {caption}")

        # --- Package cosmetic data ---
        item_data = {
            "cosmeticType": cosmetic_type,
            "description": clean_text(description),
        }
        if span_id:
            item_data["id"] = span_id
        if gallery_files:
            item_data["galleryFiles"] = gallery_files

        # --- Extract misc info (like cost, season, etc.) ---
        cost_matches = re.findall(r"{{Cost\|([^}|]+)", content)
        if cost_matches:
            normalized_costs = []
            for cost in cost_matches:
                normalized_cost = normalize_price(clean_text(cost))
                if normalized_cost:
                    normalized_costs.append(normalized_cost)
            if normalized_costs:
                item_data["costs"] = normalized_costs

        cosmetics[cosmetic_type] = item_data

    return cosmetics

def parse_ultimate_gifts_section(text):
    # Reuse cosmetics parser since structure is similar
    return parse_cosmetics_section(text)



def normalize_price(price_str):
    """Normalize price string to structured format"""
    if not price_str:
        return None
    
    # Remove extra whitespace and split
    parts = price_str.strip().split()
    if len(parts) < 2:
        return None
    
    # Handle placeholder values like "?" for unknown prices
    if parts[0] == '?' or parts[0].lower() in ['unknown', 'tbd', 'tba']:
        return {
            "amount": None,
            "currency": "unknown",
            "currency_code": "?",
            "is_placeholder": True
        }
    
    # Try to parse the amount, handle non-numeric values gracefully
    try:
        amount = int(parts[0])
    except ValueError:
        # If we can't parse the amount, return None
        return None
    
    currency = parts[1]
    
    # Map currency types
    currency_map = {
        'H': 'hearts',
        'C': 'candles', 
        'AC': 'ascended_candles',
        'SC': 'seasonal_candles',
        'SH': 'seasonal_hearts',
        'EH': 'event_tickets',
    }
    
    return {
        "amount": amount,
        "currency": currency_map.get(currency, currency),
        "currency_code": currency,
        "is_placeholder": False
    }

def parse_friendship_tree_section(text):
    """Parse friendship tree into structured format with support for multiple trees"""
    result = {
        "trees": [],
        "description": None,
        "raw": text.strip()
    }
    
    # Extract description text that appears before tree templates
    # Look for text before the first {{Friendship Tree or <section begin
    description_match = re.search(r'^(.*?)(?={{Friendship Tree|<section begin)', text, re.DOTALL)
    if description_match:
        description_text = description_match.group(1).strip()
        # Clean up the description text
        if description_text and not description_text.isspace():
            # Remove common wiki markup but keep the content
            cleaned_description = clean_text(description_text)
            if cleaned_description:
                result["description"] = cleaned_description
    
    # Split text into individual tree sections
    tree_sections = []
    
    # Look for different tree types
    tree_patterns = [
        r'<section begin="([^"]*)"[^>]*>(.*?)<section end="[^"]*"',
        r'{{Friendship Tree Info[^}]*}}(.*?)(?={{Friendship Tree Info|$)',
        r'{{Friendship Tree[^}]*}}(.*?)(?={{Friendship Tree|$)'
    ]
    
    # First, try to find section-based trees
    section_matches = re.findall(r'<section begin="([^"]*)"[^>]*>(.*?)<section end="[^"]*"', text, re.DOTALL)
    for section_name, section_content in section_matches:
        if 'Friendship Tree' in section_content:
            tree_sections.append({
                "name": section_name,
                "content": section_content,
                "type": "section"
            })
    
    # If no sections found, look for direct tree templates
    if not tree_sections:
        # Look for Friendship Tree Info blocks
        info_blocks = re.findall(r'{{Friendship Tree Info[^}]*}}(.*?)(?={{Friendship Tree Info|$)', text, re.DOTALL)
        for i, block in enumerate(info_blocks):
            tree_sections.append({
                "name": f"tree_{i+1}",
                "content": block,
                "type": "info_block"
            })
        
        # Look for standalone Friendship Tree templates
        if not tree_sections:
            tree_templates = re.findall(r'{{Friendship Tree[^}]*}}(.*?)(?={{Friendship Tree|$)', text, re.DOTALL)
            for i, template in enumerate(tree_templates):
                tree_sections.append({
                    "name": f"tree_{i+1}",
                    "content": template,
                    "type": "template"
                })
    
    # Parse each tree section
    for tree_section in tree_sections:
        tree_data = parse_single_friendship_tree(tree_section["content"], tree_section["name"])
        if tree_data:
            result["trees"].append(tree_data)
    
    return result

def parse_single_friendship_tree(content, tree_name):
    """Parse a single friendship tree"""
    tree_data = {
        "name": tree_name,
        "nodes": {},
        "levels": {},
        "metadata": {}
    }
    
    # Extract metadata from the tree content
    metadata_patterns = {
        "spirit": r'\|\|spirit\s*=\s*([^\n|]+)',
        "label": r'\|\|label\s*=\s*([^\n|]+)',
        "image": r'\|\|image\s*=\s*([^\n|]+)',
        "season": r'\|\|season\s*=\s*([^\n|]+)',
        "float": r'\|\|float\s*=\s*([^\n|]+)'
    }
    
    for key, pattern in metadata_patterns.items():
        match = re.search(pattern, content)
        if match:
            tree_data["metadata"][key] = match.group(1).strip()
    
    # Extract node information from the template
    node_pattern = r'node([CLR])(\d+)\s*=\s*([^\n|]+)'
    matches = re.findall(node_pattern, content)
    
    for position, level, content_part in matches:
        level_num = int(level)
        content_parts = content_part.strip().split()
        
        # Extract item type and price
        item_type = content_parts[0] if content_parts else None
        price_str = ' '.join(content_parts[1:]) if len(content_parts) > 1 else None
        
        # Create node ID
        node_id = f"node{position}{level_num}"
        
        # Parse price if present
        price = normalize_price(price_str) if price_str else None
        
        # Determine node position
        position_map = {
            'C': 'center',
            'L': 'left', 
            'R': 'right'
        }
        
        node_data = {
            "id": node_id,
            "level": level_num,
            "position": position_map.get(position, position),
            "item_type": item_type,
            "price": price,
            "raw_content": content_part
        }
        
        tree_data["nodes"][node_id] = node_data
        
        # Group by level for easy access
        if level_num not in tree_data["levels"]:
            tree_data["levels"][level_num] = []
        tree_data["levels"][level_num].append(node_id)
    
    # Sort levels
    tree_data["levels"] = dict(sorted(tree_data["levels"].items()))
    
    return tree_data if tree_data["nodes"] else None

def parse_gallery_section(text):
    gallery = []
    blocks = re.findall(r"<gallery[^>]*>(.*?)</gallery>", text, re.DOTALL)
    for block in blocks:
        for line in block.strip().splitlines():
            gallery.append({"file": clean_text(line)})
    return {"images": gallery}

def parse_references_section(_):
    return None

def parse_infobox(template_name, template):
    data = {}
    for param in template.params:
        key = param.name.strip().lower()
        raw_value = param.value.strip()

        # i dont want these values from the infobox
        if key in ["ultimates", "cosmetics", "emote", "props"]:
            continue
        # these need special handling
        elif key == "image" and "<gallery>" in raw_value.lower():
            data["images"] = parse_gallery(raw_value)
        # rest should just be text values
        else:
            data[key] = clean_text(raw_value)
    return data

def extract_summary(raw_text):
    start = raw_text.find('<section begin="Summary"')
    end = raw_text.find('<section end="Summary"')
    if start != -1 and end != -1:
        return clean_text(raw_text[start:end])
    return None

def parse_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        raw_text = f.read()

    infobox_type, infobox = extract_infobox_template(raw_text)
    if not infobox_type or not infobox:
        return None

    entry = parse_infobox(infobox_type, infobox)
    entry["_source_file"] = os.path.basename(filepath)
    entry["_type"] = infobox_type.replace(" infobox", "")
    entry["name"] = os.path.splitext(os.path.basename(filepath))[0]

    summary = extract_summary(raw_text)
    if summary:
        entry["summary"] = summary

    sections_raw = extract_sections(raw_text)
    sections_data = {}

    for title, content in sections_raw.items():
        title_clean = title.strip().lower()
        if title_clean == "memory":
            sections_data["Memory"] = parse_memory_section(content)
        elif title_clean == "expression":
            sections_data["Expression"] = parse_expression_section(content)
        elif title_clean == "cosmetics":
            sections_data["Cosmetics"] = parse_cosmetics_section(content)
        elif title_clean == "ultimate gifts":
            sections_data["Ultimate Gifts"] = parse_ultimate_gifts_section(content)
        elif title_clean == "friendship tree":
            sections_data["Friendship Tree"] = parse_friendship_tree_section(content)
        elif title_clean == "traveling spirit":
            sections_data["Traveling Spirit"] = parse_friendship_tree_section(content)
        elif title_clean == "season friendship tree":
            sections_data["Season Friendship Tree"] = parse_friendship_tree_section(content)
        elif title_clean == "gallery":
            sections_data["Gallery"] = parse_gallery_section(content)
        elif title_clean == "references":
            parsed_refs = parse_references_section(content)
            if parsed_refs is not None:
                sections_data["References"] = parsed_refs

    if sections_data:
        entry["sections"] = sections_data

    return entry

def separate_redirects():
    """
    Separate redirect files from main content files.
    Redirect files are typically one-liners that start with #redirect
    """
    
    redirect_dir = "sky_wiki_dump_redirects"
    main_dir = "sky_wiki_dump_main"
    
    # Create output directories
    os.makedirs(redirect_dir, exist_ok=True)
    os.makedirs(main_dir, exist_ok=True)
    
    redirect_files = []
    main_files = []
    
    # Process all .txt files
    for filepath in glob(os.path.join(INPUT_DIR, "*.txt")):
        filename = os.path.basename(filepath)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # Check if it's a redirect file
            is_redirect = (
                content.startswith('#redirect') or 
                content.startswith('#REDIRECT') or
                content.startswith('#Redirect') or
                len(content.splitlines()) <= 2  # Very short files (1-2 lines)
            )
            
            if is_redirect:
                redirect_files.append(filename)
                # Copy to redirect directory
                shutil.copy2(filepath, os.path.join(redirect_dir, filename))
            else:
                main_files.append(filename)
                # Copy to main directory
                shutil.copy2(filepath, os.path.join(main_dir, filename))
                
        except Exception as e:
            # Copy to main directory as fallback
            shutil.copy2(filepath, os.path.join(main_dir, filename))
            main_files.append(filename)
    
    print(f"Organized files: {len(main_files)} main content, {len(redirect_files)} redirects")
    return main_files, redirect_files

def parse_all_files(organize_files=True):
    global INPUT_DIR
    
    if organize_files:
        # First, separate redirects from main content
        print("Organizing files (separating redirects from main content)...")
        main_files, redirect_files = separate_redirects()
        
        # Update INPUT_DIR to use the main content directory
        INPUT_DIR = "sky_wiki_dump_main"
    else:
        # Use existing organized files
        print("Using existing organized files...")
        INPUT_DIR = "sky_wiki_dump_main"
        
        # Verify the main directory exists and has files
        if not os.path.exists(INPUT_DIR):
            print(f"Error: {INPUT_DIR} directory not found. Run with --organize to organize files first.")
            return [], []
        
        main_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.txt')]
        if not main_files:
            print(f"Error: No .txt files found in {INPUT_DIR}. Run with --organize to organize files first.")
            return [], []
        
        print(f"Found {len(main_files)} files in organized directory")
    
    entries = []
    skipped = []
    for filepath in glob(os.path.join(INPUT_DIR, "*.txt")):
        try:
            # Use safe encoding for printing
            safe_name = os.path.basename(filepath).encode('ascii', 'replace').decode('ascii')
            print(f"Parsing {safe_name}")
            parsed = parse_file(filepath)
            if parsed:
                entries.append(parsed)
                print(f"Parsed {safe_name}")
            else:
                skipped.append(os.path.basename(filepath))
        except Exception as e:
            # Handle any other errors gracefully
            print(f"Error parsing {os.path.basename(filepath)}: {str(e)}")
            skipped.append(os.path.basename(filepath))
    return entries, skipped

def save_to_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
