"""plashcards.

Usage:
  plashcards.py new <file>
  plashcards.py test <deck>

Options:
  -h --help     Show this screen.

"""
import json
import os
import random
from docopt import docopt

def makeDeck(fname):
    deck = []
    lines = open(fname, "r").read().split("\n")
    for line in lines[:-1]:
        sline = line.split("\t")
        deck.append({
            "front" : sline[0],
            "back"  : sline[1]
        })
    f, ext = os.path.splitext(fname)
    save = {
        "front" : ["front"]
        "back" : ["back"]
        "deck" : deck
    }
    open(f + ".pdeck", "w").write(json.dumps(deck, sort_keys=True, indent=4))

def test(fname):
    deckSave = json.loads(open(fname, "r").read())
    front = deckSave["front"]
    back = deckSave["back"]
    deck = deckSave["deck"]
    random.shuffle(deck)
    for card in deck:
        print("front:", card["front"])
        input()
        print("back: ", card["back"])

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Naval Fate 2.0')
    print(arguments)
    if arguments["new"]:
        makeDeck(arguments["<file>"])
    if arguments["test"]:
        test(arguments["<deck>"])
