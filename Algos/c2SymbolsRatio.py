from Algos import c2SymbolsZero as a2


class c2SymbolsPase(a2.c2SymbolsZero):
    def __init__(self, symbols, mktID="ROFX"):
        super().__init__(symbols, mktID)

    def setRatioMarket(self, bid, offer, size):
        self.myRatioBid = bid
        self.myRatioOffer = offer
        self.tradeSize = size

    def setMyRatioBid(self, myRatioBid):
        self.myRatioBid = myRatioBid

    def setMyRatioOffer(self, myRatioOffer):
        self.myRatioOffer = myRatioOffer

    def goRobot(self):

        for t in self.symbols:
            self.printLine(t)


if __name__ == '__main__':
    ticker1 = "DOJun19"
    ticker2 = "RFX20Jun19"

    tickers = (ticker1, ticker2)
    pase = c2SymbolsPase(tickers)