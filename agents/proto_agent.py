from gensim.models import KeyedVectors
from nltk.stem.wordnet import WordNetLemmatizer
import os

from collections import defaultdict

class Proto_Agent:

    def __init__(self, game_board):

        path = os.getcwd() + '\\models\\GoogleNews-vectors-negative300.bin'
        # Load Google's pretrained word2vec model
        self.vec_model = KeyedVectors.load_word2vec_format(path, binary=True, limit=500000)

        self.board = game_board
        self.past_clues = []

    def generate_clue(self, codenames):
        options = self.get_neighbors(codenames)

        clue = options[0]

        i = 0
        
        #try to give different clues each time
        while clue in self.past_clues and i < len(options):
            i += 1
            clue = options[i]
        self.past_clues.append(clue)

        return clue

    # Compute codename similar words individually, then consolidate the lists to get suggestions
    def get_neighbors(self, codenames, n_words=15):
        candidate_words = []

        # get neighbors for individual words
        for word in codenames:
            try:
                neighbors = self.vec_model.most_similar(positive=[word], topn=n_words)
                # neighbors = vec_model.most_similar_cosmul(positive=[word], topn = 20)
                # neighbors = vec_model.similar_by_word(word, topn = 10)
                neighbors = self.parse_suggestions(neighbors)
                candidate_words.extend(neighbors)
            except KeyError:
                pass

        # Consolidate neighboring words to get counts
        options = defaultdict(int)
        for result in candidate_words:
            options[result[0]] += 1

        return list(sorted(options.items(), key = lambda x: x[1], reverse=True))

    # Parse neighbors to get game-legal suggestions
    def parse_suggestions(self, neighbors):
        chars = list('@ _.#')
        wordnet = WordNetLemmatizer()

        neighbors = list(filter(lambda x: all(cha not in x[0] for cha in chars) and (len(x[0]) > 2), neighbors))
        neighbors = list(map(lambda x: (wordnet.lemmatize(x[0].lower(), pos='n'), x[1]), neighbors))
        # Can't give a clue that's the same as or part of a word in the game; remove "illegal" clues
        neighbors = list(filter(lambda x: all((x[0] not in i) and (i not in x[0]) for i in self.board), neighbors))

        return list(set(neighbors)) # remove redundancies
