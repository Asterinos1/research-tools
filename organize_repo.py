import os
from pathlib import Path

def setup_notebook_files(target_dir):
    root_path = Path(target_dir).resolve()
    root_name = root_path.name
    tree_file = root_path / f"{root_name}_directory_tree.txt"
    
    # 1. Create Directory Tree
    tree_lines = [f"Directory Tree for: {root_name}\n", "="*30 + "\n"]
    
    # Walk for tree generation and renaming
    for root, dirs, files in os.walk(root_path, topdown=False):
        level = root.replace(str(root_path), '').count(os.sep)
        indent = ' ' * 4 * level
        tree_lines.append(f"{indent}{os.path.basename(root)}/\n")
        
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            # Skip the tree file itself if it exists
            if f == tree_file.name:
                continue
                
            tree_lines.append(f"{sub_indent}{f}\n")
            
            # 2. Rename Files: original_name -> ROOT_NAME_original_name
            # We check if already prefixed to avoid double-renaming
            if not f.startswith(f"{root_name}_"):
                old_file = Path(root) / f
                new_name = f"{root_name}_{f}"
                new_file = Path(root) / new_name
                
                try:
                    old_file.rename(new_file)
                except OSError as e:
                    print(f"Error renaming {f}: {e}")

    # Write the tree to a file
    with open(tree_file, "w", encoding="utf-8") as tf:
        tf.writelines(tree_lines)
    
    print(f"Success. Tree generated: {tree_file.name}")
    print(f"Files in '{root_name}' have been prefixed.")

if __name__ == "__main__":
    # Input the folder path here
    folder_to_process = input("Enter the path to the repository folder: ").strip()
    if os.path.isdir(folder_to_process):
        setup_notebook_files(folder_to_process)
    else:
        print("Invalid directory path.")