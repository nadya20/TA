from smartcard.CardType import ATRCardType
from smartcard.CardConnection import CardConnection
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes
import time

cardtype0 = ATRCardType( toBytes( "3B 10 96" ))
cardrequest0 = CardRequest( timeout=10, cardType=cardtype0 )
cardservice0 = cardrequest0.waitforcard()
cardservice0.connection.connect()

cardtype1 = ATRCardType( toBytes( "3B 13 96 13 09 17" ))
cardrequest1 = CardRequest( timeout=10, cardType=cardtype1 )
cardservice1 = cardrequest1.waitforcard()
cardservice1.connection.connect()

SELECT = [0x00, 0xA4, 0x00, 0x00, 0x02]
MF_SC = [0x3F, 0x00]
DF_SC = [0x40, 0x00]
EF_SC = [0x40, 0x01]
READ = [0x00, 0xB0, 0x00, 0x00]
length= [0x36]

start=time.time()
apdu = SELECT + MF_SC
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice1.connection.transmit( apdu )
print ' status words: ', "%x %x" % (sw1, sw2)
apdu = SELECT + DF_SC
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice1.connection.transmit( apdu )
print ' status words: ', "%x %x" % (sw1, sw2)

if(sw1 == 0x61): print("Selamat Datang")
else: print("Tunggu Dosenmu")

apdu = SELECT + EF_SC
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice1.connection.transmit( apdu )
print ' status words: ', "%x %x" % (sw1, sw2)
apdu = READ + length
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice1.connection.transmit( apdu )
print 'response: ', toHexString(response), ' status words: ', "%x %x" % (sw1, sw2)

end=time.time()
print 'time',(end-start)
