from Objects import cSymbols2 as symb


class cAlgoPrint(symb.cSymbol):

    def __init__(self, symb1, mkt1):
        super().__init__(symb1, mkt1)
        #self.t1=symb.cSymbol(symb1, mkt1)



    def goRobot(self):
        print("algoPRINT", self.getSymbol(), self.getLastMsg())



if __name__ == '__main__':
    tick1 = symb.cSymbol("RFX20Jun19", "ROFX")
    tick2 = symb.cSymbol("DOJun19", "ROFX")
    algoP = cAlgoPrint("RFX20Jun19", "ROFX")
    algoP2 = cAlgoPrint("RFX20Sep19", "ROFX")
    algoP.suscribeMD()
    algoP2.suscribeMD()






