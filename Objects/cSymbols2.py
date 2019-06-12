import websocket
import threading
import simplejson

from time import sleep


from RofexConnect import cRESTconnect as rfx

class cSymbol(rfx.cRESTconnect):

    def __init__(self, symbol, marketID):

        super().__init__(marketID)
        self.symbol = symbol
        self.numMessages = 0
        self.symDetails = self.instrumentDetail(self.symbol)
        self.type_= "smd"
        self.level_ = "1"
        self.msg=""
        self.ws=""

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

    def getMD(self) -> object:
        return self.getMarketData(self.marketId, self.symbol, "1")

    def getBidPrice(self, mdJSON):
        try:
            m = mdJSON['marketData']['BI'][0]['price']
        except:
            m = 0
        return m

    def getBidPrice2(self):
        try:
            m=self.getBidPrice(self.getMD())
        except:
            m=0
        return m

    def getBidSize(self, mdJSON):
        try:
            m = mdJSON['marketData']['BI'][0]['size']
        except:
            m = 0
        return m

    def getBidSize2(self):
        try:
            m = self.getBidSize(self.getMD())
        except:
            m = 0
        return m

    def getOfferPrice(self, mdJSON):
        try:
            m = mdJSON['marketData']['OF'][0]['price']
        except:
            m = 0
        return m

    def getOfferSize(self, mdJSON):
        try:
            m = mdJSON['marketData']['OF'][0]['size']
        except:
            m = 0
        return m

    def getLastPrice(self, mdJSON):
        try:
            m = mdJSON['marketData']['LA']['price']
        except:
            m = 0
        return m

    def getClose(self, mdJSON):
        try:
            m = mdJSON['marketData']['CL']['price']
        except:
            m = 0
        return m

    def getOpenInterest(self, mdJSON):
        try:
            m = mdJSON['marketData']['OI']['size']
        except:
            m = 0
        return m

    def suscribeMD(self):
        headers = {'X-Auth-Token:{token}'.format(token=self.token)}
        self.ws = websocket.WebSocketApp(self.wsEndPoint,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close,
                                         on_open=self.on_open,
                                         header=headers)

        wst = threading.Thread(target=self.ws.run_forever, kwargs={"ping_interval": 5})
        wst.start()
        # Esperamos a que la conexion ws se establezca
        conn_timeout = 5
        # conn_timeout = 50 #y nada
        sleep(1)

        while not self.ws.sock.connected and conn_timeout:
            sleep(1)
            conn_timeout -= 1
        else:
            print("cSymbols2 - Sent Suscription msg for: ", self.symbol)
            self.ws.send(self.buildMessage())
            sleep(1)

    def on_message(self, message):

        self.numMessages += 1
        try:
            self.msg = simplejson.loads(message)
            msgType = self.msg['type'].upper()

            if msgType == 'MD':

                try:
                    self.goRobot()
                except:
                    print("Problem in goRobot()")

            elif msgType == 'OR':
                print("En Mensaje OR")
                print(self.msg)
            else:
                print("Tipo de Mensaje Recibido No soportado: ", self.msg)

        except:
            print("Error al procesar mensaje recibido:--->>> ", message)

    @staticmethod
    def on_close():
        print("### connection closed ###")

    def on_error(self, error):
        print("Salio por error: ", error)
        self.ws.close()

    @staticmethod
    def on_open():
        # pass
        print("WS Conection Open...")

    def buildMessage(self):

        # 'BI', 'OF', 'LA', 'OP', 'CL', 'SE', 'OI'
        return "{\"type\":\"" + self.type_ + "\",\"level\":" + self.level_ + \
               ", \"entries\":[\"BI\", \"OF\",\"LA\"],\"products\":[{\"symbol\":\"" + \
               self.symbol + "\",\"marketId\":\"" + self.marketId + "\"}]}"

    def goRobot(self):
        # Overridable Method
        #print("cSymbols2-En GoRobot, recibiendo mensajes")
        #print(self.getLastMsg())
        pass

    def getLastMsg(self):
        return self.msg


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

    print("Symbol Bid/Size :", symb.getBidPrice(md), symb.getBidSize(md))
    print("Symbol Bid/Size2:", symb.getBidPrice2(), symb.getBidSize2())
    print("Symbol Offer/Size:", symb.getOfferPrice(md), symb.getOfferSize(md))
    print("Symbol Last:", symb.getLastPrice(md))
    print("Symbol OI:", symb.getOpenInterest(md))
    print("Symbol CL:", symb.getClose(md))

    symb2 = cSymbol("DOJun19", "ROFX")
    marketDataDict={}
    print("Market suscribe 1:", symb.suscribeMD())
    print("Market suscribe 2:", symb2.suscribeMD())
