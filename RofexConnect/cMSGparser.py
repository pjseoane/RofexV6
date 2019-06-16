from datetime import date, datetime

# Parseo de msg de MD

class cMDparser():

    def __init__(self, msg):
        self.msg=msg

    #******** MD Parsers
    def getBidPrice(self):
        try:
             m = self.msg['marketData']['BI'][0]['price']
        except:
             m = 0
        return m

    def getOfferPrice(self):
        try:
             m = self.msg['marketData']['OF'][0]['price']
        except:
             m = 0
        return m

    def getBidSize(self):
        try:
            m = self.msg['marketData']['BI'][0]['size']
        except:
            m = 0
        return m

    def getOfferSize(self):
        try:
            m = self.msg['marketData']['OF'][0]['size']
        except:
            m = 0
        return m

    def getTimestamp(self):
        return int(self.msg['timestamp'])

    def getLastPrice(self):
        try:
            m = self.msg['marketData']['LA']['price']
        except:
            m = 0
        return m

    def getClosePrice(self):
        try:
            m = self.msg['marketData']['CL']['price']
        except:
            m = 0
        return m

    def getOpenInterest(self):
        try:
            m = self.msg['marketData']['OI']['size']
        except:
            m = 0
        return m

    #******* Contract Details Parsers

    def getContractMultiplier(self):
        return int(self.msg['instrument']['contractMultiplier'])

    def getContractLowLimit(self):
        return int(self.msg['instrument']['lowLimitPrice'])

    def getContractHighLimit(self):
        return int(self.msg['instrument']['highLimitPrice'])

    def getContractMinPriceIncrement(self):
        return int(self.msg['instrument']['minPriceIncrement'])

    def getMaturityDate(self):
        mdate = self.msg['instrument']['maturityDate']
        md = (date(int(mdate[:4]), int(mdate[5:6]), int(mdate[6:])))
        return md

    def getCficode(self):
        return self.msg['instrument']['cficode']

    def getCurrency(self):
        return self.msg['instrument']['currency']

    def getMarketSegmentId(self):
        return self.msg['instrument']['segment']['marketSegmentId']

    def getPriceConvertionFactor(self):
        return self.msg['instrument']['priceConvertionFactor']

    def getRoundLot(self):
        return self.msg['instrument']['roundLot']

    def getTickSize(self):
        return self.msg['instrument']['tickSize']

    def getMinTradeVol(self):
        return self.msg['instrument']['minTradeVol']

    def getMaxTradeVol(self):
        return self.msg['instrument']['maxTradeVol']

    def getLastMsgLatentency(self):
        tstamp = datetime.fromtimestamp(int(self.msg['timestamp']) / 1000.0)
        return (datetime.now() - tstamp)
