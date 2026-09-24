#!/usr/bin/env python3
import os
import sys
import io
import json
import re
import fnmatch
import tokenize
import argparse
from pathlib import Path

DEFAULT_EXCLUDES = {
    '.git', '.svn', '.hg', '.idea', '.vscode', '__pycache__', 
    '.pytest_cache', '.mypy_cache', '.ruff_cache', '.tox',
    'venv', '.venv', 'node_modules', 'dist', 'build',
    'external', 'test', 'tests', 'docs', 'cmake', 'bindings', 
    'bin', 'obj'
}

DEFAULT_EXTS = {
    '.py', '.ipynb', '.js', '.ts', '.jsx', '.tsx',
    '.c', '.cpp', '.h', '.hpp', '.cc', '.cxx',
    '.cs', '.rs', '.go', '.kt', '.swift', '.scala', '.java',
    '.html', '.css', '.scss', '.sass',
    '.sh', '.bash', '.zsh', '.ps1',
    '.sql', '.r', '.jl', '.lua', '.zig',
    '.tex', '.bib', '.sty', '.cls',
    '.yaml', '.yml', '.toml', '.json', '.proto',
    '.xaml', '.csproj'
}

LANG_MAP = {
    'ipynb': 'python',
    'txt': 'text',
    'cs': 'csharp',
    'rs': 'rust',
    'go': 'go',
    'kt': 'kotlin',
    'swift': 'swift',
    'java': 'java',
    'scala': 'scala',
    'py': 'python',
    'js': 'javascript',
    'ts': 'typescript',
    'jsx': 'javascript',
    'tsx': 'typescript',
    'c': 'c',
    'cpp': 'cpp',
    'h': 'c',
    'hpp': 'cpp',
    'cc': 'cpp',
    'cxx': 'cpp',
    'lua': 'lua',
    'zig': 'zig',
    'r': 'r',
    'jl': 'julia',
    'sql': 'sql',
    'sh': 'bash',
    'bash': 'bash',
    'zsh': 'bash',
    'ps1': 'powershell',
    'tex': 'latex',
    'bib': 'bibtex',
    'sty': 'latex',
    'cls': 'latex',
    'yaml': 'yaml',
    'yml': 'yaml',
    'toml': 'toml',
    'json': 'json',
    'proto': 'protobuf',
    'html': 'html',
    'css': 'css',
    'scss': 'scss',
    'sass': 'sass',
    'xml': 'xml',
    'xaml': 'xml',
    'csproj': 'xml',
    'md': 'markdown'
}

def load_gitignore_rules(root_path: Path) -> list[str]:
    """Parse .gitignore rules if present in the target directory root."""
    gitignore_file = root_path / ".gitignore"
    if not gitignore_file.is_file():
        return []
    rules = []
    try:
        with open(gitignore_file, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    rules.append(line)
    except Exception:
        pass
    return rules

def is_path_ignored(rel_path: Path, gitignore_rules: list[str], is_dir: bool = False) -> bool:
    """Check if a relative path matches any parsed .gitignore pattern."""
    rel_posix = rel_path.as_posix()
    name = rel_path.name
    for rule in gitignore_rules:
        rule_clean = rule.strip("/")
        if rule.endswith("/") and not is_dir:
            continue
        if fnmatch.fnmatch(name, rule_clean):
            return True
        if fnmatch.fnmatch(rel_posix, rule_clean) or fnmatch.fnmatch(rel_posix, f"*/{rule_clean}*") or fnmatch.fnmatch(rel_posix, f"{rule_clean}/*"):
            return True
    return False

def is_binary_file(file_path: Path) -> bool:
    """Detect if a file contains null bytes within its first 1024 bytes."""
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(1024)
            return b"\x00" in chunk
    except Exception:
        return False

def collapse_blank_lines(text: str, max_consecutive: int = 1) -> str:
    """Strip trailing line whitespace, collapse consecutive blank lines, and strip edges."""
    lines = [line.rstrip() for line in text.splitlines()]
    result = []
    blank_count = 0
    for line in lines:
        if line == "":
            blank_count += 1
            if blank_count <= max_consecutive:
                result.append(line)
        else:
            blank_count = 0
            result.append(line)
    return "\n".join(result).strip()

def strip_python_code(source: str, strip_comments: bool = True, include_docstrings: bool = True) -> str:
    """Safely strip comments and docstrings using Python's tokenize module."""
    if not strip_comments and include_docstrings:
        return source
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        filtered = []
        prev_type = tokenize.INDENT
        for tok in tokens:
            ttype, tval, start, end, line = tok
            if strip_comments and ttype == tokenize.COMMENT:
                continue
            if not include_docstrings and ttype == tokenize.STRING:
                if prev_type in (tokenize.INDENT, tokenize.NEWLINE, tokenize.NL, tokenize.ENCODING):
                    continue
            filtered.append((ttype, tval))
            if ttype not in (tokenize.NL, tokenize.COMMENT):
                prev_type = ttype
        return tokenize.untokenize(filtered)
    except Exception:
        return source

def strip_code(text: str, suffix: str, strip_comments: bool = True, include_docstrings: bool = True) -> str:
    """Strips comments without damaging string literals across supported languages and cleans blank lines."""
    if suffix == '.py':
        if strip_comments or not include_docstrings:
            text = strip_python_code(text, strip_comments=strip_comments, include_docstrings=include_docstrings)
    elif strip_comments:
        if suffix in {
            '.c', '.cpp', '.h', '.hpp', '.cc', '.cxx', '.cs', '.rs', '.go', 
            '.kt', '.swift', '.scala', '.java', '.js', '.ts', '.jsx', '.tsx', 
            '.css', '.scss', '.sass', '.zig', '.proto'
        }:
            pat = re.compile(r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|/\*[\s\S]*?\*/|//.*')
            text = pat.sub(lambda m: m.group(1) if m.group(1) is not None else '', text)
        elif suffix in {'.yaml', '.yml', '.sh', '.bash', '.zsh', '.ps1', '.sql', '.r', '.jl', '.toml'}:
            pat = re.compile(r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|#.*')
            text = pat.sub(lambda m: m.group(1) if m.group(1) is not None else '', text)
        elif suffix in {'.html', '.xml', '.xaml', '.csproj'}:
            pat = re.compile(r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|<!--[\s\S]*?-->')
            text = pat.sub(lambda m: m.group(1) if m.group(1) is not None else '', text)
        elif suffix in {'.tex', '.bib', '.sty', '.cls'}:
            pat = re.compile(r'(?<!\\)%.*')
            text = pat.sub('', text)

    return collapse_blank_lines(text, max_consecutive=1)

def add_line_numbers(text: str) -> str:
    """Prepends formatted line numbers (e.g. '   1 | ...') to each line."""
    lines = text.splitlines()
    if not lines:
        return ""
    width = max(len(str(len(lines))), 3)
    return "\n".join(f"{i:>{width}} | {line}" for i, line in enumerate(lines, 1))

def get_code_fence(text: str) -> str:
    """Returns a markdown backtick fence strictly longer than any internal backtick sequence."""
    max_ticks = 2
    for match in re.finditer(r'`+', text):
        max_ticks = max(max_ticks, len(match.group(0)))
    return '`' * (max_ticks + 1)

def format_file_block(rel_path: Path, content: str, line_numbers: bool = False) -> str:
    """Formats markdown section header with dynamic backtick fencing and zero empty line padding."""
    clean_body = content.strip()
    if line_numbers and clean_body:
        clean_body = add_line_numbers(clean_body)

    ext = rel_path.suffix.lstrip('.').lower()
    lang = LANG_MAP.get(ext, ext)
    fence = get_code_fence(clean_body)
    return f"\n## File: `{rel_path.as_posix()}`\n\n{fence}{lang}\n{clean_body}\n{fence}\n\n"

def estimate_tokens(char_count: int) -> int:
    """Fast local heuristic estimation (approx 4 chars per token)."""
    return char_count // 4

def bundle_codebase(
    target_dir: str, 
    output_path: str = None, 
    custom_name: str = "",
    strip_comments: bool = True,
    include_docstrings: bool = True,
    include_md: bool = False,
    extra_exts: list[str] = None,
    extra_excludes: list[str] = None,
    max_size_kb: int = 500,
    line_numbers: bool = False
) -> Path:
    """Traverse codebase, generate structure tree, extract code, and stream markdown bundle to disk."""
    root_path = Path(target_dir).resolve()
    if not root_path.is_dir():
        raise ValueError(f"Target path is not a valid directory: {target_dir}")

    base_name = custom_name.strip() if custom_name.strip() else root_path.name
    
    if output_path:
        out_file = Path(output_path).resolve()
        if out_file.is_dir():
            out_file = out_file / f"{base_name}_AI_BUNDLE.md"
    else:
        out_file = root_path.parent / f"{base_name}_AI_BUNDLE.md"

    exts = set(DEFAULT_EXTS)
    if include_md:
        exts.add('.md')
    if extra_exts:
        for ext in extra_exts:
            clean_ext = ext.strip().lower()
            if not clean_ext.startswith('.'):
                clean_ext = f".{clean_ext}"
            exts.add(clean_ext)

    excludes = set(DEFAULT_EXCLUDES)
    if extra_excludes:
        for ex in extra_excludes:
            clean_ex = ex.strip()
            if clean_ex:
                excludes.add(clean_ex)

    gitignore_rules = load_gitignore_rules(root_path)

    repo_structure = [f"# Repository Structure: `{root_path.name}`\n\n```text\n"]
    files_to_process = []

    print(f"Scanning codebase: {root_path.name}...")
    for root, dirs, files in os.walk(root_path):
        rel = Path(root).relative_to(root_path)
        
        # Filter directories: default excludes, custom excludes, hidden dirs, and .gitignore
        dirs[:] = [
            d for d in dirs 
            if d not in excludes 
            and not d.startswith('.')
            and not is_path_ignored(rel / d, gitignore_rules, is_dir=True)
        ]
        
        indent = '    ' * len(rel.parts) if rel != Path('.') else ''
        rel_str = rel.as_posix()

        # Target explicit truncation paths for non-desktop / bloated vendor subtrees
        is_target_truncate = any(p in rel_str for p in ["include/native/directx", "spirv/include/spirv", "vk_video"])
        is_wsi_bloat = "wsi" in rel_str and any(w in rel_str for w in ["glfw", "sdl2", "sdl3"])

        if is_target_truncate or is_wsi_bloat:
            total_truncated_files = sum(len(f) for _, _, f in os.walk(root))
            if total_truncated_files > 0:
                repo_structure.append(f"{indent}{os.path.basename(root)}/ [~{total_truncated_files} cross-platform asset/SDK files truncated]\n")
            dirs[:] = []
            continue

        repo_structure.append(f"{indent}{os.path.basename(root)}/\n" if indent else f"{root_path.name}/\n")

        for f in sorted(files):
            # Exclude hidden files, self-bundle output file, and .gitignore matches
            if f.startswith('.') or f == out_file.name:
                continue

            f_path = Path(root) / f
            rel_file = f_path.relative_to(root_path)
            if is_path_ignored(rel_file, gitignore_rules, is_dir=False):
                continue

            f_lower = f.lower()
            if any(plat in f_lower for plat in ["android", "fuchsia", "macos", "ios", "metal", "wayland", "xcb", "xlib", "directfb", "ggp", "ohos", "screen"]):
                continue
            if any(codec in f_lower for codec in ["av1", "h264", "h265", "vp9"]):
                continue

            if f_path.suffix.lower() in exts:
                # Skip binary files with whitelisted extensions (e.g. SQLite, pickle, binary assets)
                if is_binary_file(f_path):
                    continue

                repo_structure.append(f"{indent}    {f}\n")
                files_to_process.append(f_path)

    repo_structure.append("```\n\n# File Contents\n\n")

    print(f"Bundling {len(files_to_process)} files (streaming to disk)...")
    total_chars = 0

    with open(out_file, "w", encoding="utf-8") as out:
        def write_chunk(chunk: str):
            nonlocal total_chars
            out.write(chunk)
            total_chars += len(chunk)

        # Write directory structure
        for struct_line in repo_structure:
            write_chunk(struct_line)

        # Stream file contents directly to disk
        for fpath in files_to_process:
            if fpath.suffix.lower() == '.md' and not include_md:
                continue

            rel_fpath = fpath.relative_to(root_path)
            file_body = ""

            # Check file size limit
            try:
                f_size_kb = fpath.stat().st_size / 1024
                if max_size_kb > 0 and f_size_kb > max_size_kb:
                    file_body = f"// [FILE TRUNCATED: File size ({f_size_kb:.1f} KB) exceeds configured limit ({max_size_kb} KB)]"
                    write_chunk(format_file_block(rel_fpath, file_body, line_numbers=False))
                    continue
            except OSError:
                pass

            try:
                if fpath.suffix.lower() == '.ipynb':
                    with open(fpath, 'r', encoding='utf-8') as nbf:
                        nb_cells = []
                        for cell in json.load(nbf).get('cells', []):
                            cell_type = cell.get('cell_type', 'code')
                            src = "".join(cell.get('source', []))
                            if cell_type == 'code':
                                cleaned = strip_python_code(src, strip_comments=strip_comments, include_docstrings=include_docstrings)
                                nb_cells.append(cleaned)
                            else:
                                nb_cells.append(f"# [{cell_type.upper()}]\n" + src)
                        file_body = collapse_blank_lines("\n\n".join(nb_cells), max_consecutive=1)
                else:
                    with open(fpath, 'r', encoding='utf-8', errors='replace') as cf:
                        file_body = strip_code(cf.read(), fpath.suffix.lower(), strip_comments=strip_comments, include_docstrings=include_docstrings)

                write_chunk(format_file_block(rel_fpath, file_body, line_numbers=line_numbers))
            except Exception as e:
                write_chunk(f"\n> **Error processing {fpath.name}:** {e}\n\n")

    size_kb = out_file.stat().st_size / 1024
    tokens = estimate_tokens(total_chars)

    print("\n" + "=" * 40)
    print(f"Bundle created:   {out_file}")
    print(f"Bundle size:      {size_kb:.2f} KB")
    print(f"Total characters: {total_chars:,}")
    print(f"Estimated tokens: {tokens:,} (approx 4 chars/token)")
    print("=" * 40 + "\n")

    return out_file

def main():
    parser = argparse.ArgumentParser(description="Bundle a codebase into a clean, LLM-ready markdown file.")
    parser.add_argument("input_dir", nargs="?", default=None, help="Path to project repository directory")
    parser.add_argument("-o", "--output", default=None, help="Output markdown bundle path or directory")
    parser.add_argument("-n", "--name", default="", help="Custom project output name")
    parser.add_argument("--keep-comments", action="store_true", help="Do not strip comments")
    parser.add_argument("--no-docstrings", action="store_true", help="Strip python docstrings")
    parser.add_argument("--include-md", action="store_true", help="Include markdown files in bundle")
    parser.add_argument("--ext", default="", help="Comma-separated additional file extensions (e.g. .cu,.m)")
    parser.add_argument("--exclude", default="", help="Comma-separated additional folder names to exclude (e.g. data,weights)")
    parser.add_argument("--max-size-kb", type=int, default=500, help="Maximum file size in KB before truncation (default: 500)")
    parser.add_argument("--line-numbers", "-l", action="store_true", help="Prepend line numbers to code lines")

    args = parser.parse_args()

    target_dir = args.input_dir
    if not target_dir:
        target_dir = input("Enter path to repository folder: ").strip().strip('"').strip("'")

    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory.")
        sys.exit(1)

    extra_exts = [e.strip() for e in args.ext.split(",") if e.strip()] if args.ext else []
    extra_excludes = [e.strip() for e in args.exclude.split(",") if e.strip()] if args.exclude else []

    bundle_codebase(
        target_dir=target_dir,
        output_path=args.output,
        custom_name=args.name,
        strip_comments=not args.keep_comments,
        include_docstrings=not args.no_docstrings,
        include_md=args.include_md,
        extra_exts=extra_exts,
        extra_excludes=extra_excludes,
        max_size_kb=args.max_size_kb,
        line_numbers=args.line_numbers
    )

if __name__ == "__main__":
    main()
