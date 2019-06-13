import websocket
import threading
import simplejson

from time import sleep
from RofexConnect import cRESTconnect as rfx
from Objects import cSymbols


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
        #self.marketID=marketID
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

            for self.symbol in self.symbols:
                print("V6. cMDsuscription - Sent Suscription msg for: ", self.symbol)


                # Construye objetos cSymbol para cada ticker
                self.contractDetail[self.symbol] = cSymbols.cSymbol(self.symbol, marketID)
                self.ws.send(self.buildMessage)
                sleep(1)

    @property
    def buildMessage(self):

        # 'BI', 'OF', 'LA', 'OP', 'CL', 'SE', 'OI'
        return "{\"type\":\"" + self.type_ + "\",\"level\":" + self.level_ + \
               ", \"entries\":[\"BI\", \"OF\",\"LA\"],\"products\":[{\"symbol\":\"" + \
               self.symbol + "\",\"marketId\":\"" + self.marketId + "\"}]}"


    def on_message(self, message):

        self.numMessages += 1
        try:
            self.msg = simplejson.loads(message)
            msgType = self.msg['type'].upper()

            if msgType == 'MD':
                self.tickerMsg = self.msg['instrumentId']['symbol']
                self.marketDataDict[self.tickerMsg] = self.msg

                if self.marketDataDict.__len__() == len(self.symbols):
                    print("V6.cMDsuscription - Dict OK, New Msg")
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

    def goRobot(self):
        # Overridable Method
        print("V6. cMDsuscription-En GoRobot, recibiendo mensajes")
        print(self.getLastMsg())

    def getLastMsg(self):
        return self.msg


if __name__ == '__main__':
    print("V6. Class cMDsuscription")

    ticker1 = "DOJun19"
    ticker2 = "RFX20Jun19"


    tuple = (ticker1, ticker2)
    md1 = cMDSuscription(tuple, "ROFX")
    #md1.suscribeMD()

    print("Ticker:", ticker1)
    t1=cSymbols.cSymbol(ticker1)
    print("Contract Details     :",t1.getDetails())
    print("Contract Multiplier  :", t1.getContractMultiplier())
    print("Contract Low Limit Price:", t1.getLowLimitPrice())





