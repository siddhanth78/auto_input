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
Known issue: Displays nothing when the display is the same length as your terminal width, but input is saved so it is safe to click "Enter" and get input.
