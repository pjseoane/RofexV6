import websocket
import threading
import simplejson
from Test import cSymbols as sy

class MDsuscript(sy.cSymbol):

    def __init__(self, symbols, mktID="ROFX"):
        super().__init__(symbols, mktID)

        headers = {'X-Auth-Token:{token}'.format(token=self.token)}
        self.ws = websocket.WebSocketApp(self.wsEndPoint,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close,
                                         on_open=self.on_open,
                                         header=headers)
