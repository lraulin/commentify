#!/usr/bin/env python3
"""
A simple command-line utility for formatting text in the clipboard. Primary 
use-cases are removing line-breaks from copied text (ie from a PDF), and adding
line breaks to make text suitable as code comments.
"""

import argparse
import pyperclip


START_BLOCK_COMMENT = {"py": '"""', "js": "/**"}
END_BLOCK_COMMENT = {"py": '"""', "js": " */"}


def python_line():
    text = pyperclip.paste()
    print(text)
    text = text.split(' ')
    new_text = ['#']
    line = 0

    for word in text:
        if len(new_text[line] + word) >= 80:
            new_text[line] += '\n'
            line += 1
            new_text.append("# " + word)
        else:
            new_text[line] += ' ' + word

    new_text = ''.join(new_text)
    pyperclip.copy(new_text)


def block(text, comment_style, max=80):

    text = text.replace('\n', ' ')
    text = text.split(' ')
    new_text = ['']
    if comment_style:
        new_text[0] = new_text[0] + \
            START_BLOCK_COMMENT[comment_style] + '\n * '
    if comment_style == "js":
        max -= 3
    line = 0

    for word in text:
        if len(new_text[line] + word) >= max:
            new_text[line] += '\n'
            if comment_style == "js":
                new_text[line] += ' * '
            line += 1
            new_text.append(word)
            new_text[line] += ' '
        else:
            new_text[line] += word + ' '

    new_text = ''.join(new_text)
    if comment_style:
        new_text += '\n' + END_BLOCK_COMMENT[comment_style] + '\n'
    print(new_text)
    return new_text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--python',
        action='store_true',
        default=False,
        dest='python',
        help='Output as Python-style comments (# or """). Default block comment'
        + 'style. Use option --line-comments (-l) for line comments.'
    )
    parser.add_argument(
        '-j',
        '--javascript',
        action='store_true',
        default=False,
        dest="javascript",
        help='Output as JavaScript-style comments (// or /* */). Default block '
        + 'comment style. Use option --line-comments (-l) for line comment style.',
    )
    parser.add_argument(
        '-l',
        '--line-comments',
        action='store_true',
        default=False,
        help='Output as line comments.',
    )
    parser.add_argument(
        '-b',
        '--block-comments',
        help='Output as block comments. (Default.)',
        default=True,
        action='store_true'
    )
    parser.add_argument(
        '-m',
        '--max-lines',
        action='store',
        default=80,
        dest="max_lines",
        help='insert newlines after specified maximum line length, default 80',
    )
    parser.add_argument(
        '-r',
        '--remove',
        help='remove line breaks from text. incompatible with comment style options',
        action='store_true'
    )
    parser.add_argument(
        '-q',
        '--quote',
        help='surround text with quotes',
        action='store_true'
    )

    args = parser.parse_args()
    print(args)

    text = pyperclip.paste()

    if args.block:
        if args.python:
            comment_style = "py"
        elif args.javascript:
            comment_style = "js"
        else:
            comment_style = None
        pyperclip.copy(block(text, comment_style, args.max_lines))


if __name__ == '__main__':
    main()
