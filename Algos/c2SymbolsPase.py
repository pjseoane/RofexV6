
from Algos import c2SymbolsZero as a2


class c2SymbolsPase(a2.c2SymbolsZero):
    def __init__(self, symbols, mktID="ROFX"):
        super().__init__(symbols, mktID)


    def goRobot(self):
        print("v7. c2SymbolsPase")

        for t in self.symbols:
            print(t, "Bid / Offer", self.getBidPrice(t), "/", self.getOfferPrice(t), self.getBidSize(t), "x",
                  self.getOfferSize(t))

        days=self.getDaysBetween()

        print("Days:",days,"Pase:",'{percent:.2%}'.format(percent=(self.getBidPrice(self.symbols[1])/self.getOfferPrice(self.symbols[0])-1)/days*365), "/", '{percent:.2%}'.format(percent=(self.getOfferPrice(self.symbols[1])/self.getBidPrice(self.symbols[0])-1)/days*365))


if __name__ == '__main__':
    ticker1 = "RFX20Jun19"
    ticker2 = "RFX20Sep19"

    tuple = (ticker1, ticker2)
    pase = c2SymbolsPase(tuple)