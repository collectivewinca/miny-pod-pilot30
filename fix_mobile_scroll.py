#!/usr/bin/env python3
"""
Script to fix mobile scroll behavior in all HTML deck files.
Disables slide effect (scroll-snap and smooth scrolling) on mobile devices.
"""

import os
import re
from pathlib import Path

def fix_mobile_scroll(file_path):
    """Fix mobile scroll behavior in a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if the file already has mobile scroll fixes
        if 'scroll-behavior: auto' in content and 'scroll-snap-type: none' in content:
            print(f"  Skipping {file_path.name} - already fixed")
            return False
        
        # Pattern to find the mobile media query section
        # Look for the @media (max-width: 768px) block
        mobile_media_pattern = r'(@media\s*\(max-width:\s*768px\)\s*\{)(.*?)(\})'
        
        # Check if mobile media query exists
        mobile_match = re.search(mobile_media_pattern, content, re.DOTALL)
        
        if mobile_match:
            # Mobile media query exists, add scroll fixes to it
            media_start = mobile_match.start(1)
            media_content = mobile_match.group(2)
            media_end = mobile_match.end(3)
            
            # Check if scroll fixes already exist in this media query
            if 'scroll-behavior: auto' in media_content and 'scroll-snap-type: none' in media_content:
                print(f"  Skipping {file_path.name} - already has scroll fixes in mobile media query")
                return False
            
            # Add scroll fixes to the beginning of the mobile media query
            scroll_fixes = """    /* Disable slide effect on mobile */
    .slides-container {
        scroll-behavior: auto;
        scroll-snap-type: none;
    }
    
    .slide {
        scroll-snap-align: none;
    }
    
"""
            
            # Insert scroll fixes after the opening brace
            new_media_content = scroll_fixes + media_content
            new_content = content[:media_start] + mobile_match.group(1) + new_media_content + mobile_match.group(3) + content[media_end:]
            
        else:
            # Mobile media query doesn't exist, need to create it
            # First, find where to insert it (usually after the main CSS rules)
            
            # Look for the closing style tag or end of CSS section
            style_end_pattern = r'(\s*</style>)'
            style_end_match = re.search(style_end_pattern, content)
            
            if not style_end_match:
                print(f"  Warning: Could not find </style> tag in {file_path.name}")
                return False
            
            # Insert mobile media query before the closing style tag
            insert_position = style_end_match.start(1)
            
            mobile_css = """
/* Mobile */
@media (max-width: 768px) {
    /* Disable slide effect on mobile */
    .slides-container {
        scroll-behavior: auto;
        scroll-snap-type: none;
    }
    
    .slide {
        scroll-snap-align: none;
    }
}
"""
            
            new_content = content[:insert_position] + mobile_css + content[insert_position:]
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  Fixed {file_path.name}")
            return True
        else:
            print(f"  No changes needed for {file_path.name}")
            return False
            
    except Exception as e:
        print(f"  Error processing {file_path.name}: {e}")
        return False

def main():
    """Main function to fix all HTML files."""
    decks_dir = Path("public/decks")
    
    if not decks_dir.exists():
        print(f"Error: Directory {decks_dir} does not exist")
        return
    
    html_files = list(decks_dir.glob("*.html"))
    print(f"Found {len(html_files)} HTML files in {decks_dir}")
    
    fixed_count = 0
    for html_file in html_files:
        print(f"\nProcessing {html_file.name}...")
        if fix_mobile_scroll(html_file):
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files out of {len(html_files)}")

if __name__ == "__main__":
    main()