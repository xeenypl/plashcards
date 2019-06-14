#!/usr/bin/python3
"""plashcards.

Usage:
  plashcards.py list
  plashcards.py remove <deck>
  plashcards.py make <file>
  plashcards.py dump <file>
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
    "wrong-time": 60,
    "good-time" : 600,
    "easy-time" : 86400,
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
    save = {
        "front" : ["front"],
        "back" : ["back"],
        "deck" : deck
    }
    return save

def dumpDeck(fname):
    save = makeDeck(fname)
    f, ext = os.path.splitext(fname)
    open(f + ".pdeck", "w").write(json.dumps(save, sort_keys=True, indent=4))

def listDecks():
    saveFile = os.path.expanduser(config["save-file"])
    try:
        decksSave = json.loads(open(saveFile, "r").read())
        for deck in decksSave:
            print(" %s : %s cards" % (deck, len(decksSave[deck]["deck"])))
    except:
        print("Yuo don't have any deck")
        sys.exit()

def remove(name):
    saveFile = os.path.expanduser(config["save-file"])
    try:
        decksSave = json.loads(open(saveFile, "r").read())
    except:
        print("Yuo don't have any deck")
        sys.exit()
    del decksSave[name]
    open(saveFile, "w").write(json.dumps(decksSave,
        indent=2, separators=(',', ': ')))


def test(name):
    saveFile = os.path.expanduser(config["save-file"])
    try:
        decksSave = json.loads(open(saveFile, "r").read())
    except:
        print("Yuo don't have any deck")
        sys.exit()
    try:
        deckSave = decksSave[name]
    except:
        print("deck %s don't exist" % name)
        sys.exit()
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
            for field in backField:
                print(field + ":", card[field])
            print("a : wrong | s : good | d : easy | q : quit")
            c = readchar.readchar()
            if c == "s":
                deck[i]["waitTime"] = now + config["good-time"]
            elif c == "d":
                deck[i]["waitTime"] = now + config["easy-time"]
            elif c == "q":
                deckSave.update({"deck" : deck})
                decksSave.update({name: deckSave})
                open(saveFile, "w").write(json.dumps(
                    decksSave, indent=2, separators=(',', ': ')))
                sys.exit()
            else:
                deck[i]["waitTime"] = now + config["wrong-time"]
    print("tim for break")
    deckSave.update({"deck" : deck})
    decksSave.update({name: deckSave})
    open(saveFile, "w").write(json.dumps(decksSave,
        indent=2, separators=(',', ': ')))

def add(name, fname):
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
        save.update(decks)
    else:
        f, ext = os.path.splitext(fname)
        try:
            decks = save["decks"]
        except:
            decks = {}
        decks.update({f: deckSave})
        save.update(decks)
    open(saveFile , "w").write(
        json.dumps(save, indent=2, separators=(',', ': ')))

def make(name, fname):
    saveFile = os.path.expanduser(config["save-file"])
    try:
        save = json.loads(open(saveFile, "r").read())
    except:
        save = {}
    deckSave = makeDeck(fname)
    if name is not None:
        try:
            decks = save["decks"]
        except:
            decks = {}
        decks.update({name: deckSave})
        save.update(decks)
    else:
        f, ext = os.path.splitext(fname)
        try:
            decks = save["decks"]
        except:
            decks = {}
        decks.update({f: deckSave})
        save.update(decks)
    open(saveFile , "w").write(
        json.dumps(save, indent=2, separators=(',', ': ')))

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Naval Fate 2.0')
    config = defaultConfig
    if arguments["dump"]:
        dumpDeck(arguments["<file>"])
    elif arguments["make"]:
        make(arguments["<name>"], arguments["<file>"])
    elif arguments["list"]:
        listDecks()
    elif arguments["remove"]:
        remove(arguments["<deck>"])
    elif arguments["test"]:
        test(arguments["<deck>"])
    elif arguments["add"]:
        add(arguments["<name>"], arguments["<deck>"])
