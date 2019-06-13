from Objects import cSymbols as tk
from Algos import cAlgoZero as rb

class cAlgoPrintMD(rb.cAlgoZero):
    def __init__(self, symb, mktID="ROFX"):
        super().__init__(symb, mktID)

    def goRobot(self):
        print("***MD Dict length: ", self.marketDataDict.__len__(), self.getLastMsg())
        tick0Bid=self.contractDetail[self.symbols[0]].getBidPrice()
        tick0Offer=self.contractDetail[self.symbols[0]].getOfferPrice()
        tick0BidSize=self.contractDetail[self.symbols[0]].getBidSize()
        tick0OfferSize = self.contractDetail[self.symbols[0]].getOfferSize()

        tick1Bid = self.contractDetail[self.symbols[1]].getBidPrice()
        tick1Offer = self.contractDetail[self.symbols[1]].getOfferPrice()
        tick1BidSize = self.contractDetail[self.symbols[1]].getBidSize()
        tick1OfferSize = self.contractDetail[self.symbols[1]].getOfferSize()

        print(self.symbols[0], "Bid/Offer: ", tick0Bid ,"/",tick0Offer," ",tick0BidSize,tick0OfferSize)
        print(self.symbols[1], "Bid/Offer: ", tick1Bid ,"/",tick1Offer," ",tick1BidSize,tick1OfferSize)
        print("Pase:", tick1Bid/tick0Offer-1, tick1Offer/tick0Bid-1)

        #print(self.contractDetail[1].getBidPrice())

if __name__ == '__main__':
    ticker1 = "RFX20Jun19"
    ticker2 = "RFX20Sep19"
    #ticker3= "RFX20Jun19 44000c"
    tuple = (ticker1, ticker2)
    md1 = cAlgoPrintMD(tuple, "ROFX")