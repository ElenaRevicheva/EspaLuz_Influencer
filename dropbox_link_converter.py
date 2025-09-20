#!/usr/bin/env python3
"""
Dropbox Link Converter
Converts Dropbox sharing links to direct download links for YouTube uploads
"""

import re
from urllib.parse import urlparse, parse_qs

def convert_dropbox_link(original_link):
    """
    Convert a Dropbox sharing link to a direct download link
    
    Args:
        original_link (str): The original Dropbox sharing link
        
    Returns:
        str: The direct download link
    """
    # Parse the URL
    parsed = urlparse(original_link)
    
    # Check if it's a valid Dropbox link
    if 'dropbox.com' not in parsed.netloc:
        raise ValueError("This doesn't appear to be a Dropbox link")
    
    # Extract the path (everything after the domain)
    path = parsed.path
    
    # For the new Dropbox sharing format (scl/fi/...)
    if '/scl/fi/' in path:
        # Extract the file path and name
        # Pattern: /scl/fi/{hash}/{filename}
        match = re.search(r'/scl/fi/([^/]+)/([^/?]+)', original_link)
        if match:
            hash_part = match.group(1)
            filename = match.group(2)
            
            # Create the direct download link
            direct_link = f"https://dl.dropboxusercontent.com/scl/fi/{hash_part}/{filename}"
            return direct_link
    
    # For older Dropbox format (s/...)
    elif '/s/' in path:
        # Extract the file path
        match = re.search(r'/s/([^/]+)/([^/?]+)', original_link)
        if match:
            hash_part = match.group(1)
            filename = match.group(2)
            
            # Create the direct download link
            direct_link = f"https://dl.dropboxusercontent.com/s/{hash_part}/{filename}"
            return direct_link
    
    raise ValueError("Unable to parse this Dropbox link format")

def main():
    """Main function to demonstrate the conversion"""
    
    # Example link from the user
    original_link = "https://www.dropbox.com/scl/fi/uy5uv35wicmtbcr667p9u/202509151508.mp4?rlkey=om1n84rnwnpkobgvcm31d7xhd&st=me8k5b4i&dl=0"
    
    print("Dropbox Link Converter")
    print("=" * 50)
    print(f"Original link:")
    print(f"{original_link}")
    print()
    
    try:
        direct_link = convert_dropbox_link(original_link)
        print(f"Direct download link:")
        print(f"{direct_link}")
        print()
        print("✅ Conversion successful!")
        print()
        print("How to use this link:")
        print("1. Copy the direct download link above")
        print("2. Use it in your Make scenario for YouTube upload")
        print("3. YouTube will be able to access the file directly")
        
    except ValueError as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()