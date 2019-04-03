
#
# todo:
# add context around spelling areas
# file with words to add to dictionary
# better output formatting
# how to handle hyphenated words
# "testing"
#

import sys
import pickle
from spellchecker import SpellChecker

if len(sys.argv) < 2:
    print('Please provide a file name!')
    exit(1)

if len(sys.argv) == 3:
    add_words = bool(sys.argv[2])
else:
    add_words = False

file_name = sys.argv[1]
word_count = 0
custom_words = set()

try:
    with open('pickle.p', 'rb') as f:
        custom_words = pickle.load(f)
except Exception as e:
    print(f'Error loading custom dictionary words! {e}')

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
            line_words = line.split()
            word_count = word_count + len(line_words)
            words = [w for w in 
                        [''.join(filter(lambda c: c.isalpha() or c == "'" or c == "-", w)) 
                        for w in line_words]
                            if len(w) > 0]
            misspelled = spell.unknown(words)
            if len(misspelled) > 0:
                print('\n\nFound mispelling:')
                print(f'Context: {words}')
                for word in misspelled:
                    custom_words.add(word)
                    print(f'{word} misspelled on {idx}, candidates are {spell.candidates(word)}')

print(f'{wc} words are in the file, not including front matter')

if add_words:
    print(f'Adding words: {custom_words}')
    try:
        with open('pickle.p', 'wb') as f:
            pickle.dump(custom_words, f)
    except Exception as e:
        print(f'There was an error saving the custom words - {e}.')




