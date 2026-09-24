# Repository Structure: `research-tools`

```text
research-tools/
    README.md
    latex-libraries/
        code.sty
        example.tex
        greekenglish.sty
    python-tools/
        bundler.py
```

# File Contents


## File: `README.md`

````markdown
# Various Tools

In this repo I've gathered various small tools I made during my academic career, tailored to my working style.

## LaTeX Libraries (`latex-libraries/`)

Custom LaTeX packages for academic writing and technical reports:

- **[`code.sty`](latex-libraries/code.sty)**: Provides pretty, dark-themed code blocks (One Dark / Monokai palette) for reports. Includes pre-configured environments for Python, Java, Scala, SQL, JavaScript, HTML, and CSS.
  ```latex
  \usepackage{code}

  \begin{python}
  def hello():
      print("Hello World")
  \end{python}
  ```
- **[`greekenglish.sty`](latex-libraries/greekenglish.sty)**: Offers seamless bilingual Greek and English support using Unicode fonts (`fontspec` + `babel`). Allows typing Greek directly without `\foreignlanguage` or `\textgreek`.
  - **Compiler Requirement**: Use **LuaLaTeX** or **XeLaTeX**.
  - **Font Requirement**: Requires the `Libertinus Serif` font installed on your system.
  ```latex
  \usepackage{greekenglish}
  ```

A rendered demonstration is available at **[`latex-libraries/example.pdf`](latex-libraries/example.pdf)** (source: [`latex-libraries/example.tex`](latex-libraries/example.tex)).

## Python Tools (`python-tools/`)

- **[`bundler.py`](python-tools/bundler.py)**: Takes a codebase directory as input and packages it into a clean, single Markdown file. It extracts the directory tree structure and the contents of important source files in a layout optimized for both human readability and LLM parsing.

  This tool enabled me to explore how LLMs parse files and how to best structure context to save tokens. It was especially useful during discussions with mainstream AI tools (Gemini, ChatGPT, NotebookLM) before adopting CLI-native AI coding assistants.

  ### Features
  - Strips inline comments (`#`, `//`, `/* */`) while strictly preserving docstrings and string literals.
  - Automatically filters out build directories, virtual environments, caches, and platform-specific bloat.
  - Respects `.gitignore` rules when present.
  - Extracts and formats Jupyter Notebook (`.ipynb`) cells into Python code blocks.
  - Binary file detection (skips compiled assets, pickles, databases).
  - Configurable file size guard (`--max-size-kb`).
  - Low-memory direct disk streaming (handles repositories of any size).
  - Fast local token estimation (approx. 4 chars/token).
  - Zero external dependencies (uses Python standard library only).

  ### Usage
  ```bash
  # Interactive mode (prompts for path)
  python python-tools/bundler.py

  # Direct CLI usage
  python python-tools/bundler.py /path/to/project -o output_bundle.md

  # Additional options
  python python-tools/bundler.py /path/to/project --keep-comments --include-md --line-numbers
  ```

A bundled demonstration of this repository is available at **[`python-tools/example.md`](python-tools/example.md)**.
````


## File: `latex-libraries/code.sty`

```latex
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{code}[2026/02/17 ECE Dark Code Highlighting]

\RequirePackage{xcolor}
\RequirePackage{listings}

\definecolor{bgdark}{RGB}{40, 44, 52}
\definecolor{keyword}{RGB}{198, 120, 221}
\definecolor{string}{RGB}{152, 195, 121}
\definecolor{comment}{RGB}{92, 99, 112}
\definecolor{number}{RGB}{0, 0, 0}
\definecolor{identifier}{RGB}{97, 175, 239}

\lstset{
    backgroundcolor=\color{bgdark},
    commentstyle=\color{comment}\itshape,
    keywordstyle=\color{keyword}\bfseries,
    numberstyle=\small\color{number},
    stringstyle=\color{string},
    identifierstyle=\color{identifier},
    basicstyle=\ttfamily\small\color{white},
    breakatwhitespace=false,
    breaklines=true,
    captionpos=b,
    keepspaces=true,
    numbers=left,
    numbersep=10pt,
    showspaces=false,
    showstringspaces=false,
    tabsize=4,
    frame=tb,
    rulecolor=\color{gray},
    framerule=0.5pt,
    mathescape=false,
    escapeinside={(*@}{@*)},
}

\lstdefinelanguage{JavaScript}{
    keywords={typeof, new, true, false, catch, function, return, null, switch, var, let, const, if, in, while, do, else, case, break, async, await, class, export, import, this},
    sensitive=false,
    comment=[l]{//},
    morecomment=[s]{/*}{*/},
    morestring=[b]',
    morestring=[b]"
}

\lstdefinelanguage{CSS}{
    keywords={color, background, margin, padding, font, width, height, border, display, flex, grid},
    sensitive=false,
    morecomment=[s]{/*}{*/},
    morestring=[b]',
    morestring=[b]"
}

\lstnewenvironment{python}[1][]{\lstset{language=Python, #1}}{}
\lstnewenvironment{java}[1][]{\lstset{language=Java, #1}}{}
\lstnewenvironment{scala}[1][]{\lstset{language=Scala, #1}}{}
\lstnewenvironment{sql}[1][]{\lstset{language=SQL, #1}}{}
\lstnewenvironment{javascript}[1][]{\lstset{language=JavaScript, #1}}{}
\lstnewenvironment{htmlcode}[1][]{\lstset{language=HTML, #1}}{}
\lstnewenvironment{csscode}[1][]{\lstset{language=CSS, #1}}{}
```


## File: `latex-libraries/example.tex`

```latex
\documentclass[11pt,a4paper]{article}

\usepackage{geometry}
\geometry{margin=1in}

\usepackage{greekenglish}

\usepackage{code}

\title{\textbf{Research Tools: LaTeX Libraries Demonstration}}
\author{Asterinos}

\begin{document}

\maketitle

\section{Introduction / Εισαγωγή}
This document demonstrates the two custom packages in the \texttt{latex/} folder:
\begin{itemize}
    \item \texttt{greekenglish.sty}: Enables typing both English and Greek seamlessly using Unicode fonts with LuaLaTeX / XeLaTeX.
    \item \texttt{code.sty}: Provides stylish dark-mode syntax highlighted code environments for various languages.
\end{itemize}

\subsection{Bilingual Text Switching (Άμεση εναλλαγή γλωσσών)}
Here is an example use of English and Greek text:
\begin{quote}
    The quick brown fox jumps over the lazy dog.
    Η γρήγορη καφέ αλεπού πηδά πάνω από το τεμπέλικο σκυλί.
    Η επιστήμη των υπολογιστών και οι σύγχρονες τεχνολογίες επεξεργασίας δεδομένων.
    Computer science and modern data engineering technologies.
\end{quote}
No commands were required.

\section{Code Highlighting Examples}

\subsection{Python Environment}
\begin{python}
# Python sample code
def fibonacci(n: int) -> list[int]:
    """Generate Fibonacci sequence up to n numbers."""
    if n <= 0:
        return []
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]

if __name__ == "__main__":
    print(f"Fibonacci(8): {fibonacci(8)}")
\end{python}

\subsection{SQL Environment}
\begin{sql}
-- Query user research analytics
SELECT
    u.id,
    u.username,
    COUNT(r.id) AS total_runs,
    AVG(r.execution_time_ms) AS avg_time_ms
FROM users u
LEFT JOIN research_runs r ON u.id = r.user_id
WHERE r.created_at >= '2026-01-01'
GROUP BY u.id, u.username
ORDER BY total_runs DESC;
\end{sql}

\subsection{JavaScript Environment}
\begin{javascript}
// Modern async fetch function
async function fetchResearchData(endpoint) {
    try {
        const response = await fetch(`https://api.research.local/${endpoint}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (err) {
        console.error("Failed to fetch research metrics:", err);
    }
}
\end{javascript}

\end{document}
```


## File: `latex-libraries/greekenglish.sty`

```latex
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{greekenglish}[2026/02/17 Unicode Greek/English Switch]

\RequirePackage{fontspec}

\RequirePackage[greek, english]{babel}

\babelfont{rm}{Libertinus Serif}
\babelfont[greek]{rm}{Libertinus Serif}

\babelprovide[import, main, onchar=ids fonts]{english}
\babelprovide[import, onchar=ids fonts]{greek}
```


## File: `python-tools/bundler.py`

````python
import os
import sys
import io
import json
import re
import fnmatch
import tokenize
import argparse
from pathlib import Path

DEFAULT_EXCLUDES ={
'.git','.svn','.hg','.idea','.vscode','__pycache__',
'.pytest_cache','.mypy_cache','.ruff_cache','.tox',
'venv','.venv','node_modules','dist','build',
'external','test','tests','docs','cmake','bindings',
'bin','obj'
}

DEFAULT_EXTS ={
'.py','.ipynb','.js','.ts','.jsx','.tsx',
'.c','.cpp','.h','.hpp','.cc','.cxx',
'.cs','.rs','.go','.kt','.swift','.scala','.java',
'.html','.css','.scss','.sass',
'.sh','.bash','.zsh','.ps1',
'.sql','.r','.jl','.lua','.zig',
'.tex','.bib','.sty','.cls',
'.yaml','.yml','.toml','.json','.proto',
'.xaml','.csproj'
}

LANG_MAP ={
'ipynb':'python',
'txt':'text',
'cs':'csharp',
'rs':'rust',
'go':'go',
'kt':'kotlin',
'swift':'swift',
'java':'java',
'scala':'scala',
'py':'python',
'js':'javascript',
'ts':'typescript',
'jsx':'javascript',
'tsx':'typescript',
'c':'c',
'cpp':'cpp',
'h':'c',
'hpp':'cpp',
'cc':'cpp',
'cxx':'cpp',
'lua':'lua',
'zig':'zig',
'r':'r',
'jl':'julia',
'sql':'sql',
'sh':'bash',
'bash':'bash',
'zsh':'bash',
'ps1':'powershell',
'tex':'latex',
'bib':'bibtex',
'sty':'latex',
'cls':'latex',
'yaml':'yaml',
'yml':'yaml',
'toml':'toml',
'json':'json',
'proto':'protobuf',
'html':'html',
'css':'css',
'scss':'scss',
'sass':'sass',
'xml':'xml',
'xaml':'xml',
'csproj':'xml',
'md':'markdown'
}

def load_gitignore_rules (root_path :Path )->list [str ]:
    """Parse .gitignore rules if present in the target directory root."""
    gitignore_file =root_path /".gitignore"
    if not gitignore_file .is_file ():
        return []
    rules =[]
    try :
        with open (gitignore_file ,"r",encoding ="utf-8",errors ="replace")as f :
            for line in f :
                line =line .strip ()
                if line and not line .startswith ("#"):
                    rules .append (line )
    except Exception :
        pass
    return rules

def is_path_ignored (rel_path :Path ,gitignore_rules :list [str ],is_dir :bool =False )->bool :
    """Check if a relative path matches any parsed .gitignore pattern."""
    rel_posix =rel_path .as_posix ()
    name =rel_path .name
    for rule in gitignore_rules :
        rule_clean =rule .strip ("/")
        if rule .endswith ("/")and not is_dir :
            continue
        if fnmatch .fnmatch (name ,rule_clean ):
            return True
        if fnmatch .fnmatch (rel_posix ,rule_clean )or fnmatch .fnmatch (rel_posix ,f"*/{rule_clean }*")or fnmatch .fnmatch (rel_posix ,f"{rule_clean }/*"):
            return True
    return False

def is_binary_file (file_path :Path )->bool :
    """Detect if a file contains null bytes within its first 1024 bytes."""
    try :
        with open (file_path ,"rb")as f :
            chunk =f .read (1024 )
            return b"\x00"in chunk
    except Exception :
        return False

def collapse_blank_lines (text :str ,max_consecutive :int =1 )->str :
    """Strip trailing line whitespace, collapse consecutive blank lines, and strip edges."""
    lines =[line .rstrip ()for line in text .splitlines ()]
    result =[]
    blank_count =0
    for line in lines :
        if line =="":
            blank_count +=1
            if blank_count <=max_consecutive :
                result .append (line )
        else :
            blank_count =0
            result .append (line )
    return "\n".join (result ).strip ()

def strip_python_code (source :str ,strip_comments :bool =True ,include_docstrings :bool =True )->str :
    """Safely strip comments and docstrings using Python's tokenize module."""
    if not strip_comments and include_docstrings :
        return source
    try :
        tokens =tokenize .generate_tokens (io .StringIO (source ).readline )
        filtered =[]
        prev_type =tokenize .INDENT
        for tok in tokens :
            ttype ,tval ,start ,end ,line =tok
            if strip_comments and ttype ==tokenize .COMMENT :
                continue
            if not include_docstrings and ttype ==tokenize .STRING :
                if prev_type in (tokenize .INDENT ,tokenize .NEWLINE ,tokenize .NL ,tokenize .ENCODING ):
                    continue
            filtered .append ((ttype ,tval ))
            if ttype not in (tokenize .NL ,tokenize .COMMENT ):
                prev_type =ttype
        return tokenize .untokenize (filtered )
    except Exception :
        return source

def strip_code (text :str ,suffix :str ,strip_comments :bool =True ,include_docstrings :bool =True )->str :
    """Strips comments without damaging string literals across supported languages and cleans blank lines."""
    if suffix =='.py':
        if strip_comments or not include_docstrings :
            text =strip_python_code (text ,strip_comments =strip_comments ,include_docstrings =include_docstrings )
    elif strip_comments :
        if suffix in {
        '.c','.cpp','.h','.hpp','.cc','.cxx','.cs','.rs','.go',
        '.kt','.swift','.scala','.java','.js','.ts','.jsx','.tsx',
        '.css','.scss','.sass','.zig','.proto'
        }:
            pat =re .compile (r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|/\*[\s\S]*?\*/|//.*')
            text =pat .sub (lambda m :m .group (1 )if m .group (1 )is not None else '',text )
        elif suffix in {'.yaml','.yml','.sh','.bash','.zsh','.ps1','.sql','.r','.jl','.toml'}:
            pat =re .compile (r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|#.*')
            text =pat .sub (lambda m :m .group (1 )if m .group (1 )is not None else '',text )
        elif suffix in {'.html','.xml','.xaml','.csproj'}:
            pat =re .compile (r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|<!--[\s\S]*?-->')
            text =pat .sub (lambda m :m .group (1 )if m .group (1 )is not None else '',text )
        elif suffix in {'.tex','.bib','.sty','.cls'}:
            pat =re .compile (r'(?<!\\)%.*')
            text =pat .sub ('',text )

    return collapse_blank_lines (text ,max_consecutive =1 )

def add_line_numbers (text :str )->str :
    """Prepends formatted line numbers (e.g. '   1 | ...') to each line."""
    lines =text .splitlines ()
    if not lines :
        return ""
    width =max (len (str (len (lines ))),3 )
    return "\n".join (f"{i :>{width }} | {line }"for i ,line in enumerate (lines ,1 ))

def get_code_fence (text :str )->str :
    """Returns a markdown backtick fence strictly longer than any internal backtick sequence."""
    max_ticks =2
    for match in re .finditer (r'`+',text ):
        max_ticks =max (max_ticks ,len (match .group (0 )))
    return '`'*(max_ticks +1 )

def format_file_block (rel_path :Path ,content :str ,line_numbers :bool =False )->str :
    """Formats markdown section header with dynamic backtick fencing and zero empty line padding."""
    clean_body =content .strip ()
    if line_numbers and clean_body :
        clean_body =add_line_numbers (clean_body )

    ext =rel_path .suffix .lstrip ('.').lower ()
    lang =LANG_MAP .get (ext ,ext )
    fence =get_code_fence (clean_body )
    return f"\n## File: `{rel_path .as_posix ()}`\n\n{fence }{lang }\n{clean_body }\n{fence }\n\n"

def estimate_tokens (char_count :int )->int :
    """Fast local heuristic estimation (approx 4 chars per token)."""
    return char_count //4

def bundle_codebase (
target_dir :str ,
output_path :str =None ,
custom_name :str ="",
strip_comments :bool =True ,
include_docstrings :bool =True ,
include_md :bool =False ,
extra_exts :list [str ]=None ,
extra_excludes :list [str ]=None ,
max_size_kb :int =500 ,
line_numbers :bool =False
)->Path :
    """Traverse codebase, generate structure tree, extract code, and stream markdown bundle to disk."""
    root_path =Path (target_dir ).resolve ()
    if not root_path .is_dir ():
        raise ValueError (f"Target path is not a valid directory: {target_dir }")

    base_name =custom_name .strip ()if custom_name .strip ()else root_path .name

    if output_path :
        out_file =Path (output_path ).resolve ()
        if out_file .is_dir ():
            out_file =out_file /f"{base_name }_AI_BUNDLE.md"
    else :
        out_file =root_path .parent /f"{base_name }_AI_BUNDLE.md"

    exts =set (DEFAULT_EXTS )
    if include_md :
        exts .add ('.md')
    if extra_exts :
        for ext in extra_exts :
            clean_ext =ext .strip ().lower ()
            if not clean_ext .startswith ('.'):
                clean_ext =f".{clean_ext }"
            exts .add (clean_ext )

    excludes =set (DEFAULT_EXCLUDES )
    if extra_excludes :
        for ex in extra_excludes :
            clean_ex =ex .strip ()
            if clean_ex :
                excludes .add (clean_ex )

    gitignore_rules =load_gitignore_rules (root_path )

    repo_structure =[f"# Repository Structure: `{root_path .name }`\n\n```text\n"]
    files_to_process =[]

    print (f"Scanning codebase: {root_path .name }...")
    for root ,dirs ,files in os .walk (root_path ):
        rel =Path (root ).relative_to (root_path )

        dirs [:]=[
        d for d in dirs
        if d not in excludes
        and not d .startswith ('.')
        and not is_path_ignored (rel /d ,gitignore_rules ,is_dir =True )
        ]

        indent ='    '*len (rel .parts )if rel !=Path ('.')else ''
        rel_str =rel .as_posix ()

        is_target_truncate =any (p in rel_str for p in ["include/native/directx","spirv/include/spirv","vk_video"])
        is_wsi_bloat ="wsi"in rel_str and any (w in rel_str for w in ["glfw","sdl2","sdl3"])

        if is_target_truncate or is_wsi_bloat :
            total_truncated_files =sum (len (f )for _ ,_ ,f in os .walk (root ))
            if total_truncated_files >0 :
                repo_structure .append (f"{indent }{os .path .basename (root )}/ [~{total_truncated_files } cross-platform asset/SDK files truncated]\n")
            dirs [:]=[]
            continue

        repo_structure .append (f"{indent }{os .path .basename (root )}/\n"if indent else f"{root_path .name }/\n")

        for f in sorted (files ):

            if f .startswith ('.')or f ==out_file .name :
                continue

            f_path =Path (root )/f
            rel_file =f_path .relative_to (root_path )
            if is_path_ignored (rel_file ,gitignore_rules ,is_dir =False ):
                continue

            f_lower =f .lower ()
            if any (plat in f_lower for plat in ["android","fuchsia","macos","ios","metal","wayland","xcb","xlib","directfb","ggp","ohos","screen"]):
                continue
            if any (codec in f_lower for codec in ["av1","h264","h265","vp9"]):
                continue

            if f_path .suffix .lower ()in exts :

                if is_binary_file (f_path ):
                    continue

                repo_structure .append (f"{indent }    {f }\n")
                files_to_process .append (f_path )

    repo_structure .append ("```\n\n# File Contents\n\n")

    print (f"Bundling {len (files_to_process )} files (streaming to disk)...")
    total_chars =0

    with open (out_file ,"w",encoding ="utf-8")as out :
        def write_chunk (chunk :str ):
            nonlocal total_chars
            out .write (chunk )
            total_chars +=len (chunk )

        for struct_line in repo_structure :
            write_chunk (struct_line )

        for fpath in files_to_process :
            if fpath .suffix .lower ()=='.md'and not include_md :
                continue

            rel_fpath =fpath .relative_to (root_path )
            file_body =""

            try :
                f_size_kb =fpath .stat ().st_size /1024
                if max_size_kb >0 and f_size_kb >max_size_kb :
                    file_body =f"// [FILE TRUNCATED: File size ({f_size_kb :.1f} KB) exceeds configured limit ({max_size_kb } KB)]"
                    write_chunk (format_file_block (rel_fpath ,file_body ,line_numbers =False ))
                    continue
            except OSError :
                pass

            try :
                if fpath .suffix .lower ()=='.ipynb':
                    with open (fpath ,'r',encoding ='utf-8')as nbf :
                        nb_cells =[]
                        for cell in json .load (nbf ).get ('cells',[]):
                            cell_type =cell .get ('cell_type','code')
                            src ="".join (cell .get ('source',[]))
                            if cell_type =='code':
                                cleaned =strip_python_code (src ,strip_comments =strip_comments ,include_docstrings =include_docstrings )
                                nb_cells .append (cleaned )
                            else :
                                nb_cells .append (f"# [{cell_type .upper ()}]\n"+src )
                        file_body =collapse_blank_lines ("\n\n".join (nb_cells ),max_consecutive =1 )
                else :
                    with open (fpath ,'r',encoding ='utf-8',errors ='replace')as cf :
                        file_body =strip_code (cf .read (),fpath .suffix .lower (),strip_comments =strip_comments ,include_docstrings =include_docstrings )

                write_chunk (format_file_block (rel_fpath ,file_body ,line_numbers =line_numbers ))
            except Exception as e :
                write_chunk (f"\n> **Error processing {fpath .name }:** {e }\n\n")

    size_kb =out_file .stat ().st_size /1024
    tokens =estimate_tokens (total_chars )

    print ("\n"+"="*40 )
    print (f"Bundle created:   {out_file }")
    print (f"Bundle size:      {size_kb :.2f} KB")
    print (f"Total characters: {total_chars :,}")
    print (f"Estimated tokens: {tokens :,} (approx 4 chars/token)")
    print ("="*40 +"\n")

    return out_file

def main ():
    parser =argparse .ArgumentParser (description ="Bundle a codebase into a clean, LLM-ready markdown file.")
    parser .add_argument ("input_dir",nargs ="?",default =None ,help ="Path to project repository directory")
    parser .add_argument ("-o","--output",default =None ,help ="Output markdown bundle path or directory")
    parser .add_argument ("-n","--name",default ="",help ="Custom project output name")
    parser .add_argument ("--keep-comments",action ="store_true",help ="Do not strip comments")
    parser .add_argument ("--no-docstrings",action ="store_true",help ="Strip python docstrings")
    parser .add_argument ("--include-md",action ="store_true",help ="Include markdown files in bundle")
    parser .add_argument ("--ext",default ="",help ="Comma-separated additional file extensions (e.g. .cu,.m)")
    parser .add_argument ("--exclude",default ="",help ="Comma-separated additional folder names to exclude (e.g. data,weights)")
    parser .add_argument ("--max-size-kb",type =int ,default =500 ,help ="Maximum file size in KB before truncation (default: 500)")
    parser .add_argument ("--line-numbers","-l",action ="store_true",help ="Prepend line numbers to code lines")

    args =parser .parse_args ()

    target_dir =args .input_dir
    if not target_dir :
        target_dir =input ("Enter path to repository folder: ").strip ().strip ('"').strip ("'")

    if not os .path .isdir (target_dir ):
        print (f"Error: '{target_dir }' is not a valid directory.")
        sys .exit (1 )

    extra_exts =[e .strip ()for e in args .ext .split (",")if e .strip ()]if args .ext else []
    extra_excludes =[e .strip ()for e in args .exclude .split (",")if e .strip ()]if args .exclude else []

    bundle_codebase (
    target_dir =target_dir ,
    output_path =args .output ,
    custom_name =args .name ,
    strip_comments =not args .keep_comments ,
    include_docstrings =not args .no_docstrings ,
    include_md =args .include_md ,
    extra_exts =extra_exts ,
    extra_excludes =extra_excludes ,
    max_size_kb =args .max_size_kb ,
    line_numbers =args .line_numbers
    )

if __name__ =="__main__":
    main ()
````

