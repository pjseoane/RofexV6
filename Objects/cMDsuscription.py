import websocket
import threading
import simplejson

from time import sleep
from RofexConnect import cRESTconnect as rfx
#from Objects import cSymbols


class cMDSuscription(rfx.cRESTconnect):

    def __init__(self, symbols, marketID='ROFX',type_="smd", level_="1"):

        super().__init__(marketID)
        self.symbols = symbols
        self.numMessages = 0
        self.type_ = type_
        self.level_= level_
        self.msg=""
        self.ws=""
        self.tickerMsg = ""
        self.marketDataDict = {}
        self.contractDetail = {}
        self.marketCloseData = {}
        self.symbol=""

    #def suscribeMD(self):
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

            for self.sym in self.symbols:
                print("V7. cMDsuscription - Sent Suscription msg for: ", self.sym)

                self.contractDetail[self.sym] = self.instrumentDetail(self.sym)
                self.marketCloseData[self.sym] = self.getMarketData(marketID,self.sym, str(1))

                self.ws.send(self.buildMessage)
                sleep(1)

    @property
    def buildMessage(self):

        # 'BI', 'OF', 'LA', 'OP', 'CL', 'SE', 'OI'
        return "{\"type\":\"" + self.type_ + "\",\"level\":" + self.level_ + \
               ", \"entries\":[\"BI\", \"OF\",\"LA\",\"OP\",\"CL\",\"SE\",\"OI\"],\"products\":[{\"symbol\":\"" + \
               self.sym + "\",\"marketId\":\"" + self.marketId + "\"}]}"


    def on_message(self, message):

        self.numMessages += 1
        try:
            self.msg = simplejson.loads(message)
            msgType = self.msg['type'].upper()

            if msgType == 'MD':
                # Arma y carga el Dictionary
                # Busca de que sym es el mensaje que viene y lo coloca en el Dictionary

                tickerMsg = self.msg['instrumentId']['symbol']
                self.marketDataDict[tickerMsg] = self.msg

                if self.marketDataDict.__len__() == len(self.symbols):
                    print("V7. cMDsuscription - Dict OK, New Msg")
                    try:
                        self.goRobot()
                    except:
                        print("Problem in goRobot()")
                        print("Dictionary", self.marketDataDict)

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

    def goRobot(self):
        # Overridable Method
        print("V7. cMDsuscription-En GoRobot, recibiendo mensajes")
        print(self.getLastMsg())

    def getLastMsg(self):
        return self.msg

    #*********** contract details parsers ***************

    def getContractMultiplier(self, ticker):
        return self.contractDetail[ticker]['instrument']['contractMultiplier']

    def getContractLowLimit(self, ticker):
        return self.contractDetail[ticker]['instrument']['lowLimitPrice']

    def getContractHighLimit(self, ticker):
        return self.contractDetail[ticker]['instrument']['highLimitPrice']

    def getContractMinPriceIncrement(self, ticker):
        return self.contractDetail[ticker]['instrument']['minPriceIncrement']

    def getMaturityDate(self, ticker):
        return self.contractDetail[ticker]['instrument']['maturityDate']

    def getCficode(self, ticker):
        return self.contractDetail[ticker]['instrument']['cficode']

    def getCurrency(self, ticker):
        return self.contractDetail[ticker]['instrument']['currency']

    def getMarketSegmentId(self, ticker):
        return self.contractDetail[ticker]['instrument']['segment']['marketSegmentId']

    def getPriceConvertionFactor(self, ticker):
        return self.contractDetail[ticker]['instrument']['priceConvertionFactor']

    def getRoundLot(self, ticker):
        return self.contractDetail[ticker]['instrument']['roundLot']

    def getTickSize(self, ticker):
        return self.contractDetail[ticker]['instrument']['tickSize']

    def getMinTradeVol(self, ticker):
        return self.contractDetail[ticker]['instrument']['minTradeVol']

    def getMaxTradeVol(self, ticker):
        return self.contractDetail[ticker]['instrument']['maxTradeVol']



    # ********* market data parsers ****************
    def getLastMsgTicker(self, ticker):
        return self.marketDataDict[ticker]

    def getFullMD(self, ticker, depth):
        return self.getMarketData(self.marketId, ticker, depth)

    def getBidPrice(self, ticker):
        try:
            m = self.marketDataDict[ticker]['marketData']['BI'][0]['price']
        except:
            m = 0
        return m

    def getBidSize(self, ticker) -> int:
        try:
            m = self.marketDataDict[ticker]['marketData']['BI'][0]['size']
        except:
            m = 0
        return m

    def getOfferPrice(self, ticker):
        try:
            m = self.marketDataDict[ticker]['marketData']['OF'][0]['price']
        except:
            m = 0
        return m

    def getOfferSize(self, ticker)-> int:
        try:
            m = self.marketDataDict[ticker]['marketData']['OF'][0]['size']
        except:
            m = 0
        return m

    def getTimestamp(self, ticker):
        return self.marketDataDict[ticker]['timestamp']

    def getLastPrice(self, ticker):
        try:
            m = self.marketCloseData[ticker]['marketData']['LA']['price']
        except:
            m = 0
        return m

    def getClosePrice(self, ticker):
        try:
            m = self.marketCloseData[ticker]['marketData']['CL']['price']
        except:
            m = 0
        return m

    def getOpenInterest(self, ticker):
        try:
            m = self.marketCloseData[ticker]['marketData']['OI']['size']
        except:
            m = 0
        return m



if __name__ == '__main__':
    print("V7. Class cMDsuscription")

    t1 = "DOJun19"
    t2 = "RFX20Jun19"
    t3 = "RFX20Sep19"

    contratos = (t1, t2,t3)
    md1 = cMDSuscription(contratos)


    print("Ticker:", t1)
    print("Contract Details     :", t1, md1.instrumentDetail(t1))
    print("Contract Multiplier  :", t1, md1.getContractMultiplier(t1))
    print("Contract Low Limit Price:", t1, md1.getContractLowLimit(t1))
    print(t1," ", md1.getBidPrice(t1),"/",md1.getOfferPrice(t1),md1.getBidSize(t1),"/", md1.getOfferSize(t1),"/","timestamp:",md1.getTimestamp(t1))
    print(t2," ", md1.getBidPrice(t2),"/",md1.getOfferPrice(t2),md1.getBidSize(t2),"/", md1.getOfferSize(t2),"/","timestamp:",md1.getTimestamp(t2))
    print(t3, " ", md1.getBidPrice(t3), "/", md1.getOfferPrice(t3), md1.getBidSize(t3), "/", md1.getOfferSize(t3), "/","timestamp:", md1.getTimestamp(t3))


