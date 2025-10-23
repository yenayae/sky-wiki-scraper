# sky_parser/main.py

import os
import argparse
from sky_parser.sky_wiki_parser import parse_file, parse_all_files, save_to_json

OUTPUT_FILE = "parsed_entries.json"
SKIPPED_FILE = "skipped_files.json"

def main():
    parser = argparse.ArgumentParser(description="Sky Spirit Parser")
    parser.add_argument("--file", type=str, help="Parse a single file (e.g. 'sky_wiki_dump/SpiritName.txt')")
    parser.add_argument("--organize", action="store_true", help="Force organization of files (separate redirects from main content)")
    parser.add_argument("--no-organize", action="store_true", help="Skip organization and parse existing organized files")
    args = parser.parse_args()

    if args.file:
        print(f"Parsing single file: {args.file}")
        result = parse_file(args.file)
        if result:
            output_path = f"{os.path.splitext(os.path.basename(args.file))[0]}_parsed.json"
            save_to_json(result, output_path)
            print(f"Saved to {output_path}")
        else:
            print("Could not parse the file or missing infobox.")
    else:
        print("Parsing all files...")
        
        # Determine organization behavior
        if args.organize:
            print("Forcing organization of files (separate redirects from main content)")
            organize_files = True
        elif args.no_organize:
            print("Skipping organization, using existing organized files")
            organize_files = False
        else:
            # Auto-detect: organize if main directory doesn't exist or is empty
            if not os.path.exists("sky_wiki_dump_main") or len(os.listdir("sky_wiki_dump_main")) == 0:
                print("No organized files found, organizing files (separate redirects from main content)")
                organize_files = True
            else:
                print("Found existing organized files, skipping organization")
                organize_files = False
        
        all_data, skipped = parse_all_files(organize_files=organize_files)
        save_to_json(all_data, OUTPUT_FILE)
        save_to_json(skipped, SKIPPED_FILE)
        print(f"Parsed {len(all_data)} files, skipped {len(skipped)} files")
        print(f"Results saved to {OUTPUT_FILE}")
        print(f"Skipped files saved to {SKIPPED_FILE}")
        if organize_files:
            print(f"Organized files:")
            print(f"  - Main content: sky_wiki_dump_main/")
            print(f"  - Redirects: sky_wiki_dump_redirects/")

if __name__ == "__main__":
    main()
