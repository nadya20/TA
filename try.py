Python 3.4.2 (default, Oct 19 2014, 13:31:11) 
[GCC 4.9.1] on linux
Type "copyright", "credits" or "license()" for more information.
>>> from smartcard.System import readers
>>> from smartcard.util import toHexString
>>>
>>> r=readers()
>>> print r
['SchlumbergerSema Reflex USB v.2 0', 'Utimaco CardManUSB 0']
>>> connection = r[0].createConnection()
>>> connection.connect()
>>> SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
>>> DF_TELECOM = [0x7F, 0x10]
>>> data, sw1, sw2 = connection.transmit( SELECT + DF_TELECOM )
>>> print "%x %x" % (sw1, sw2)
9f 1a
>>>
