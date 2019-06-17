import websocket
import threading
import simplejson

from RofexConnect import cRESTconnect as rfx
from time import sleep


class cSymbol(rfx.cRESTconnect):

    def __init__(self, symbol, marketID="ROFX"):

        super().__init__(marketID)
        self.symbol = symbol
        self.numMessages = 0
        self.symDetails = self.instrumentDetail(self.symbol)
        self.lastMSG=""
        self.newMsg=False
        self.type_ = "smd"
        self.level_ = "1"


    def getInstrumentDetails(self):
        return self.symDetails


    #*********************************

    # def getPriceFromJSON(self, field):
    #     # field: 'BI' 'OF' 'LA' 'CL'
    #     mdJSON=self.getMD()
    #     try:
    #         m = mdJSON['marketData'][field][0]['price']
    #     except:
    #         m=0
    #     return m
    #
    # def getSizeFromJSON(self, field):
    #     # field: 'BI' 'OF'
    #     mdJSON = self.getMD()
    #     try:
    #         m = mdJSON['marketData'][field][0]['size']
    #     except:
    #         m=0
    #     return m

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
            print("V7. Test /Suscription - Sent Suscription msg for: ", self.symbol)
            self.ws.send(self.buildMessage)
            sleep(1)

    @property
    def buildMessage(self):

        # 'BI', 'OF', 'LA', 'OP', 'CL', 'SE', 'OI'
        return "{\"type\":\"" + self.type_ + "\",\"level\":" + self.level_ + \
               ", \"entries\":[\"BI\", \"OF\",\"LA\",\"OP\",\"CL\",\"SE\",\"OI\"],\"products\":[{\"symbol\":\"" + \
               self.symbol + "\",\"marketId\":\"" + self.marketId + "\"}]}"

    def resetFlagMsg(self):
            self.newMsg=False

    def on_message(self, message):

        self.numMessages += 1
        try:
            self.msg = simplejson.loads(message)
            msgType = self.msg['type'].upper()

            if msgType == 'MD':

                self.lastMSG=self.msg
                self.newMsg=True
            #****Aca procesar el msg

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


if __name__ == '__main__':

    print("V6. Class cSymbol")
    s1 = "DOJun19"
    s2 = "DOSep19"
    s3 = "RFX20Jun19"
    s4 = "RFX20Sep19"

    t = (s1, s2, s3, s4)

    lista=[]

    for s in t:
        symb=cSymbol(s, "ROFX")

        lista.append(symb)
        symb.suscribeMD()

    while True:
        for x in lista:
            if x.newMsg:
                print(x.lastMSG)
                x.resetFlagMsg()
                print(lista.__len__())


    sleep(1)

    #     print(symb.getInstrumentDetails())
    #     print("Flag:", s, symb.newMsg)
    #
    #
    # #     if symb.newMsg:
    # #         print(symb.lastMSG)
    # #         symb.resetFlagMsg()
    # sleep(1)


    # symb1 = cSymbol("RFX20Jun19", "ROFX")
    # print("JSON", symb1.getInstrumentDetails())
    #
    #
    #

    # print("Market Segment", symb.getMarketSegmentId())
    # print("Low Limit", symb.getLowLimitPrice())
    # print("High Limit", symb.getHighLimitPrice())
    # print("Min Price Incr", symb.getMinPriceIncrement())
    # print("Min Trade Vol", symb.getMinTradeVol())
    # print("Max Trade Vol", symb.getMaxTradeVol())
    # print("Tick Size", symb.getTickSize())
    # print("Multiplier", symb.getContractMultiplier())
    # print("Round lot", symb.getRoundLot())
    # print("Price Convertion Factor", symb.getPriceConvertionFactor())
    # print("Maturity Date", symb.getMaturityDate())
    # print("Currency", symb.getCurrency())
    # print("cficode", symb.getCficode())
    # print("Market Id", symb.getMarketId())
    # print("Symbol", symb.getSymbol())

    # md = symb.getMD()
    # print("Symbol MD", md)
    #
    # print("Symbol Bid/Size :", symb.getBidPrice(), symb.getBidSize())
    # print("Symbol Offer/Size:", symb.getOfferPrice(), symb.getOfferSize())
    # print("Symbol Last:", symb.getLastPrice())
    # print("Symbol OI:", symb.getOpenInterest())
    # print("Symbol CL:", symb.getClosePrice())
