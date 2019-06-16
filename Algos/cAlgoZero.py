from RofexConnect import cMDsuscription as md
from RofexConnect import cMSGparser as mp


class cAlgoZero(md.cMDSuscription):

    def __init__(self, symbols, mktID="ROFX", algoName="Z-Robot"):

        super().__init__(symbols, mktID)
        self.algoName=algoName

    def goRobot(self):
        lm=self.getLastMsg()
        m=mp.cMDparser(lm)
        print("V7. cAlgoZero, last msg latency",m.getLastMsgLatentency())

        pass


if __name__ == '__main__':
    t1 = "RFX20Jun19"
    t2 = "RFX20Sep19"
    t3= "RFX20Jun19 44000c"
    tuple = (t1, t2,t3)
    aZero=cAlgoZero(tuple)

