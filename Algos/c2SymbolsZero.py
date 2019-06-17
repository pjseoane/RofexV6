from Algos import cAlgoZero as az


class c2SymbolsZero(az.cAlgoZero):

    def __init__(self, symbols, mktID="ROFX", algoName="2-tickets"):
        super().__init__(symbols, mktID, algoName)

        #self.symbols = symbols


    def printLine(self, ticker):
        print(ticker, "Bid / Offer", self.getBidPrice(ticker), "/", self.getOfferPrice(ticker), self.getBidSize(ticker), "x",
              self.getOfferSize(ticker))

    def getDaysBetween(self):
        d0 = self.getMaturityDate(self.symbols[0])
        d1 = self.getMaturityDate(self.symbols[1])
        delta=d1-d0
        return delta.days

    def getSpreadRatioOffer(self):
        try:
            return self.getOfferPrice(self.symbols[1])/self.getBidPrice(self.symbols[0])
        except:
            return 0

    def getPaseOffer(self):
        return self.getSpreadRatioOffer()*1/self.getDaysBetween() * 365

    def getPaseBid(self):
        return self.getSpreadRatioBid() * 1 / self.getDaysBetween() * 365

    def getSpreadRatioBid(self):
        try:
            return self.getBidPrice(self.symbols[1])/self.getOfferPrice(self.symbols[0])
        except:
            return 0

    def getSpreadBidSize(self):
        try:
            bidValue = self.getBidPrice(self.symbols[1]) * self.getBidSize(self.symbols[1]) * self.getContractMultiplier(
            self.symbols[1])
            offerValue=self.getOfferPrice(self.symbols[0])*self.getOfferSize(self.symbols[0])*self.getContractMultiplier(self.symbols[0])

            if bidValue <= offerValue:
                size = int(bidValue/(self.getOfferPrice(self.symbols[0])*self.getContractMultiplier(self.symbols[0])))
            else:
                size = int(offerValue/(self.getBidPrice(self.symbols[1])*self.getContractMultiplier(self.symbols[1])))
            return size
        except:
            return 0

    def getSpreadOfferSize(self):
        try:
            offerValue=self.getOfferPrice(self.symbols[1])*self.getOfferSize(self.symbols[1])*self.getContractMultiplier(self.symbols[1])
            bidValue= self.getBidPrice(self.symbols[0])*self.getBidSize(self.symbols[0])*self.getContractMultiplier(self.symbols[0])

            if bidValue <= offerValue:
                size = int(bidValue/(self.getOfferPrice(self.symbols[0])*self.getContractMultiplier(self.symbols[0])))
            else:
                size = int(offerValue / (self.getBidPrice(self.symbols[1]) * self.getContractMultiplier(self.symbols[1])))
            return size
        except:
            return 0

    def goRobot(self):
        print(self.algoName)
        print ("Days Between:", self.getDaysBetween() )
        for t in self.symbols:
            self.printLine(t)


if __name__ == '__main__':
    t1 = "DOSep19"
    t2 = "RFX20Sep19"
    symbolsTuple = (t1, t2)
    c2S = c2SymbolsZero(symbolsTuple,"ROFX","c2SymbolsZ")

    print("Spread ratio mkt:",c2S.getSpreadRatioBid(),"/", c2S.getSpreadRatioOffer(), c2S.getSpreadBidSize(),"x",c2S.getSpreadOfferSize())
