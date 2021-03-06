
## All the Import Boilerplate goes Here.

import random

import pprint

import pygame

import time

import sys

from pygame.locals import *

## CARD VALUES AND SUITS ##

CARD_VALUES = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]

CARD_VALUE_DICT = {
    "A" : "Ace",
    "2" : "Two",
    "3" : "Three",
    "4" : "Four",
    "5" : "Five",
    "6" : "Six",
    "7" : "Seven",
    "8" : "Eight",
    "9" : "Nine",
    "T": "Ten",
    "J" : "Jack",
    "Q" : "Queen",
    "K" : "King"
    }

CARD_SUIT_DICT = {
    "C" : "Clubs",
    "H" : "Hearts",
    "S" : "Spades",
    "D" : "Diamonds"
    }

## ORDER CONSTANTS

CHASED_SUITS = ["C", "H", "S", "D"]  ## The "Chased Order."
SHOCKED_SUITS = ["S", "H", "C", "D"] ## The "Shocked Order."
NDO_SUITS = ["H", "C", "D", "S"] ## New Deck Order. Bicycle suit order from out of the box.

## DECK CONSTANTS

MEMORANDUM = "JS7CTHAD4C7H4DAS4H7D4SAHTD7SJCKDTS8CJHACKS5C8H3DQSKH9CQH6C9H2D3C6H5D2S3H8D5SKCJD8STC2C5H6D3S2H9D6SQCQD9S"

class Card(object):
    def __init__(self,card_index):
        self.value = card_index[0]
        self.suit = card_index[1]
        self.image = pygame.transform.scale(pygame.image.load("card_images/"+CARD_VALUE_DICT[card_index[0]]+"of"+CARD_SUIT_DICT[card_index[1]]+".png"), (87,122))

    def __str__(self):
        return self.value+self.suit

class Deck(object):
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)

    def make_new_deck(self):
        ## Makes a deck in NDO
        top_half, bottom_half = self.cut_the(self.make_a_deck_in(NDO_SUITS))
        ## Reverse the bottom half, so we see the ace of spades. AK AK KA KA
        new_deck = top_half + bottom_half[0:13][::-1] + bottom_half[13:26][::-1]
        self.construct_deck(new_deck)

    def make_a_deck_in(self,suit_order):
        ## Makes a deck in a specific suit order, AK AK AK AK
        return [value+suit for suit in suit_order for value in CARD_VALUES]

    def construct_deck(self,card_indexes):
        for card_index in card_indexes:
            card = Card(card_index)
            self.add_card(card)
            
    def create_deck_from(self,deck_order):
        self.clear()
        self.construct_deck([deck_order[i:i+2] for i in range(0, len(deck_order), 2)])

    def return_deckstring(self):
        deck_order = ""
        for card in self.cards:
            deck_order+=str(card)
        return deck_order

    def mirror(self):
        ## Works on a deck in NDO
        ## Cuts the 13 Clubs cards to the top of the deck
        self.cards = self.cards[13:26] + self.cards[0:13] + self.cards[26:52]

    def print_me(self):
        pretty_deck = []
        for index, card in enumerate(self.cards):
            new_card = list(card)
            expanded_value = CARD_VALUE_DICT[new_card[0]]
            expanded_suit = CARD_SUIT_DICT[new_card[1]]
            pretty_deck.append(expanded_value+" of "+expanded_suit)
        return pretty_deck

    def memorandum(self):
        ## Returns a deck in Memorandum Stack.
        ## For now, it returns a standard faro 4 deck without the adjustment.
        self.clear()
        self.make_new_deck()
        self.mirror()
        self.out_faro(4)
        self.cards = self.cards[1:12]+[self.cards[0]]+self.cards[12:]
        self.cards = self.cards[44:]+self.cards[0:44]
        self.cards = self.cards[0:34]+[self.cards[51]]+self.cards[34:51]
        self.cards = self.cards[0:24]+self.cards[34:]+self.cards[24:34]
        self.cards = self.cards[0:24]+[self.cards[27]]+self.cards[24:27]+self.cards[28:]

    def clear(self):
        self.cards = []

    def cut_the(self,deck):
        top_half = len(deck)/2
        return deck[:top_half], deck[top_half:]

    def out_faro(self,faro_number):
        for shuffles in range(faro_number):
            flatten = lambda l: [i for s in l for i in s]
            ## A shuffle that cuts the deck in half and performs an out faro,
            ## This leaves the Ace of spades on bottom and Ace of Clubs on top.
            self.cards = flatten([[x, y] for x, y in zip(*self.cut_the(self.cards))])

    def anti_faro(self,antifaro_number):
        for shuffles in range(antifaro_number):
            top_half = []
            bottom_half = []
            for i in range(0,len(self.cards),2):
                top_half.append(self.cards[i])
                bottom_half.append(self.cards[i+1])
            self.cards = top_half + bottom_half
        
    def spit_it_out(self):
        print self.print_me()

    def shuffle(self):
        random.shuffle(self.cards)


## PROGRAM MAIN LOOP ##

showtime = True
pygame.init()

if __name__ == "__main__":
    ## Begin Screen Setup
    screen=pygame.display.set_mode((1024,768),HWSURFACE|DOUBLEBUF|RESIZABLE)
    
    background=pygame.image.load("backgrounds/example.png")#You need an example picture in the same folder as this file!
   
    screen.blit(pygame.transform.scale(background,(1024,768)),(0,0))

    pygame.display.flip()

    ## Prepare the Deck

    deck = Deck()
    deck.make_new_deck()
    deck.mirror()
    deck.anti_faro(4)
    
##    deck.memorandum()
##
##    example_deck = Deck()
##    example_deck.create_deck_from(MEMORANDUM)
##
##    deck_order = deck.return_deckstring()
##    example_deck_order = example_deck.return_deckstring()
##
##    if deck_order == example_deck_order:
##        print "The decks perfectly match!"
##    else:
##        print deck_order
##        print example_deck_order

    while showtime == True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print ("""
                    Escape Key Detected. Quitting the App.
                    """)
                    pygame.quit()
                    sys.exit()
            elif event.type==QUIT: pygame.display.quit()
            elif event.type==VIDEORESIZE:
                screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                screen.blit(pygame.transform.scale(background,event.dict['size']),(0,0))
            horizontal_adjustment = 85
            for card in deck.cards:
                screen.blit(card.image, (horizontal_adjustment,200))
                horizontal_adjustment+=15
##            horizontal_adjustment = 85
##            for card in example_deck.cards:
##                screen.blit(card.image, (horizontal_adjustment,400))
##                horizontal_adjustment+=15
        pygame.display.flip()
        time.sleep(0.03) #Frame limiter at 30 milliseconds
    pygame.quit()


