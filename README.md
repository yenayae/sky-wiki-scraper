# Commands

```python
# Auto-detect (recommended for most use cases)
python main.py

# Force organization (useful when you want to re-organize)
python main.py --organize

# Skip organization (faster when files are already organized)
python main.py --no-organize

# Parse single file (unchanged)
python main.py --file sky_wiki_dump/SpiritName.txt
```

```python
# When you fetch a new wiki dump:
python main.py --organize  # Organize the new files
# OR just:
python main.py            # Auto-detects and organizes

# For subsequent parsing (much faster):
python main.py --no-organize  # Skip organization
# OR just:
python main.py               # Auto-detects and skips
```
