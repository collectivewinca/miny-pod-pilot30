import os
import re

def rename_images():
    deck_dir = "public/decks"
    
    if not os.path.exists(deck_dir):
        print(f"Directory {deck_dir} does not exist!")
        return
    
    files = os.listdir(deck_dir)
    
    for filename in files:
        if filename.endswith('.jpg'):
            # Replace all hyphens with underscores in the filename
            new_name = filename.replace('-', '_')
            
            # Only rename if the name actually changes
            if new_name != filename:
                old_path = os.path.join(deck_dir, filename)
                new_path = os.path.join(deck_dir, new_name)
                
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed: {filename} -> {new_name}")
                except Exception as e:
                    print(f"Error renaming {filename}: {e}")
    
    print("\nRenaming complete!")

if __name__ == "__main__":
    rename_images()