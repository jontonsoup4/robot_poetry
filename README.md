# What is robot_poetry?

`robot_poetry` is comprised of two main classes: `Rhyming` and `RobotPoetry`. `Rhyming` contains functions for finding rhymes and soundex of words. `RobotPoetry` writes poems based on given text.

# Example script
```
from robot_poetry import RobotPoetry,

text = RobotPoetry('texts/hamlet.txt')
print(text.write_quad())
```

## Output
```
Or pour plausive but physic else forgone supply
Dislike deserved quality, who any stated scratch keeps attribute
Polonius, however thou understand both trust, army rely
Yourself hide pastime on labour body sir pale methinks countersuit

Forty its combination, armour stream, them sweet honesty
Yourself 'twill do this proof tune
Him you dispatch whereof dalgety
Materials yet errors faith curse sleeping huntoon
```

# Setup
`python3 setup.py install`

# Dependencies
`nltk>=3.0.5`

# Complete list of functions
```

# defining two words and a sentence
word1 = 'snow'
word2 = 'blow'
sentence = 'I know that I like to blow snow'


"""Rhyming class"""
rhymes = Rhyming()

# returns a boolean for if two words rhyme
rhymes.does_it_rhyme(word1, word2)

# returns a dictionary with all rhymes in the text
rhymes.rhymes(sentence)

# returns a list of list with words in the text that rhyme together
rhymes.rhymes_in_text(sentence)

# returns soundex value of word
rhymes.soundex(word1)

# returns a soundex value of each word in a text
rhymes.soundex_multi(sentence)


"""Poetry class"""
poetry = RobotPoetry('shakespeare.txt')

# [[word1, [rhyme_words1]], [word2, [rhyme_words2]]]
poetry.random_rhyme(2)

# Experimental search of words within the text that rhyme. Really slow currently
poetry.rhymes_in_text()

# Force updates the pickles.
poetry.update()

# Writes a line using source text
poetry.write_line()

# Writes several lines using source text. Does not rhyme
poetry.write_lines()

# Writes an ABAB poem based on source text
poetry.write_quad()
```