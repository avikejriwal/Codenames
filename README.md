This is my implementation of a bot for playing the role of Spymaster in Codenames, the word association game.

The current bot uses a pretrained word2vec model to generate clues based on words contextually similar to words on the game board.

#### Files/Directories

`main.py`: runs the game  
`game.py`: contains core game code  
`agents/`: contains the scripts implementing the Spymaster AI for the game  
`models/`: store the word2vec embedding file(s) (not included; can download a copy [here](https://code.google.com/archive/p/word2vec/))  
`words.txt`: words used in the game are sampled from this file

#### Key Modules:
`gensim`  
`nltk`
