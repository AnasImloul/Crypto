# Import libraries
import json
import requests

from time import sleep
from ClockDate import todayDate, clockTime
from time import time
from files import *


class Crypto:
    def __init__(self):
        # defining key/request url        
        key = "https://api.binance.com/api/v3/ticker/price?"
        self.key = key
        self.prices = dict()
        self.lastDateModification = dict()
        self.timeStep = 60

        self.defaultSymbols = ["BTCTUSD", "ETHTUSD", "BNBTUSD"]
        self.symbols = set()

    def getSymbols(self, path):

        try:
            file = open(path + "symbols.txt", "r")
            lines = file.read().split("\n")
            file.close()
            self.symbols = set(lines)

        except:
            file = open(path + "symbols.txt", "a")
            file.write("\n".join(self.defaultSymbols))
            file.close()
            self.symbols = set(self.defaultSymbols)

    def getAllExchangeRates(self):
        symbols = []
        try:
            # requesting data from url
            data = requests.get(self.key)
            data = data.json()

            return data

        except:
            return

    def start(self, path, symbol):

        if symbol not in self.symbols:
            return

        try:
            # open file for reading
            open(path + "data/" + symbol + ".txt", "r").close()
        except:
            # create file if it doesn't exist
            open(path + "data/" + symbol + ".txt", "a").close()

        # read file content
        file = open(path + "data/" + symbol + ".txt", "r")
        lines = file.read().split("\n")
        file.close()

        lastPrice, lastDate = getLastPrice(lines), getLastDate(lines)
        self.prices[symbol] = lastPrice
        self.lastDateModification[symbol] = lastDate

    def write(self, path, symbol, price):

        if symbol not in self.symbols:
            return

            # get today date
        date = todayDate()

        # get clockTime
        clock = clockTime()

        if symbol not in self.prices:
            self.start(path, symbol)

        try:
            # open file for reading
            open(path + "data/" + symbol + ".txt", "r").close()
        except:
            # if file doesn't exist start from beginning
            self.start(path, symbol)

        # don't do anything if price didn't changed from last modification
        if self.timeStep == 0 and self.prices[symbol] == price:
            return

        # open file for writing
        file = open(path + "data/" + symbol + ".txt", "a")

        # don't write date if it hasn't changed yet
        if date != self.lastDateModification[symbol]:
            file.write(date + "\n")
            self.lastDateModification[symbol] = date

        # write clockTime and price to the text file
        file.write(clock + " " + str(round(price, 12)) + "\n")
        self.prices[symbol] = price

        # close file
        file.close()

        return

    def save(self, path):

        while True:

            start = time()

            coins = self.getAllExchangeRates()

            while coins == None:
                coins = self.getAllExchangeRates()

            self.getSymbols(path)

            for coin in coins:
                symbol, price = coin["symbol"], float(coin["price"])

                self.write(path, symbol, price)

            dt = time() - start
            try:
                sleep(max((self.timeStep - dt), 0))
            except:
                continue