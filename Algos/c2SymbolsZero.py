from Algos import cAlgoZero as az


class c2SymbolsZero(az.cAlgoZero):

    def __init__(self, symbols, mktID="ROFX", algoName="2-tickets"):
        super().__init__(symbols,mktID)

        self.symbols = symbols

    def getDaysBetween(self):
        d0 = self.getMaturityDate(self.symbols[0])
        d1 = self.getMaturityDate(self.symbols[1])
        delta=d1-d0
        return delta.days

    def getSpreadRatioOffer(self):
        return self.getOfferPrice(self.symbols[1])/self.getBidPrice(self.symbols[0])

    def getSpreadRatioBid(self):
        return self.getBidPrice(self.symbols[1])/self.getOfferPrice(self.symbols[0])

    def getSpreadBidSize(self):
        bidValue = self.getBidPrice(self.symbols[1]) * self.getBidSize(self.symbols[1]) * self.getContractMultiplier(
            self.symbols[1])
        offerValue=self.getOfferPrice(self.symbols[0])*self.getOfferSize(self.symbols[0])*self.getContractMultiplier(self.symbols[0])

        if bidValue <= offerValue:
            size = int(bidValue/(self.getOfferPrice(self.symbols[0])*self.getContractMultiplier(self.symbols[0])))
        else:
            size = int(offerValue/(self.getBidPrice(self.symbols[1])*self.getContractMultiplier(self.symbols[1])))
        return size

    def getSpreadOfferSize(self):
        offerValue=self.getOfferPrice(self.symbols[1])*self.getOfferSize(self.symbols[1])*self.getContractMultiplier(self.symbols[1])
        bidValue= self.getBidPrice(self.symbols[0])*self.getBidSize(self.symbols[0])*self.getContractMultiplier(self.symbols[0])

        if bidValue <= offerValue:
            size = int(bidValue/(self.getOfferPrice(self.symbols[0])*self.getContractMultiplier(self.symbols[0])))
        else:
            size = int(offerValue / (self.getBidPrice(self.symbols[1]) * self.getContractMultiplier(self.symbols[1])))
        return size

def goRobot(self):
    pass

if __name__ == '__main__':
    t1 = "DOSep19"
    t2 = "RFX20Sep19"
    symbolsTuple = (t1, t2)
    c2S = c2SymbolsZero(tuple)
    print("v7. Algo2s")
    print("Days Between:",c2S.getDaysBetween())

    for t in symbolsTuple:
        print(t, "Bid / Offer", c2S.getBidPrice(t),"/",c2S.getOfferPrice(t), c2S.getBidSize(t),"x",c2S.getOfferSize(t))

    print("Spread ratio mkt:",c2S.getSpreadRatioBid(),"/", c2S.getSpreadRatioOffer(), c2S.getSpreadBidSize(),"x",c2S.getSpreadOfferSize())
