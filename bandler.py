import os
import json
from pathlib import Path

def bundle_for_notebook(target_dir):
    root_path = Path(target_dir).resolve()
    root_name = root_path.name
    output_bundle = root_path.parent / f"{root_name}_MASTER_SOURCE.txt"
    
    valid_exts = {'.py', '.sh', '.c', '.cpp', '.h', '.hpp', '.cu', '.txt', '.md'}
    all_content = [
        f"--- REPOSITORY OVERVIEW ---\n",
        f"Project Name: {root_name}\n",
        f"Generated on: 2026-02-14\n",
        f"Purpose: Integrated Source for AI Analysis\n",
        "==========================================\n\n"
    ]
    
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for f in files:
            file_path = Path(root) / f
            ext = file_path.suffix.lower()
            rel_path = file_path.relative_to(root_path)

            # NOTEBOOKLM FRIENDLY DELIMITER
            header = f"\n\n[FILE_START: {rel_path}]\n" + "="*40 + "\n"
            footer = f"\n[FILE_END: {rel_path}]\n" + "="*40 + "\n"

            if ext in valid_exts:
                all_content.append(header)
                try:
                    with open(file_path, 'r', encoding='utf-8') as code_file:
                        all_content.append(code_file.read())
                except Exception as e:
                    all_content.append(f"ERROR READING FILE: {e}")
                all_content.append(footer)

            elif ext == '.ipynb':
                all_content.append(header + "(Jupyter Notebook Content)\n")
                try:
                    with open(file_path, 'r', encoding='utf-8') as jf:
                        data = json.load(jf)
                        for cell in data.get('cells', []):
                            ctype = cell.get('cell_type', 'unknown')
                            src = "".join(cell.get('source', []))
                            all_content.append(f"\n--- {ctype.upper()} CELL ---\n{src}\n")
                except Exception as e:
                    all_content.append(f"ERROR PARSING NOTEBOOK: {e}")
                all_content.append(footer)

    with open(output_bundle, "w", encoding="utf-8") as out:
        out.writelines(all_content)
    print(f"NotebookLM-ready bundle created: {output_bundle.name}")

if __name__ == "__main__":
    path = input("Enter repo folder path: ").strip().strip('"') # Strip quotes for Windows paths
    bundle_for_notebook(path)