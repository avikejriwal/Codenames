import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from game import Game
from agents.proto_agent import Proto_Agent

with open('words.txt', 'r') as f:
    words = [i.strip('\n').lower() for i in f.readlines()]

game = Game(words, Proto_Agent)
