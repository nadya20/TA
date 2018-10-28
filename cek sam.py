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
MUA = [0x00, 0x82, 0x00, 0x00, 0x10]

WRITE2 = [0x00, 0xD0] 
READ = [0x00, 0xB0, 0x00, 0x00]
ENCRIPT= [0x51, 0x33, 0x00, 0x00]
length= [0x09]
byte = [0x00, 0x00]
KODE1_PRESENSI= [0x45,0x4C,0x48,0x34,0x41,0x33,0x31,0x00,0x00]

GR_SC = [0x00, 0xC0, 0x00, 0x00]
GC_SC=	[0x00, 0x84, 0x00, 0x00, 0x01]
GU_SC = [0x00, 0xCA, 0x00, 0x00, 0x07]
MF_SC = [0x3F, 0x00]
DF_SC = [0x40, 0x00]
EF_SC = [0x40, 0x01]
DF_SCM= [0x50, 0x00]
EF_SCMP= [0x50, 0x02]

MF_SAM = [0x3F, 0x00]
DF_SAM = [0x40, 0x00]
EF_SAM = [0x40, 0x02]
LK_SAM = [0x51, 0x36, 0x03, 0x83, 0x08]
GC_SAM = [0x00, 0x84, 0x00, 0x00, 0x10]
GR_SAM = [0x00, 0xC0, 0x00, 0x00]
WK_SAM = [0x07]

start=time.time()

apdu = SELECT + MF_SAM
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice0.connection.transmit( apdu )
print ' status words: ', "%x %x" % (sw1, sw2)
apdu = SELECT + DF_SAM
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice0.connection.transmit( apdu )
print ' status words: ', "%x %x" % (sw1, sw2)
apdu = SELECT + EF_SAM
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice0.connection.transmit( apdu )
print ' status words: ', "%x %x" % (sw1, sw2)

apdu = GU_SC
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice1.connection.transmit( apdu )
print 'response: ', toHexString(response), ' status words: ', "%x %x" % (sw1, sw2)

apdu = LK_SAM + response + WK_SAM
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice0.connection.transmit( apdu )
print 'response: ', toHexString(response), ' status words: ', "%x %x" % (sw1, sw2)

apdu = GU_SC
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice1.connection.transmit( apdu )
print 'response: ', toHexString(response), ' status words: ', "%x %x" % (sw1, sw2)

apdu = SELECT + MF_SC
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice1.connection.transmit( apdu )
print ' status words: ', "%x %x" % (sw1, sw2)
apdu = SELECT + DF_SCM
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice1.connection.transmit( apdu )
print ' status words: ', "%x %x" % (sw1, sw2)

apdu = GC_SC + WK_SAM
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice1.connection.transmit( apdu )
print ' status words: ', "%x %x" % (sw1, sw2)

apdu = GR_SC + [sw2]
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice1.connection.transmit( apdu )
print 'response: ', toHexString(response), ' status words: ', "%x %x" % (sw1, sw2)

apdu = GC_SAM + response
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice0.connection.transmit( apdu )
print ' status words: ', "%x %x" % (sw1, sw2)

apdu = GR_SAM + [sw2]
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice0.connection.transmit( apdu )
print 'response: ', toHexString(response), ' status words: ', "%x %x" % (sw1, sw2)

apdu = MUA + response
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice1.connection.transmit( apdu )
print ' status words: ', "%x %x" % (sw1, sw2)

apdu = GR_SC + [sw2]
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice1.connection.transmit( apdu )
print 'response: ', toHexString(response),' status words: ', "%x %x" % (sw1, sw2)

apdu = MUA + response
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice0.connection.transmit( apdu )
print ' status words: ', "%x %x" % (sw1, sw2)

apdu = SELECT + EF_SCMP
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice1.connection.transmit( apdu )
print ' status words: ', "%x %x" % (sw1, sw2)

apdu = ENCRIPT + length + KODE1_PRESENSI
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice0.connection.transmit( apdu )
print ' status words: ', "%x %x" % (sw1, sw2)

lengthu= sw2
apdu = GR_SAM + [sw2]
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice0.connection.transmit( apdu )
print 'response: ', toHexString(response),' status words: ', "%x %x" % (sw1, sw2)

apdu = WRITE2 + byte + [lengthu+1] + length + response
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice1.connection.transmit( apdu )
print ' status words: ', "%x %x" % (sw1, sw2)
