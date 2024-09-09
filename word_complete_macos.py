import sys
import os
import termios
import tty
import fcntl
import struct
from typing import List, Tuple

def get_cursor_position() -> Tuple[int, int]:
    buf = ""
    stdin = sys.stdin.fileno()
    tattr = termios.tcgetattr(stdin)
    try:
        tty.setcbreak(stdin, termios.TCSANOW)
        sys.stdout.write("\033[6n")
        sys.stdout.flush()
        while True:
            buf += sys.stdin.read(1)
            if buf[-1] == "R":
                break
    finally:
        termios.tcsetattr(stdin, termios.TCSANOW, tattr)
    
    matches = re.match(r".*\[(\d*);(\d*)R", buf)
    if matches:
        return int(matches.group(1)), int(matches.group(2))
    return 0, 0

def get_terminal_size() -> Tuple[int, int]:
    h, w, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return h, w

def wrap_text(text: str, width: int) -> List[str]:
    if not text:
        return [""]
    return [text[i : i + width] for i in range(0, len(text), width)] or [""]

def find_str(chars: str, word_list: List[str]) -> Tuple[List[str], int]:
    word_begin_li = [w for w in word_list if w[: len(chars)] == chars]
    word_begin_li.sort()
    return word_begin_li[:15], 0

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def prompt_(words: List[str], prompt_: str = "") -> str:
    sys.stdout.write(prompt_)
    sys.stdout.flush()
    letters = []
    suggestions = []
    sindex = 0
    word = ""
    sflag = 0
    all_words = ""

    terminal_height, terminal_width = get_terminal_size()
    start_row, start_col = get_cursor_position()

    words = list(set(words))

    while True:
        char = getch()

        if char in ('\r', '\n'):
            print()
            return all_words + word

        if char == '\t':
            if suggestions:
                word = suggestions[sindex]
                letters = list(word)
                sindex = (sindex + 1) % len(suggestions)
                sflag = 1
        elif char in ('\b', '\x7f'):
            if letters:
                letters.pop()
                word = "".join(letters)
                sflag = 0
            elif all_words:
                all_words = all_words.rstrip()
                if all_words:
                    all_words = all_words[:-1]
                    words_list = all_words.split()
                    if words_list:
                        word = words_list[-1]
                        all_words = " ".join(words_list[:-1])
                        if all_words:
                            all_words += " "
                        letters = list(word)
                    else:
                        word = ""
                        letters = []
                sflag = 0
        elif char == '\x1b':
            next1, next2 = getch(), getch()
            if next1 == '[':
                if next2 == 'A':  # Up arrow
                    sindex = (sindex - 1) % len(suggestions) if suggestions else 0
                elif next2 == 'B':  # Down arrow
                    sindex = (sindex + 1) % len(suggestions) if suggestions else 0
                if suggestions:
                    word = suggestions[sindex]
                    letters = list(word)
                    sflag = 1
        else:
            if char == " ":
                all_words += word + " "
                letters = []
                word = ""
                sflag = 0
            else:
                letters.append(char)
                word = "".join(letters)
                sflag = 0

        if word.strip():
            if sflag == 0:
                suggestions, sindex = find_str(word, words)
        else:
            suggestions = []

        if suggestions:
            display = f"{prompt_}{all_words}{word} [{' | '.join(suggestions)}]"
        else:
            display = f"{prompt_}{all_words}{word}"
        wrapped_lines = wrap_text(display, terminal_width)

        sys.stdout.write("\033[s")
        sys.stdout.write("\033[J")

        for i, line in enumerate(wrapped_lines):
            current_row = start_row + i
            if current_row >= terminal_height:
                sys.stdout.write(f"\033[{terminal_height};1H\n")
                start_row -= 1
                current_row -= 1
            sys.stdout.write(f"\033[{current_row};1H{line}")
        sys.stdout.flush()

        cursor_row = start_row + len(wrapped_lines) - 1
        cursor_col = len(wrapped_lines[-1]) % terminal_width + 1

        sys.stdout.write(f"\033[{cursor_row};{cursor_col}H")

        sys.stdout.write("\033[s")
        sys.stdout.write("\033[J")

        sys.stdout.flush()

    return all_words + word
