from smartcard.CardType import ATRCardType
from smartcard.CardConnection import CardConnection
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes, hl2bs
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
MF_SCM = [0x3F, 0x00]
DF_SCM = [0x50, 0x00]
EF_SCN = [0x50, 0x01]
EF_SCP = [0x50, 0x02]
READ = [0x00, 0xB0, 0x00, 0x00]
lengthn= [0x10]
lengthp= [0x48]


MATKUL=[0x00]
MATKULM=[0x00]

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

MATKUL=hl2bs(response[48:])
print 'matkul: ', (MATKUL)
a=MATKUL
if(a!=0):
apdu = SELECT + MF_SCM
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice1.connection.transmit( apdu )
print ' status words: ', "%x %x" % (sw1, sw2)
apdu = SELECT + DF_SCM
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice1.connection.transmit( apdu )
print ' status words: ', "%x %x" % (sw1, sw2)
apdu = SELECT + EF_SCP
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice1.connection.transmit( apdu )
print ' status words: ', "%x %x" % (sw1, sw2)
apdu = READ + lengthp
print 'sending ' + toHexString(apdu)
response, sw1, sw2 = cardservice1.connection.transmit( apdu )
print 'response: ', toHexString(response), ' status words: ', "%x %x" % (sw1, sw2)

MATKULM=hl2bs(response[9:-9])
print 'matkul: ', (MATKULM)

end=time.time()
print 'time',(end-start)
