#!/usr/bin/env python
"""
Manual translation compiler - Use this if gettext tools are not installed
"""
import struct
import array
from pathlib import Path

def generate_mo_file(po_file, mo_file):
    """Compile .po file to .mo file manually"""
    
    # Read .po file with UTF-8 encoding
    with open(po_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    # Parse translations
    translations = {}
    msgid = None
    msgstr = None
    
    for line in lines:
        line = line.strip()
        if line.startswith('msgid "'):
            msgid = line[7:-1]
        elif line.startswith('msgstr "'):
            msgstr = line[8:-1]
            if msgid and msgstr:
                translations[msgid] = msgstr
                msgid = None
                msgstr = None
    
    # Remove empty translation
    if '' in translations:
        del translations['']
    
    # Build .mo file
    keys = sorted(translations.keys())
    offsets = []
    ids = b''
    strs = b''
    
    for key in keys:
        offsets.append((len(ids), len(key), len(strs), len(translations[key])))
        ids += key.encode('utf-8') + b'\x00'
        strs += translations[key].encode('utf-8') + b'\x00'
    
    # MO file format
    keystart = 7 * 4 + 16 * len(keys)
    valuestart = keystart + len(ids)
    
    # Build key index
    koffsets = []
    voffsets = []
    for o1, l1, o2, l2 in offsets:
        koffsets += [l1, o1 + keystart]
        voffsets += [l2, o2 + valuestart]
    
    offsets = koffsets + voffsets
    
    # Write .mo file
    with open(mo_file, 'wb') as f:
        # Magic number
        f.write(struct.pack('Iiiiiii',
            0x950412de,           # Magic
            0,                    # Version
            len(keys),            # Number of entries
            7 * 4,                # Start of key index
            7 * 4 + len(keys) * 8,  # Start of value index
            0, 0))                # Size and offset of hash table
        
        # Write offsets
        f.write(array.array("i", offsets).tobytes())
        
        # Write keys and values
        f.write(ids)
        f.write(strs)
    
    print(f"[OK] Compiled: {po_file} -> {mo_file}")

if __name__ == '__main__':
    # Compile all .po files
    locale_dir = Path('locale')
    
    if not locale_dir.exists():
        print("[ERROR] locale directory not found!")
        exit(1)
    
    compiled = 0
    for po_file in locale_dir.rglob('*.po'):
        mo_file = po_file.with_suffix('.mo')
        try:
            generate_mo_file(po_file, mo_file)
            compiled += 1
        except Exception as e:
            print(f"[ERROR] Error compiling {po_file}: {e}")
    
    if compiled > 0:
        print(f"\n[SUCCESS] Compiled {compiled} translation file(s)!")
        print("\nNow restart your Django server and test language switching.")
    else:
        print("\n[ERROR] No .po files found to compile.")
