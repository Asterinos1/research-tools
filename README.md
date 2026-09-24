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

