from Objects import cMDsuscription as md
from datetime import date
from datetime import date


class cAlgoZero(md.cMDSuscription):

    def __init__(self, symbols, mktID="ROFX"):

        super().__init__(symbols, mktID)
        self.maturities=[]

        for s in symbols:
            self.maturities.append(self.contractDetail[s].getMaturityDate())

    def getDaysBetween(self):
        dates = []
        for d in self.maturities:
            dates.append(date(int(d[:4]), int(d[5:6]), int(d[6:])))

        delta = dates[1] - dates[0]
        return delta.days


def goRobot(self):
        pass

if __name__ == '__main__':
    ticker1 = "RFX20Jun19"
    ticker2 = "RFX20Sep19"
    #ticker3= "RFX20Jun19 44000c"
    tuple = (ticker1, ticker2)
    aZero=cAlgoZero(tuple)
    print("Days:",aZero.getDaysBetween())
