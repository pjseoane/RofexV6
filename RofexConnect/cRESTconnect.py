import configparser
import requests
import simplejson


class cRESTconnect():

    def __init__(self, marketID):

        self.marketId= marketID
        cpParser = configparser.RawConfigParser()
        cfgFile = r'..\Configuration\RofexV6.cfg'

        cpParser.read(cfgFile)

        self.activeEndpoint = cpParser.get('url', 'endpointDemo')
        self.wsEndPoint = cpParser.get('url', 'wsEndpointDemo')
        usr = cpParser.get('usr-credentials', 'usr')
        pswd = cpParser.get('usr-credentials', 'pswd')

        self.account = cpParser.get('usr-credentials', 'account')

        s = requests.Session()
        self.url = self.activeEndpoint + "auth/getToken"
        headers = {'X-Username': usr, 'X-Password': pswd}
        loginResponse = s.post(self.url, headers=headers, verify=False)

        if loginResponse.ok:
            self.token = loginResponse.headers['X-Auth-Token']
        else:
            self.token = 0

    def getToken(self):
        return self.token

    def retReq(self):
        headers = {'X-Auth-Token': self.getToken()}
        r = requests.get(self.url, headers=headers, verify=False)
        return simplejson.loads(r.content)

    def instrumentos(self):
        self.url = self.activeEndpoint + "rest/instruments/all"
        return self.retReq()

    def instrumentDetail(self, symbol):
        self.url = self.activeEndpoint + "rest/instruments/detail?symbol=" + symbol + "&marketId=" + self.marketId
        return self.retReq()

    def instrumentsDetailsAll(self):
        self.url = self.activeEndpoint + "rest/instruments/details"
        return self.retReq()

    def listaSegmentosDisp(self):
        self.url = self.activeEndpoint + "rest/segment/all"
        return self.retReq()

    def instrumentsByCFICode(self, CFIcode):
        self.url = self.activeEndpoint + "rest/instruments/byCFICode?CFICode=" + CFIcode
        return self.retReq()

    def instrumentsBySegments(self, segments):
        self.url = self.activeEndpoint + "rest/instruments/bySegment?MarketSegmentID=" + segments + "&MarketID=ROFX"
        return self.retReq()

    def newSingleOrder(self, symbol, price, orderQty, ordType, side, timeInForce, account, cancelPrevious):
        self.url = self.activeEndpoint + "rest/order/newSingleOrder?marketId=" + self.marketId + "&symbol=" + symbol + "&price=" + price + "&orderQty=" + orderQty + "&ordType=" + ordType + "&side=" + side + "&timeInForce=" + timeInForce + "&account=" + account + "&cancelPrevious=" + cancelPrevious
        # self.trades+=1
        return self.retReq()

    def newIcebergOrder(self, marketId, symbol, price, orderQty, ordType, side, timeInForce, account,
                        cancelPrevious,
                        iceberg,
                        displayQty):

        self.url = self.activeEndpoint + "rest/order/newSingleOrder?marketId=" + marketId + "&symbol=" + symbol + "&price=" + price + "&orderQty=" + orderQty + "&ordType=" + ordType + "&side=" + side + "&timeInForce=" + timeInForce + "&account=" + account + "&cancelPrevious=" + cancelPrevious + "&iceberg=" + iceberg + "&displayQty=" + displayQty
        return self.retReq()

    def newGTDOrder(self, marketId, symbol, price, orderQty, ordType, side, timeInForce, account, expireDate):
        self.url = self.activeEndpoint + "rest/order/newSingleOrder?marketId=" + marketId + "&symbol=" + symbol + "&price=" + price + "&orderQty=" + orderQty + "&ordType=" + ordType + "&side=" + side + "&timeInForce=GTD" + "&account=" + account + "&expireDate=" + expireDate
        return self.retReq()

    def replaceOrderById(self, clOrdId, proprietary, price, orderQty):
        self.url = self.activeEndpoint + "rest/order/replaceById?clOrdId=" + clOrdId + "&proprietary=" + proprietary + "&price=" + price + "&orderQty=" + orderQty
        return self.retReq()

    def cancelOrderById(self, clOrdId, proprietary):
        self.url = self.activeEndpoint + "rest/order/cancelById?clOrdId=" + clOrdId + "&proprietary=" + proprietary
        return self.retReq()

    def consultarUltEstadoOrderById(self, clOrdId, proprietary):
        self.url = self.activeEndpoint + "rest/order/id?clOrdId=" + clOrdId + "&proprietary=" + proprietary
        return self.retReq()

    def consultarAllEstadoOrderById(self, clOrdId, proprietary):
        self.url = self.activeEndpoint + "rest/order/allById?clOrdId=" + clOrdId + "&proprietary=" + proprietary
        return self.retReq()

    def consultarOrden(self, orderId):
        self.url = self.activeEndpoint + "rest/order/byOrderId?orderId=" + orderId
        return self.retReq()

    def getOrdenesOpen(self, accountId):
        self.url = self.activeEndpoint + "rest/order/actives?accountId=" + accountId
        return self.retReq()

    def getOrdenesFilled(self, accountId):
        self.url = self.activeEndpoint + "rest/order/filleds?accountId=" + accountId
        return self.retReq()

    def getOrdenesAll(self, accountId):
        self.url = self.activeEndpoint + "rest/order/all?accountId=" + accountId
        return self.retReq()

    def consultarOrdenExecutionId(self, execId):
        self.url = self.activeEndpoint + "rest/order/byExecId?execId=" + execId
        return self.retReq()

    # def getMarketData(self, marketId: str, symbol: str, p1: object, p2: object, p3: object, p4: object, p5: object,
    #                   p6: object, p7: object, depth: object) -> object:
    #     # parameters p1...p7 :"BI","OF","LA","OP","CL","SE","OI"
    #     self.url = self.activeEndpoint + "rest/marketdata/get?marketId=" + marketId + "&symbol=" + symbol + "&entries=" + p1 + "," + p2 + "," + p3 + "," + p4 + "," + p5 + "," + p6 + "," + p7 + "&depth=" + depth
    #     return self.retReq()

    def getMarketData(self, marketId, symbol,depth):
        self.url = self.activeEndpoint + "rest/marketdata/get?marketId=" + marketId + "&symbol=" + symbol + "&entries=BI,OF,LA,OP,CL,SE,OI&depth=" + depth
        return self.retReq()

    def getMarketDataHist(self, marketId, symbol, date):
        self.url = self.activeEndpoint + "rest/data/getTrades?marketId=" + marketId + "&symbol=" + symbol + "&date=" + date
        return self.retReq()

    def getMarketDataHistRange(self, marketId, symbol, dateFrom, dateTo):
        self.url = self.activeEndpoint + "rest/data/getTrades?marketId=" + marketId + "&symbol=" + symbol + "&dateFrom=" + dateFrom + "&dateTo=" + dateTo
        return self.retReq()


if __name__ == '__main__':

    RFXtoken=cRESTconnect('ROFX')
    print("V6. Token:-->", RFXtoken.getToken())

else:
    pass