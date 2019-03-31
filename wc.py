
#
# todo:
# add context around spelling areas
# file with words to add to dictionary
# better output formatting
# "testing"
#

import sys
from spellchecker import SpellChecker

if len(sys.argv) != 2:
    print('Please provide a file name!')
    exit(1)

fn = sys.argv[1]
wc = 0
 
with open(fn) as f:
    front_matter = True
    marker_count = 0
    spell = SpellChecker(distance=1)
    for idx, line in enumerate(f):
        if line.strip() == '---' and front_matter == True:
            marker_count += 1
            front_matter = False if marker_count == 2 else True
            continue
        if not front_matter:
            wc = wc + len(line.split())
            misspelled = spell.unknown([w for w in 
                                        [''.join(filter(lambda c: c.isalpha() or c == "'", w)) 
                                         for w in line.split()]
                                         if len(w) > 0])
            if len(misspelled) > 0:
                for word in misspelled:
                    print(f'{word} misspelled on {idx}, candidates are {spell.candidates(word)}')

print(f'{wc} words are in the file, not including front matter')




