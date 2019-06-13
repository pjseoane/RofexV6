from RofexConnect import cRESTconnect as rfx


class cSymbol(rfx.cRESTconnect):

    def __init__(self, symbol, marketID="ROFX"):

        super().__init__(marketID)
        self.symbol = symbol
        self.numMessages = 0
        self.symDetails = self.instrumentDetail(self.symbol)

    def getDetails(self):
        return self.symDetails

    def getContractMultiplier(self):
        return self.symDetails['instrument']['contractMultiplier']

    def getLowLimitPrice(self):
        return self.symDetails['instrument']['lowLimitPrice']

    def getHighLimitPrice(self):
        return self.symDetails['instrument']['highLimitPrice']

    def getMinPriceIncrement(self):
        return self.symDetails['instrument']['minPriceIncrement']

    def getMaturityDate(self):
        return self.symDetails['instrument']['maturityDate']

    def getMinTradeVol(self):
        return self.symDetails['instrument']['minTradeVol']

    def getMaxTradeVol(self):
        return self.symDetails['instrument']['maxTradeVol']

    def getTickSize(self):
        return self.symDetails['instrument']['tickSize']

    def getRoundLot(self):
        return self.symDetails['instrument']['roundLot']

    def getPriceConvertionFactor(self):
        return self.symDetails['instrument']['priceConvertionFactor']

    def getMarketSegmentId(self):
        return self.symDetails['instrument']['segment']['marketSegmentId']

    def getCurrency(self):
        return self.symDetails['instrument']['currency']

    def getCficode(self):
        return self.symDetails['instrument']['cficode']

    def getMarketId(self):
        return self.symDetails['instrument']['instrumentId']['marketId']

    def getSymbol(self):
        return self.symDetails['instrument']['instrumentId']['symbol']

    #*********************************

    def getMD(self):
        return self.getMarketData(self.marketId, self.symbol, "1")

    def getPriceFromJSON2(self, field, mdJSON):
        try:
            m = mdJSON['marketData'][field][0]['price']
        except:
            m=0
        return m

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


    def getBidPrice(self):
        return self.getPriceFromJSON('BI')

    def getOfferPrice(self):
        return self.getPriceFromJSON('OF')

    # def getLastPrice(self):
    #     return self.getPriceFromJSON('LA')


    def getLastPrice(self):
        mdJSON = self.getMD()
        try:
            m = mdJSON['marketData']['LA']['price']
        except:
            m = 0
        return m

    def getClosePrice(self):
        mdJSON = self.getMD()
        try:
            m = mdJSON['marketData']['CL']['price']
        except:
            m = 0
        return m

    # def getClosePrice(self):
    #     return self.getPriceFromJSON('CL')

    def getBidSize(self):
        return self.getSizeFromJSON('BI')

    def getOfferSize(self):
        return self.getSizeFromJSON('OF')

    # def getOpenInterest(self):
    #     return self.getSizeFromJSON('OI')

    def getOpenInterest(self):
        mdJSON = self.getMD()

        try:
            m = mdJSON['marketData']['OI']['size']
        except:
            m = 0
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
