from RofexConnect import cRESTconnect as rfx



class cSymbol(rfx.cRESTconnect):

    def __init__(self, symbol, marketID="ROFX"):

        super().__init__(marketID)
        self.symbol = symbol
        self.numMessages = 0
        self.symDetails = self.instrumentDetail(self.symbol)

    def getDetails(self):
        return self.symDetails



















    #*********************************

    def getPriceFromJSON(self, field):
        # field: 'BI' 'OF' 'LA' 'CL'
        mdJSON=self.getMD()
        try:
            m = mdJSON['marketData'][field][0]['price']
        except:
            m=0
        return m

    def getSizeFromJSON(self, field):
        # field: 'BI' 'OF'
        mdJSON = self.getMD()
        try:
            m = mdJSON['marketData'][field][0]['size']
        except:
            m=0
        return m





if __name__ == '__main__':

    print("V6. Class cSymbol")
    symb = cSymbol("RFX20Jun19", "ROFX")
    print("JSON", symb.getDetails())
    print("Market Segment", symb.getMarketSegmentId())
    print("Low Limit", symb.getLowLimitPrice())
    print("High Limit", symb.getHighLimitPrice())
    print("Min Price Incr", symb.getMinPriceIncrement())
    print("Min Trade Vol", symb.getMinTradeVol())
    print("Max Trade Vol", symb.getMaxTradeVol())
    print("Tick Size", symb.getTickSize())
    print("Multiplier", symb.getContractMultiplier())
    print("Round lot", symb.getRoundLot())
    print("Price Convertion Factor", symb.getPriceConvertionFactor())
    print("Maturity Date", symb.getMaturityDate())
    print("Currency", symb.getCurrency())
    print("cficode", symb.getCficode())
    print("Market Id", symb.getMarketId())
    print("Symbol", symb.getSymbol())

    md = symb.getMD()
    print("Symbol MD", md)

    print("Symbol Bid/Size :", symb.getBidPrice(), symb.getBidSize())
    print("Symbol Offer/Size:", symb.getOfferPrice(), symb.getOfferSize())
    print("Symbol Last:", symb.getLastPrice())
    print("Symbol OI:", symb.getOpenInterest())
    print("Symbol CL:", symb.getClosePrice())
