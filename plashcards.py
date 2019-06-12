"""plashcards.

Usage:
  plashcards.py new <file>
  plashcards.py test <deck>
  plashcards.py add <deck> [<name>]

Options:
  -h --help     Show this screen.

"""
import json
import sys
import os
import os.path
import readchar
import random
from datetime import datetime
from docopt import docopt

configFile = os.path.expanduser("~/.config/plashcards/config.json")
defaultConfig = {
    "save-file"	: "~/.plashcards",
    "nknow-time": 60,
    "hard-time" : 600,
    "easy-time" : 86400,
    "nknow-key": "a",
    "hard-key" : "s",
    "easy-key" : "d",
    "quit-key" : "q"
    }


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
    for i in range(len(deck)):
        card = deck[i]
        now = int(datetime.timestamp(datetime.now()))
        if now > card["waitTime"]:
            for field in frontField:
                print(field + ":", card[field])
            c = readchar.readchar()
            if c == config["hard-key"]:
                deck[i]["waitTime"] = now + config["hard-time"]
            elif c == config["easy-key"]:
                deck[i]["waitTime"] = now + config["easy-time"]
            elif c == config["quit-key"]:
                deckSave.update({"deck" : deck})
                open(fname, "w").write(json.dumps(
                    deckSave, indent=2, separators=(',', ': ')))
                sys.exit()
            else:
                deck[i]["waitTime"] = now + config["nknow-time"]
            print(deck[i]["waitTime"], now)
            for field in backField:
                print(field + ":", card[field])
    deckSave.update({"deck" : deck})
    open(fname, "w").write(json.dumps(deckSave, indent=2, separators=(',', ': ')))

def addToSave(name, fname):
    saveFile = os.path.expanduser(config["save-file"])
    try:
        save = json.loads(open(saveFile, "r").read())
    except:
        save = {}
    deckSave = json.loads(open(fname, "r").read())
    if name is not None:
        try:
            decks = save["decks"]
        except:
            decks = {}
        decks.update({name: deckSave})
        save.update({"decks": decks})
    else:
        f, ext = os.path.splitext(fname)
        try:
            decks = save["decks"]
        except:
            decks = {}
        decks.update({f: deckSave})
        save.update({"decks": decks})
    open(saveFile , "w").write(
        json.dumps(save, indent=2, separators=(',', ': ')))



if __name__ == '__main__':
    arguments = docopt(__doc__, version='Naval Fate 2.0')
    config = defaultConfig
    if arguments["new"]:
        makeDeck(arguments["<file>"])
    elif arguments["test"]:
        test(arguments["<deck>"])
    elif arguments["add"]:
        addToSave(arguments["<name>"], arguments["<deck>"])
