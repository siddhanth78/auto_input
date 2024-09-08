import re
import msvcrt
import sys


def find_str(chars, word_list):
    word_begin_li = [w for w in word_list if w.startswith(chars)]
    return word_begin_li[:10], 0


def clear_current_line():
    sys.stdout.write("\0338\033[0J")
    sys.stdout.flush()


def prompt_(words, prompt_=""):
    sys.stdout.write(f"{prompt_}")
    sys.stdout.write("\u001B[s")
    sys.stdout.flush()

    letters = []
    suggestions = []
    sindex = 0
    word = ""
    sflag = 0
    all_words = ""

    while True:
        if msvcrt.kbhit():
            char = msvcrt.getch()

            if char.startswith(b"\xe0"):
                continue

            char = char.decode()

            if char == "\n" or char == "\r":
                print()
                return all_words + word

            elif char == "\s" or char == " ":
                letters = []
                all_words = all_words + word + " "
                sflag = 0

            elif char == "\b" or char == "\x7f":
                if letters:
                    letters.pop()
                    sflag = 0
                else:
                    if all_words.strip() != "":
                        all_li = all_words.split(" ")
                        if "" in all_li:
                            all_li.remove("")
                        letters = list(all_li[-1] + " ")
                        letters.pop()
                        all_words = (
                            " ".join(all_li[:-1]) + " " if len(all_li) > 1 else ""
                        )
                        sflag = 0

            elif char == "\t":
                if suggestions:
                    letters = list(suggestions[sindex % len(suggestions)])
                    sindex += 1
                    if sindex == len(suggestions):
                        sindex = 0
                    sflag = 1
                else:
                    sflag = 0
                    sindex = 0
            else:
                letters.append(char)

            word = "".join(letters)

            if word.strip() != "":
                if sflag == 0:
                    suggestions, sindex = find_str(word, words)
            elif word.strip() == "":
                suggestions = []

            if suggestions:
                display = f"{all_words}{word} [{'|'.join(suggestions)}]"
            else:
                display = f"{all_words}{word}"

            sys.stdout.write("\u001B[u\033[0J")
            sys.stdout.write(" " * len(display))
            sys.stdout.write("\u001B[u\033[0J")
            sys.stdout.write(display)
            sys.stdout.flush()
