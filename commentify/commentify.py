#!/usr/bin/env python3
"""
A simple command-line utility for formatting text in the clipboard. Primary 
use-cases are removing line-breaks from copied text (ie from a PDF), and adding
line breaks to make text suitable as code comments. 
"""

# TODO: Triple comments in Python are string literals, used for docstrings.

import argparse
import pyperclip


START_BLOCK_COMMENT = {'py': '"""', 'js': '/**'}
END_BLOCK_COMMENT = {'py': '"""', 'js': ' */'}
LINE_COMMENT = {'py': '# ', 'js': '// '}


def quote(text):
    paragraphs = []
    for paragraph in text.split('\n'):
        if len(paragraph):
            while paragraph[-1] == ' ':
                paragraph = paragraph[:-1]
            paragraphs.append('"' + paragraph + '"')
    quoted_text = "\n\n".join(paragraphs)
    return quoted_text


def line_comments(text, style, indent, max=79):
    max -= indent
    indent = ' ' * indent
    text = text.split(' ')
    new_text = ['']
    new_text += indent + LINE_COMMENT[style]
    line = 0

    for word in text:
        if len(new_text[line] + word) >= max:
            new_text[line] += '\n' + indent
            line += 1
            new_text.append(LINE_COMMENT[style] + word)
        else:
            new_text[line] += ' ' + word

    new_text = ''.join(new_text)
    print(new_text)
    return new_text


def block(text, comment_style, indent, max=79):
    """Reflow text to fit max column width and add selected delimiters."""
    max -= indent
    indent = indent * ' '
    text = text.replace('\n', ' \n ')
    text = text.split(' ')
    new_text = [indent]
    if comment_style:
        new_text[0] += indent + START_BLOCK_COMMENT[comment_style] + '\n'
    if comment_style == "js":
        max -= 3
        new_text[0] += indent + ' * '
    line = 0

    for word in text:
        if word == '':
            continue
        if len(new_text[line] + word) >= max or word == '\n':
            if word == '\n':
                word = ''
            else:
                word += ' '
            new_text[line] += '\n'
            if comment_style == "js":
                new_text[line] += ' * '
            line += 1
            new_text.append(word)
        else:
            new_text[line] += word + ' '

    new_text = ''.join(new_text)
    if comment_style:
        new_text += '\n' + END_BLOCK_COMMENT[comment_style] + '\n'
    print(new_text)
    return new_text


def remove_line_breaks(text):
    new_text = text.replace('\n', ' ')
    print(new_text)
    return new_text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--python',
        action='store_true',
        dest='python',
        help='output as Python-style comments or docstring string literals (# '
        + 'or """). Default docstring style. Use option --line-comments (-l) '
        + 'for comments.'
    )
    parser.add_argument(
        '-j',
        '--javascript',
        action='store_true',
        dest="javascript",
        help='output as JavaScript-style comments (// or /* */). Default block'
        + 'comment style. Use option --line-comments (-l) for line comment '
        + 'style.',
    )
    parser.add_argument(
        '-l',
        '--line-comments',
        action='store_true',
        dest='line',
        help='output as line comments. Note that Python block comments are same'
        + 'as line comments.',
    )
    parser.add_argument(
        '-b',
        '--block-comments',
        default=True,
        action='store_true',
        dest='block',
        help='output as block comment, or docstring string literal for Python'
    )
    parser.add_argument(
        '-m',
        '--max-lines',
        action='store',
        default=80,
        dest="max_lines",
        help='insert newlines after specified maximum line length '
        + '(default 80)',
    )
    parser.add_argument(
        '-r',
        '--remove',
        action='store_true',
        help='remove line breaks from text. Incompatible with comment style '
        + 'options'
    )
    parser.add_argument(
        '-q',
        '--quote',
        action='store_true',
        help='surround text with quotes'
    )
    parser.add_argument(
        '-i',
        '--indent',
        action='count',
        help='add indent for each time option is used. Indent depnds on style.'
        + 'Default 4, 2 for JS. Ie -jiii indents 6 spaces.'
    )
    parser.add_argument(
        '-s',
        '--strip-newlines',
        action='store_true',
        dest='strip',
        help='strip newlines before reformatting'
    )

    args = parser.parse_args()
    indent = args.indent * 4 if args.indent else 0

    text = pyperclip.paste()

    if args.quote:
        output = quote(text)
        print(output)
        pyperclip.copy(output)
        exit()

    if args.python:
        comment_style = "py"
    elif args.javascript:
        comment_style = "js"
        indent = int(indent / 2)
    else:
        comment_style = None

    if args.strip:
        text == text.replace('\n', ' ')

    if args.remove:
        pyperclip.copy(remove_line_breaks(text))
    elif args.line:
        pyperclip.copy(line_comments(
            text, comment_style, indent, args.max_lines))
    elif args.block:
        pyperclip.copy(block(text, comment_style, indent, args.max_lines))


if __name__ == '__main__':
    main()
