import msvcrt
import sys
import os
import ctypes
from ctypes import wintypes
from typing import List, Tuple

kernel32 = ctypes.windll.kernel32


class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes._COORD),
        ("dwCursorPosition", wintypes._COORD),
        ("wAttributes", wintypes.WORD),
        ("srWindow", wintypes.SMALL_RECT),
        ("dwMaximumWindowSize", wintypes._COORD),
    ]


def get_cursor_position() -> Tuple[int, int]:
    h_stdout = kernel32.GetStdHandle(-11)
    csbi = CONSOLE_SCREEN_BUFFER_INFO()
    kernel32.GetConsoleScreenBufferInfo(h_stdout, ctypes.byref(csbi))
    return csbi.dwCursorPosition.Y + 1, csbi.dwCursorPosition.X + 1


def get_terminal_size() -> Tuple[int, int]:
    h_stdout = kernel32.GetStdHandle(-11)
    csbi = CONSOLE_SCREEN_BUFFER_INFO()
    kernel32.GetConsoleScreenBufferInfo(h_stdout, ctypes.byref(csbi))
    return (
        csbi.srWindow.Bottom - csbi.srWindow.Top + 1,
        csbi.srWindow.Right - csbi.srWindow.Left + 1,
    )


def wrap_text(text: str, width: int) -> List[str]:
    return [text[i : i + width] for i in range(0, len(text), width)]


def find_str(chars: str, word_list: List[str]) -> Tuple[List[str], int]:
    word_begin_li = [w for w in word_list if w.startswith(chars)]
    word_begin_li.sort()
    return word_begin_li, 0


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

    while True:
        if msvcrt.kbhit():
            char = msvcrt.getch()
            if char == b"\xe0":
                arrow = msvcrt.getch()
                if arrow == b"H":
                    sindex = (sindex - 1) % len(suggestions) if suggestions else 0
                elif arrow == b"P":
                    sindex = (sindex + 1) % len(suggestions) if suggestions else 0
                if suggestions:
                    word = suggestions[sindex]
                    letters = list(word)
                    sflag = 1
                continue

            if char in (b"\r", b"\n"):
                print()
                return all_words + word

            if char == b"\t":
                if suggestions:
                    word = suggestions[sindex]
                    letters = list(word)
                    sindex = (sindex + 1) % len(suggestions)
                    sflag = 1
            elif char in (b"\b", b"\x7f"):
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
            else:
                char = char.decode()
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

            display = f"{prompt_}{all_words}{word}"
            wrapped_lines = wrap_text(display, terminal_width)

            num_lines = len(wrapped_lines)

            for i in range(num_lines):
                sys.stdout.write(f"\033[{start_row + i};1H\033[K")

            for i, line in enumerate(wrapped_lines):
                current_row = start_row + i
                if current_row >= terminal_height:
                    sys.stdout.write(f"\033[{terminal_height};1H\n")
                    start_row -= 1
                    current_row -= 1
                sys.stdout.write(f"\033[{current_row};1H{line}")

            if suggestions:
                suggestion_text = f"[{' | '.join(suggestions[:15])}]"
                suggestion_lines = wrap_text(suggestion_text, terminal_width)
                for i, line in enumerate(suggestion_lines):
                    current_row = start_row + num_lines + i
                    if current_row >= terminal_height:
                        sys.stdout.write(f"\033[{terminal_height};1H\n")
                        start_row -= 1
                        current_row -= 1
                    sys.stdout.write(f"\033[{current_row};1H\033[K{line}")

            cursor_row = start_row + len(wrapped_lines) - 1
            cursor_col = len(wrapped_lines[-1]) % terminal_width + 1
            sys.stdout.write(f"\033[{cursor_row};{cursor_col}H")
            sys.stdout.flush()

    return all_words + word
