from os.path import isfile
from os import system
from requests import get
from time import sleep
import numpy as np
from datetime import datetime

class ShitcoinTracker:
    #def __init__(self, settingsPath, cryptoPath):
       # pancakeswapURL = "https://api.pancakeswap.info/api/v2/tokens/"
    
    def checkFiles(self):
        if (isfile("./settings.txt") == False):
            with open("./settings.txt", "w") as fileSettings:
                #fileSettings.write("path=./cryptoshitcoins.csv\nrefreshRate=60\nmultiplier=2")
                fileSettings.write("refreshRate=60\nmultiplier=2")
        if (isfile("./cryptoshitcoins.csv") == False):
            cryptoFile = np.array(["Token Contract", "BNB Cost", "Number of Tokens"])
            cryptoFile.tofile("./cryptoshitcoins.csv", sep=",")
    
    def openSettings(self):
        with open("./settings.txt", "r") as fileSettings:
            settings = fileSettings.readlines()
        #cryptoPath = settings[0][5:].replace("\n", "")
        refreshRate = settings[1][12:].replace("\n", "")
        multiplier = settings[2][11:].replace("\n", "")
        
        return (refreshRate, multiplier)


    def dataCalculation(self, multiplier):
        data = np.loadtxt("./cryptoshitcoins.csv", delimiter=",", skiprows=1, usecols=(1,2))
        calculated = np.full_like(data, 0)      #col 0 is breakeven, col 1 is multiplier price
        multiplier = float(multiplier)
        for i in range(0, np.shape(calculated)[0]):
            breakEvenValue = data[i][0]/data[i][1]
            multiplierSell = breakEvenValue*multiplier
            calculated[i] = np.array([breakEvenValue, multiplierSell])
        self.updateScreen(calculated)
    
    def updateScreen(self, calculated):
        system("cls")
        tokenArray = np.loadtxt("./cryptoshitcoins.csv", delimiter=",", skiprows=1, usecols=0, dtype="str")

        for i in range(0, np.shape(tokenArray)[0]):    # For some reason numpy loads the string with quotation marks so remove them
            tokenArray[i] = tokenArray[i].strip("\'")
        
        print("Last updated: " + str(datetime.now())[:-7])
        print( "Ticker      | Breakeven  | Multiplied | Current price | Status")
        
        for row in range(0,np.shape(calculated)[0]): 
            jsonFile = get("https://api.pancakeswap.info/api/v2/tokens/"+tokenArray[row]).json()["data"]
            x=calculated[row][0]
            y=calculated[row][1]
            ticker=jsonFile["symbol"].ljust(11," ")
            z = float(jsonFile["price_BNB"])
            
            if (z < x):
                status = "Loss" 
            elif (z > x and z < y):
                status = "Profit"
            else:
                status = "Sell initial"
            
            print(f"{ticker} | {x:.4E} | {y:.4E} | {z:.4E}    | {status}")

ShitcoinTracker().checkFiles()
(refreshRate, multiplier) = ShitcoinTracker().openSettings()
refreshRate = int(refreshRate)

while True:
    ShitcoinTracker().dataCalculation(multiplier)
    sleep(refreshRate)