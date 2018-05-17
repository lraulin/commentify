# commentify

A simple command-line utility for formatting text in the clipboard. Primary
use-cases are removing line-breaks from copied text (ie from a PDF), and adding
line breaks to make text suitable as code comments. _Requires Pyperclip._

usage: commentify.py [-h][-p] [-j][-l] [-b][-m max_lines] [-r][-q]

optional arguments:

* -h, --help show this help message and exit
* -p, --python output as Python-style comments (# or """). Default
  block commentstyle. Use option --line-comments (-l)
  for line comments.
* -j, --javascript output as JavaScript-style comments (// or /\* \*/).
  Default block comment style. Use option --line-
  comments (-l) for line comment style.
* -l, --line-comments output as line comments
* -b, --block-comments output as block comments (default)
* -m MAX_LINES, --max-lines MAX_LINES
  insert newlines after specified maximum line length
  (default 80)
* -r, --remove remove line breaks from text. Incompatible with
  comment style options
* -q, --quote surround text with quotes
