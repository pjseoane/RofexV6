import websocket
import threading
import simplejson

from time import sleep
from datetime import datetime
from RofexConnect import cRESTconnect as rfx
from RofexConnect import cMSGparser as mp

#from Test import cSymbols


class cMDSuscription(rfx.cRESTconnect):

    def __init__(self, symbolsTuple, marketID='ROFX',algoName="cMDSuscription",type_="smd", level_="1"):

        super().__init__(marketID)
        self.symbols = symbolsTuple
        self.numMessages = 0
        self.algoName=algoName
        self.type_ = type_
        self.level_= level_
        self.msg=""
        self.ws=""
        self.tickerMsg = ""
        self.marketDataDict = {}
        self.contractDetail = {}
        self.marketCloseData = {}
        self.sym=""

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
                        print("V7. cMDSuscription Problem in goRobot()")
                        print("V7. Dictionary lenght",self.marketDataDict.__len__(), self.marketDataDict)

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
        m = mp.cMDparser(self.contractDetail[ticker])
        return m.getContractMultiplier()

    def getContractLowLimit(self, ticker):
        m = mp.cMDparser(self.contractDetail[ticker])
        return m.getContractLowLimit()

    def getContractHighLimit(self, ticker):
        m = mp.cMDparser(self.contractDetail[ticker])
        return m.getContractHighLimit()

    def getContractMinPriceIncrement(self, ticker):
        m = mp.cMDparser(self.contractDetail[ticker])
        return m.getContractMinPriceIncrement()

    def getMaturityDate(self, ticker):
        m = mp.cMDparser(self.contractDetail[ticker])
        return m.getMaturityDate()

    def getCficode(self, ticker):
        m = mp.cMDparser(self.contractDetail[ticker])
        return m.getCficode()

    def getCurrency(self, ticker):
        m = mp.cMDparser(self.contractDetail[ticker])
        return m.getCurrency()

    def getMarketSegmentId(self, ticker):
        m = mp.cMDparser(self.contractDetail[ticker])
        return m.getMarketSegmentId()

    def getPriceConvertionFactor(self, ticker):
        m = mp.cMDparser(self.contractDetail[ticker])
        return m.getPriceConvertionFactor()

    def getRoundLot(self, ticker):
        m = mp.cMDparser(self.contractDetail[ticker])
        return m.getRoundLot()

    def getTickSize(self, ticker):
        m = mp.cMDparser(self.contractDetail[ticker])
        return m.getTickSize()

    def getMinTradeVol(self, ticker):
        m = mp.cMDparser(self.contractDetail[ticker])
        return m.getMinTradeVol()

    def getMaxTradeVol(self, ticker):
        m = mp.cMDparser(self.contractDetail[ticker])
        return m.getMaxTradeVol()

    # ********* market data parsers ****************
    def getLastMsgTicker(self, ticker):
        return self.marketDataDict[ticker]

    def getFullMD(self, ticker, depth):
        return self.getMarketData(self.marketId, ticker, depth)

    # def buildParser(self,ticker):
    #     return mp.cMDparser(self.marketDataDict[ticker])

    def getBidPrice(self, ticker):
        m=mp.cMDparser(self.marketDataDict[ticker])
        return m.getBidPrice()

    def getOfferPrice(self, ticker):
        m = mp.cMDparser(self.marketDataDict[ticker])
        return m.getOfferPrice()

    def getBidSize(self, ticker) -> int:
        m=mp.cMDparser(self.marketDataDict[ticker])
        return m.getBidSize()

    def getOfferSize(self, ticker)-> int:
        m = mp.cMDparser(self.marketDataDict[ticker])
        return m.getOfferSize()

    def getTimestamp(self,ticker):
        m = mp.cMDparser(self.marketDataDict[ticker])
        return datetime.fromtimestamp(m.getTimestamp()/1000.0)


    def getLastPrice(self, ticker):
        m = mp.cMDparser(self.marketDataDict[ticker])
        return m.getLastPrice()

    def getClosePrice(self, ticker):
        m = mp.cMDparser(self.marketDataDict[ticker])
        return m.getClosePrice()

    def getOpenInterest(self, ticker):
        m = mp.cMDparser(self.marketDataDict[ticker])
        return m.getOpenInterest()

    def getLatency(self, ticker):
        return datetime.now()-self.getTimestamp(ticker)

#**************************
#ideas form Intereactive Brokers

#data.current(security,fields)
#print(data.current(context.secutity,'price))

if __name__ == '__main__':
    print("V7. Class cMDsuscription")

    t1 = "DOSep19"
    t2 = "RFX20Sep19"
    # t3 = "RFX20Sep19"

    contratos = (t1, t2)
    md1 = cMDSuscription(contratos)

    #test funciones
    for t in contratos:
        print("Ticker:", t)
        print("Contract Details     :", t, md1.instrumentDetail(t))
        print("Contract Multiplier  :", t, md1.getContractMultiplier(t))
        print("Contract Low Limit Price:", t, md1.getContractLowLimit(t))
        print("Maturity Date:",t, md1.getMaturityDate(t))

        print(t," ", md1.getBidPrice(t),"/",md1.getOfferPrice(t),"Size:", md1.getBidSize(t),"-", md1.getOfferSize(t),"/","timestamp:",md1.getTimestamp(t), "Latency:",md1.getLatency(t))



