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
wcompleter = Wordcompleter(word_list)
input_ = wcompleter.prompt(prompt_ = ">>")
```

```
# Clean up and use string
doc = '''
#hello world!
def main():
  print("hello world")
main()
'''

word_list = au.string_to_words(au.clean(doc))
wcompleter = Wordcompleter(word_list)
input_ = wcompleter.prompt(prompt_ = ">>")
```

```
# Clean up and use file data
doc = "example.txt"

word_list = au.file_to_words(doc)
wcompleter = Wordcompleter(word_list)
input_ = wcompleter.prompt(prompt_ = ">>")
```

```
# Update suggestions

new_word = "new_word"
wcompleter.add_word(new_word)

new_words_to_suggest = ["new", "words"]
wcompleter.add_list(new_words_to_suggest)
```
