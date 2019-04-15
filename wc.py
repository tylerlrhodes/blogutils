
#
# todo:
# add context around spelling areas
# file with words to add to dictionary
# better output formatting
# how to handle hyphenated words
# "testing"
# ignore code blocks in markdown - between '''
# ignore markdown links
# it would be nice to add words to the custom dictionary on a word by word basis
# it would be nice to be able to ignore words without adding them to the dictionary per document
# a mode to go from one misspelled word to the next
# 

import sys
import pickle
from spellchecker import SpellChecker

# Filename to check
if len(sys.argv) < 2:
    print('Please provide a file name!')
    exit(1)

# Add words at end of run to custom words?
if len(sys.argv) == 3:
    add_words = bool(sys.argv[2])
else:
    add_words = False

# Single step mode
if len(sys.argv) == 4:
    single_step_mode = bool(sys.argv[3])
else:
    single_step_mode = False


file_name = sys.argv[1]
word_count = 0
custom_words = set()

try:
    with open('pickle.p', 'rb') as f:
        custom_words = pickle.load(f)
except Exception as e:
    print(f'Error loading custom dictionary words! {e}')

# cases to deal with:
# - hyphenated words
# - characters that words can have within them
# - markdown links need to be ignored
# - words with numbers in them should be ignored
# - dealing with when i write something like word1/word2/word3 and use the slash to seperate them
# - strip leading and trailing quotations from words
# 

def remove_links(line):
    # do nothing for now
    return line

def get_line_words(line):
    line = remove_links(line)
    line_words = [w for w in line.split() if not any(c.isdigit() for c in w)]
    for idx, w in enumerate(line_words):
        if len(w) > 1 and not w[0].isalpha():
            w = w[1:]
        if len(w) > 1 and not w[-1].isalpha():
            w = w[0:-1]
        line_words[idx] = w
    words = [w for w in 
                [''.join(filter(lambda c: c.isalpha() or c in "'-", w)) 
                for w in line_words]
                    if len(w) > 0]
    return words
    
with open(file_name) as f:
    front_matter = True
    marker_count = 0
    spell = SpellChecker(distance=1)
    spell.word_frequency.load_words(custom_words)
    for idx, line in enumerate(f):
        if line.strip() == '---' and front_matter == True:
            marker_count += 1
            front_matter = False if marker_count == 2 else True
            continue
        if not front_matter:
            words = get_line_words(line)
            word_count = word_count + len(words)
            misspelled = spell.unknown(words)
            if len(misspelled) > 0:
                print('\n\nFound mispelling:')
                print(f'Context: {words}')
                for word in misspelled:
                    print(f'{word} misspelled on {idx}, candidates are {spell.candidates(word)}')
                    if single_step_mode:
                        c = input("To continue enter 'c', enter 'a' to add word:")
                        if c == 'a':
                            custom_words.add(word)
                            spell.word_frequency.load_words(custom_words)
                    else:
                        custom_words.add(word)

print(f'{word_count} words are in the file, not including front matter')

if add_words:
    print(f'Adding words: {custom_words}')
    try:
        with open('pickle.p', 'wb') as f:
            pickle.dump(custom_words, f)
    except Exception as e:
        print(f'There was an error saving the custom words - {e}.')




