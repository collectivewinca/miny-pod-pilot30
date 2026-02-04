#!/usr/bin/env python3
"""
Script to fix the ECONOMICS slide in all HTML deck files.
Fixes the heading font size and adds responsive classes for mobile/desktop.
"""

import os
import re
from pathlib import Path

def fix_economics_slide(file_path):
    """Fix the ECONOMICS slide in a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if the file already has the revenue-section class
        if 'revenue-section' in content:
            print(f"  Skipping {file_path.name} - already fixed")
            return False
        
        # Pattern to find the ECONOMICS slide section
        # Look for the slide containing "TURN.*LISTENERS INTO REVENUE"
        pattern = r'(<!-- SLIDE 7: ECONOMICS -->\s*<section class="slide">\s*<div class="slide-content">\s*<h2 class="reveal">)(TURN.*LISTENERS INTO REVENUE)(</h2>\s*<div class="grid-2" style="align-items: flex-start;">)'
        
        # Replace the heading with responsive font size
        new_content = re.sub(
            pattern,
            r'\1\2\3',
            content,
            flags=re.DOTALL
        )
        
        # Now fix the heading specifically with responsive font size
        heading_pattern = r'(<h2 class="reveal">)(TURN.*LISTENERS INTO REVENUE)(</h2>)'
        new_content = re.sub(
            heading_pattern,
            r'<h2 class="reveal" style="font-size: clamp(2rem, 4vw, 3.5rem); line-height: 1.2;">\2</h2>',
            new_content,
            flags=re.DOTALL
        )
        
        # Add revenue-section class to the slide
        new_content = new_content.replace(
            '<!-- SLIDE 7: ECONOMICS -->\n        <section class="slide">',
            '<!-- SLIDE 7: ECONOMICS -->\n        <section class="slide revenue-section">'
        )
        
        # Fix the revenue share box with responsive styles
        revenue_box_pattern = r'(<div class="reveal delay-2" style="text-align: center; border: 1px solid var\(--accent\); padding: 3rem; border-radius: 20px;">)'
        revenue_box_replacement = r'<div class="reveal delay-2 revenue-share-box" style="text-align: center; border: 1px solid var(--accent); padding: clamp(1.5rem, 3vw, 3rem); border-radius: 20px;">'
        new_content = re.sub(revenue_box_pattern, revenue_box_replacement, new_content)
        
        # Fix the h1 font size with clamp
        h1_pattern = r'(<h1 class="accent-text" style="font-size: 5rem; margin: 0;">)'
        h1_replacement = r'<h1 class="accent-text" style="font-size: clamp(2.5rem, 5vw, 5rem); margin: 0; line-height: 1.2;">'
        new_content = re.sub(h1_pattern, h1_replacement, new_content)
        
        # Fix the paragraph with responsive font size
        p_pattern = r'(<p>)(✓ \$0 Onboarding\s*\|\s*✓ \$0 Production\s*\|\s*✓ 75% Share)(</p>)'
        p_replacement = r'<p style="font-size: clamp(0.9rem, 1.5vw, 1.1rem); margin-top: 1rem;">\2</p>'
        new_content = re.sub(p_pattern, p_replacement, new_content, flags=re.DOTALL)
        
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
    
    # Skip the already fixed file
    html_files = [f for f in html_files if f.name != "ancient-history-fangirl.html"]
    
    print(f"Will process {len(html_files)} files (excluding ancient-history-fangirl.html)")
    
    fixed_count = 0
    for html_file in html_files:
        print(f"\nProcessing {html_file.name}...")
        if fix_economics_slide(html_file):
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files out of {len(html_files)}")

if __name__ == "__main__":
    main()