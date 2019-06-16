
from Algos import c2SymbolsZero as a2


class c2SymbolsPase(a2.c2SymbolsZero):
    def __init__(self, symbols, mktID="ROFX",algoName="V7. 2SymbolsPase"):

        super().__init__(symbols, mktID, algoName)

    # def paseCalc(self):
    #     try:
    #         days = self.getDaysBetween()
    #         if self.getOfferPrice(self.symbols[0]) > 0:
    #             self.paseBid=(self.getBidPrice(self.symbols[1])/self.getOfferPrice(self.symbols[0])-1)/days*365
    #
    #
    #     except:
    #         print("Division by Zero error")
    #

    # def getPaseBid(self):
    #     paseBid = 0
    #     days = self.getDaysBetween()
    #     if self.getOfferPrice(self.symbols[0]) > 0:
    #         paseBid = (self.getBidPrice(self.symbols[1]) / self.getOfferPrice(self.symbols[0]) - 1) / days * 365
    #
    #     return paseBid

    # def getPaseOffer(self):
    #     paseOffer=0
    #     days = self.getDaysBetween()
    #     if self.getBidPrice(self.symbols[0]) > 0:
    #         paseOffer = (self.getOfferPrice(self.symbols[1])/self.getBidPrice(self.symbols[0])-1)/days*365
    #
    #     return paseOffer

    def goRobot(self):
        #print(self.algoName)

        for t in self.symbols:
            self.printLine(t)
        print("in goRobot() c2SymbolsPase")
        print("Pase:",'{percent:.2%}'.format(percent=self.getPaseBid()),"/", '{percent:.2%}'.format(percent=self.getPaseOffer()))


if __name__ == '__main__':
    ticker1 = "RFX20Jun19"
    ticker2 = "RFX20Sep19"

    tuple = (ticker1, ticker2)
    pase = c2SymbolsPase(tuple)