import numpy as np
from agents.proto_agent import Proto_Agent
#import pdb
import copy

class Game:

    def __init__(self, words, agent):
        def get_game_words(words):
            game_words = np.random.choice(words, replace=False, size=25)
            game_words = [i.replace('-', ' ').replace('_', '') for i in game_words]
            return game_words

        game_words = get_game_words(words)
        self.board = game_words
        self.blue = copy.copy(game_words[:9])
        self.red = copy.copy(game_words[9:17])
        self.neutral = copy.copy(game_words[17:24])
        self.assassin = copy.copy([game_words[24]])

        self.player = np.random.choice(['blue','red'])

        self.spymaster = agent(self.board)

        if self.player == 'blue':
            self.turn_toggle = True
        else:
            self.turn_toggle = False

        np.random.shuffle(self.board)
        return

    #executes the game
    def execute(self):
        print('Let\'s play Codenames')
        print('Your color is: ' + self.player)
        print('the board is:')

        self.show_board()
        while self.blue and self.red and self.assassin:
            if self.turn_toggle:
                print('It\'s your turn; type \"PASS\" to end your turn.')
                self.show_board()
                self.turn()
            else:
                print('It\'s the computer\'s turn:')
                self.opp_turn()
                print('the computer has gone.')

            self.turn_toggle = not self.turn_toggle

        if not self.red:
            print('Red identified all their agents!! They win!!')
        elif not self.blue:
            print('Blue identified all their agents!! They win!!')
        else:
            print('Assassin!! Game over!  ', end = '')
            if self.turn_toggle:
                print('You win!!')
            else:
                print('Computer wins!')
        self.show_board()

    #shows the game board as a 5x5 grid
    def show_board(self):
        print()
        for j in range(0, 25, 5):
            for i in range(5):
                form_string = '{: ^' + str((i+2)*5) + 's}'
                print(form_string.format(self.board[j+i]), end="")
            print()
        print()
        return

    #execute a full turn for the player
    def turn(self):
        print('Spymaster is generating a clue...')
        if self.player == 'blue':
            clue = self.spymaster.generate_clue(self.blue)
        else:
            clue = self.spymaster.generate_clue(self.red)
        print("Your clue is: " + clue[0] + ', ' + str(clue[1]))

        num_guesses = clue[1] + 1
        end = False
        i = 0
        word = ''

        while i < num_guesses and not end and word != 'PASS':
            word = self.guess()
            if word == 'PASS':
                return
            if (word not in self.blue and self.player == 'blue') or (word not in self.red and self.player=='red'):
                print('Your guess was incorrect.  Your turn is over.')
                print()
                end = True
            else:
                print('Correct. You have ' + str(num_guesses-i-1) + ' more guess(es).')
            self.remove_word(word)
            i += 1
        return

    #query a guess from the user
    def guess(self):
        query = input('Guess a word: ')
        if query == 'PASS':
            return query
        while query not in self.board:
            query = input('error: query not in game board. Try again: ')
        return query

    #choose words for the opponent
    def opp_turn(self):
        num = np.random.choice([0,1,2,3], p=[0.2, 0.6, 0.1, 0.1])
        if num == 0:
            self.remove_word(np.random.choice(self.neutral + self.assassin))
        elif self.player == 'blue':
            for w in np.random.choice(self.red, size=min(num, len(self.red)), replace=False):
                self.remove_word(w)
        elif self.player == 'red':
            for w in np.random.choice(self.blue, size=min(num, len(self.blue)), replace=False):
                self.remove_word(w)

    #removes a word from the game once it's guessed
    def remove_word(self, word):
        if word in self.blue:
            self.board = [i if i != word else 'BLUE' for i in self.board]
            self.blue.remove(word)
        elif word in self.red:
            self.board = [i if i != word else 'RED' for i in self.board]
            self.red.remove(word)
        elif word in self.neutral:
            self.board = [i if i != word else 'NEUTRAL' for i in self.board]
            self.neutral.remove(word)
        elif word in self.assassin:
            self.board = [i if i != word else 'ASSASSIN' for i in self.board]
            self.assassin.remove(word)
        return
