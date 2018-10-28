from smartcard.CardType import AnyCardType
from smartcard.CardConnection import CardConnection
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes

cardtype = AnyCardType()
cardrequest = CardRequest( timeout=1, cardType=cardtype )
cardservice = cardrequest.waitforcard()

cardservice.connection.connect()

UID = [0x00, 0xCA, 0x00, 0x00, 0x07]

apdu = UID
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice.connection.transmit( apdu )
print 'response: ', toHexString(response), ' status words: ', "%x %x" % (sw1, sw2)
