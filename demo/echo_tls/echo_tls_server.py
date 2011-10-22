###############################################################################
##
##  Copyright 2011 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

import sys
from twisted.python import log
from twisted.internet import reactor, ssl
from twisted.web.server import Site
from twisted.web.static import File
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS

class EchoServerProtocol(WebSocketServerProtocol):

   def sendHello(self):
      if self.send_hello:
         for i in xrange(0, 3):
            self.sendMessage("*" * (self.count * 5))
         self.count += 1
         reactor.callLater(1, self.sendHello)

   def onOpen(self):
      self.count = 1
      self.send_hello = True
      #self.sendHello()

   def onMessage(self, msg, binary):
      print msg
      self.sendMessage(msg, binary)

   def connectionLost(self, reason):
      WebSocketServerProtocol.connectionLost(self, reason)
      self.send_hello = False


if __name__ == '__main__':

   log.startLogging(sys.stdout)

   ## create a WS server factory with our protocol
   ##
   factory = WebSocketServerFactory("wss://localhost:9000", debug = False)
   factory.protocol = EchoServerProtocol

   ## SSL server context: load server key and certificate
   ##
   contextFactory = ssl.DefaultOpenSSLContextFactory('keys/server.key', 'keys/server.crt')

   ## now start listening ..
   listenWS(factory, contextFactory)


   ## https://localhost:9090/
   webdir = File(".")
   web = Site(webdir)
   reactor.listenSSL(9090, web, contextFactory)

   reactor.run()
