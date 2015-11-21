import pickle
import nltk
import random
import re
import os
from collections import defaultdict
from string import punctuation, printable


class Rhyming:
    FAR_RHYMES = 1
    NEAR_RHYMES = 2
    CLOSE_RHYMES = 3
    SOUNDEX_DIGITS = '01230120022455012623010202'

    def __init__(self):
        """
        Used to find rhymes within short text or words
        """
        self.entries = pickle.load(open(os.path.dirname(__file__) + '/data/entries.pickle', 'rb'))

    @staticmethod
    def clean(t):
        """
        :param t: text
        :return: text without punctuation
        """
        for i in punctuation:
            if i == '\'':
                pass
            else:
                t = t.replace(i, '')
        return t

    def does_it_rhyme(self, word1, word2):
        """
        :param word1: primary word
        :param word2: word to check against word1
        :return: boolean for if word1 and word2 rhyme
        """
        word1 = self.words_that_rhyme_with(word1, Rhyming.FAR_RHYMES)
        return word2 in word1

    def rhymes(self, body, sim=NEAR_RHYMES):
        """
        :param body: text to be checked
        :param sim: similarity [1 (far) - 3 (close)]
        :return: dictionary with all rhymes in the body
        """
        body = self.clean(body).lower().split()
        rhymes = {}
        for word in body:
            if word not in rhymes.keys() and len(word) < 15:
                print("checking '{}'".format(word))
                rhymes[word] = self.words_that_rhyme_with(word, sim)
        print()
        return rhymes

    def rhymes_in_text(self, text, sim=NEAR_RHYMES):
        """
        :param text: text to check
        :param sim: similarity [1 (far) - 3 (close)]
        :return: list of lists. In each list is a couplet of words from the text that rhyme together
        """
        sen = self.rhymes(text, sim)
        comb = [sorted([w, val]) for w in sen.keys() for val in sen.keys() if w in sen[val] and w != val]
        output = []
        for i in comb:
            if i not in output:
                output.append(i)
        return output

    @staticmethod
    def soundex(word, length=4):
        """
        :param word: single word to be indexed
        :param length: length of index to output
        :return: soundex index of given word
        """
        soundex_index = ''
        first_character = ''
        for character in word.upper():
            if character.isalpha():
                if not first_character:
                    first_character = character
                d = Rhyming.SOUNDEX_DIGITS[ord(character) - ord('A')]
                if not soundex_index or (d != soundex_index[-1]):
                    soundex_index += d
        soundex_index = (first_character + soundex_index[1:]).replace('0', '')
        return (soundex_index + (length * '0'))[:length]

    def soundex_multi(self, words, length=4):
        """
        :param words: sentence to be indexed
        :param length: length of each index to output
        :return: string of soundex indexes from the given sentence
        """
        words = self.clean(words).split()
        soundex_indexes = []
        for word in words:
            soundex_indexes.append(self.soundex(word, length))
        return ' '.join(soundex_indexes)

    def words_that_rhyme_with(self, check_word, sim=NEAR_RHYMES):
        """
        :param check_word: word to check rhymes of
        :param sim: similarity [1 (far) - 3 (close)]
        :return: list of words that rhyme with given word
        """
        syllables = [(word, syl) for word, syl in self.entries if word == check_word.lower()]
        rhymes = []
        for (word, syllable) in syllables:
            rhymes += [word for word, pro in self.entries if pro[-sim:] == syllable[-sim:] and check_word != word]
        return sorted(set(rhymes))


class RobotPoetry:
    def __init__(self, file_path):
        """
        Used write poetry using text documents
        :param file_path: path to text file
        """
        self.file_path = file_path
        self.file_name = self.file_path.split('.')[0].split('/')[-1]
        self.rhyming = Rhyming()
        self.punctuation = punctuation
        try:
            open(file_path)
        except FileNotFoundError:
            print('Incorrect file path \nExiting...')
            exit()
        if not os.path.exists('rhyming_data/{}'.format(self.file_name)):
            os.makedirs('rhyming_data/{}'.format(self.file_name))
        try:
            self._load_from_pickle()
        except FileNotFoundError:
            self._save_to_pickle()
            self._load_from_pickle()

    def _build_line(self, max_line_length=10, show_form=False):
        return self.write_line(max_line_length, show_form).split()[:-1]

    def _load_from_pickle(self):
        self.word_dict = pickle.load(
            open('rhyming_data/{0}/{0}_words.pickle'.format(self.file_name), "rb"))
        self.line_form = pickle.load(
            open('rhyming_data/{0}/{0}_form.pickle'.format(self.file_name), "rb"))
        self.words_in_text = []
        for x in self.word_dict.values():
            for y in x:
                self.words_in_text.append(y)

    def _save_to_pickle(self):
        print('Preparing to write pickles...')
        safe = '\'\".,?!-'
        pun = ''.join(filter(lambda x: x not in safe, self.punctuation))
        sample = ''.join(filter(lambda x: x in printable, open(self.file_path).read())).strip()
        sample = re.sub(r'\s+', ' ', ''.join(filter(lambda x: x not in pun, sample))).lower()
        tokenized = nltk.sent_tokenize(sample)
        self.word_dict = defaultdict(list)
        self.line_form = []
        sent = 0
        for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            line = []
            for word in tagged:
                if word[0] not in self.word_dict[word[1]]:
                    self.word_dict[word[1]].append(word[0])
                line.append(word[1])
            if line not in self.line_form:
                self.line_form.append(line)
            sent += 1
            if sent % 10 == 0 or sent == len(tokenized):
                print(sent, ':', len(tokenized))
        print('*** Finished pickles ***\n')
        with open('rhyming_data/{0}/{0}_words.pickle'.format(self.file_name), "wb") as f:
            pickle.dump(self.word_dict, f)
        with open('rhyming_data/{0}/{0}_form.pickle'.format(self.file_name), "wb") as g:
            pickle.dump(self.line_form, g)

    def random_rhyme(self, num_rhymes=1, sim=Rhyming.NEAR_RHYMES):
        """
        :param num_rhymes: The desired number of results
        :param sim: similarity [1 (far) - 3 (close)]
        :return: [[word1, [rhyme_words1]], [word2, [rhyme_words2]]]
        """
        counter = 0
        rhymes = []
        while counter < num_rhymes:
            word = random.choice(self.words_in_text)
            words_that_rhyme = self.rhyming.words_that_rhyme_with(word, sim)
            length = len(words_that_rhyme)
            if length > 1:
                rhymes.append([word, words_that_rhyme])
                counter += 1
            else:
                continue
        return rhymes

    def rhymes_in_text(self):
        """
        WARNING: really slow process
        :return: list of lists of words within the text that rhyme together
        """
        print('WARNING: really slow process')
        return self.rhyming.rhymes_in_text(' '.join(self.words_in_text))

    def update(self):
        """
        Force update of the pickles
        :return: Poetry init
        """
        self._save_to_pickle()
        return RobotPoetry(self.file_path)

    def write_line(self, max_line_length=10, show_form=False):
        """
        :param max_line_length: maximum words in the line
        :param show_form: prints a readout of the form
        :return: string containing a sentence built from a random form based on the text
        """
        form = random.choice(self.line_form)
        if show_form:
            print(form[:max_line_length])
        sentence = [random.choice(self.word_dict[word]) for word in form][:max_line_length]
        sentence = re.sub(r'\s([.,?!;\'()/"](?:\s|$))', r'\1', ' '.join(sentence)).capitalize()
        if sentence[-1] not in punctuation:
            sentence += '.'
        return sentence

    def write_lines(self, num_lines=1, max_line_length=10, show_form=False):
        """
        :param max_line_length: maximum words in the line
        :param num_lines: number of lines to write
        :param show_form: prints a readout of the form
        :return: write_line() strings combined with \n
        """
        sentences = [self.write_line(max_line_length, show_form) for _ in range(num_lines)]
        return '\n'.join(sentences)

    def write_quad(self, num_quads=1, max_line_length=10, limiter='\n', show_form=False):
        """
        :param num_quads: number of desired quads to output
        :param max_line_length: determines max number of words in a line
        :param limiter: determines what is between the quads
        :param show_form: prints a readout of the form
        :return: ABAB poem based on text
        """
        sentences = []
        for _ in range(num_quads):
            rhyme1, rhyme2 = self.random_rhyme(2)
            sentence1 = ' '.join(self._build_line(max_line_length, show_form) + [rhyme1[0]])
            sentence2 = ' '.join(self._build_line(max_line_length, show_form) + [rhyme2[0]])
            sentence3 = ' '.join(self._build_line(max_line_length, show_form) + [random.choice(rhyme1[1])])
            sentence4 = ' '.join(self._build_line(max_line_length, show_form) + [random.choice(rhyme2[1])])
            sentences.append(
                '{0}\n{1}\n{2}\n{3}\n'.format(sentence1.capitalize(), sentence2.capitalize(), sentence3.capitalize(),
                                              sentence4.capitalize()))
        return limiter.join(sentences)
