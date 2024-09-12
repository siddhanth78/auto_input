## AutoPyInput

- For Windows
- Requires Python >= 3.10
- Autocomplete words while user input
- Use Tab or arrow keys to cycle through choices

## Usage

```
from autopyinput.word_complete import Wordcompleter
import autopyinput.utils as au

# Custom words
word_list = ['hello', 'world', 'word', 'hi']
wc = Wordcompleter(word_list)
input_ = wc.prompt(prompt_ = ">>")
```

```
# Clean up and use string
doc = '''
#hello world!
def main():
  print("hello world")
main()
'''

word_list = au.string_to_words(doc)
wc = Wordcompleter(word_list)
input_ = wc.prompt(prompt_ = ">>")
```

```
# Clean up and use file data
doc = "example.txt"

word_list = au.file_to_words(doc)
wc = Wordcompleter(word_list)
input_ = wc.prompt(prompt_ = ">>")
```

```
# Update suggestions
new_word = "new_word"
wc.add_word(new_word)

new_words_to_suggest = ["new", "words"]
wc.add_list(new_words_to_suggest)
```
