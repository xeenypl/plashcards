"""plashcards.

Usage:
  plashcards.py new <file>
  plashcards.py test <deck>

Options:
  -h --help     Show this screen.

"""
import json
import os
import os.path
import random
from docopt import docopt

configFile = expanduser("~/.config/plashcards/config.json")

def makeDeck(fname):
    deck = []
    lines = open(fname, "r").read().split("\n")
    for line in lines[:-1]:
        sline = line.split("\t")
        deck.append({
            "front"    : sline[0],
            "back"     : sline[1],
            "waitTime" : 0
        })
    f, ext = os.path.splitext(fname)
    save = {
        "front" : ["front"],
        "back" : ["back"],
        "deck" : deck
    }
    open(f + ".pdeck", "w").write(json.dumps(save, sort_keys=True, indent=4))

def test(fname):
    deckSave = json.loads(open(fname, "r").read())
    frontField = deckSave["front"]
    backField = deckSave["back"]
    deck = deckSave["deck"]
    random.shuffle(deck)
    for card in deck:
        for field in frontField:
            print(field + ":", card[field])
        input()
        for field in backField:
            print(field + ":", card[field])

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Naval Fate 2.0')
    try:
        config = open(configFile, "r").read()
        arguments = config.update(arguments)
    except:
        pass
    if arguments["new"]:
        makeDeck(arguments["<file>"])
    if arguments["test"]:
        test(arguments["<deck>"])
