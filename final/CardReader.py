from smartcard.CardType import ATRCardType
from smartcard.CardConnection import CardConnection
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes, hl2bs
import time

class Data(object):
    def __init__(self, isSuccess = False, response = None):
        self.isSuccess = isSuccess
        self.response = response

class Course(object):
    def __init__(self, subject = "CS0121", attendace = "90"):
        self.subject = subject
        self.attendance = attendace

    def __repr__(self):
        return (self.subject, self.attendance)

class Card(object):
    SELECT = [0x00, 0xA4, 0x00, 0x00, 0x02]
    OPEN_SUCCESS = 0x61
    READ_SUCCESS = 0x90

class Person(Card):
    ATR = toBytes("3B 13 96 13 09 17")
    MF_SC = [0x3F, 0x00] 

class Lecture(Person):
    DF_SC = [0x40, 0x00]
    EF_SC = [0x40, 0x01] 
    READ = [0x00, 0xB0, 0x00, 0x00]
    LENGTH= [0x36]

    def __init__(self, id, name, subject):
        self.id = id
        self.name = name
        self.subject = subject

class Student(Person):
    DF_SC = [0x50, 0x00]
    READ = [0x00, 0xB0, 0x00, 0x00]

    def __init__(self, id, courses = []):
        self.id = id
        self.courses = courses

    class ID (object):
        EF_SC = [0x50, 0x01]
        LENGTH = [0x10]

    class Course (object):
        EF_SC = [0x50, 0x02]
        LENGTH = [0x48]

class Xamp(Card):
    ATR = toBytes("3B 13 96 13 09 17")
    MUA = [0x00, 0x82, 0x00, 0x00, 0x10]

    WRITE2 = [0x00, 0xD0] 
    ENCRIPT= [0x51, 0x33, 0x00, 0x00]
    LENGTH= [0x09]
    # byte = [0x00, 0x00]

    KODE1_PRESENSI= [0x45,0x4C,0x48,0x34,0x41,0x33,0x31,0x00,0x00] # XXXAAA100

    GR_SC = [0x00, 0xC0, 0x00, 0x00]
    GC_SC=	[0x00, 0x84, 0x00, 0x00, 0x01]
    GU_SC = [0x00, 0xCA, 0x00, 0x00, 0x07]
    
    EF_SAM = [0x40, 0x02]
    LK_SAM = [0x51, 0x36, 0x03, 0x83, 0x08]
    GC_SAM = [0x00, 0x84, 0x00, 0x00, 0x10]
    GR_SAM = [0x00, 0xC0, 0x00, 0x00]
    WK_SAM = [0x07]


def __transmit(cardService, apduSelect, expectedSw1):
    response, sw1, _ = cardService.connection.transmit(apduSelect)

    # return isSucces and responce
    return Data(sw1 == expectedSw1, response)


def __splitCourse(chunk):
    course = hl2bs(chunk[:-3])
    attendace = hl2bs(chunk[-3:])
    return Course(course, attendace)


def __readStudentId(cardResquest):
    service = cardResquest.waitforcard()
    service.connection.connect()
    
    # Call MF 
    apdu = Card.SELECT + Person.MF_SC
    data = __transmit(service, apdu, Card.OPEN_SUCCESS)

    if (not data.isSuccess): return None # wrong card

    # Call DF
    apdu = Card.SELECT + Student.DF_SC
    data = __transmit(service, apdu, Card.OPEN_SUCCESS)
    if (not data.isSuccess): return None # not a lecture

    # Call EF
    apdu = Card.SELECT + Student.ID.EF_SC
    data = __transmit(service, apdu, Card.OPEN_SUCCESS)
    if (not data.isSuccess): return None # wrong card
    
    # Call READ
    apdu = Student.READ + Student.ID.LENGTH
    data = __transmit(service, apdu, Card.READ_SUCCESS)
    if (not data.isSuccess): return None # wrong card

    # DATA
    NIM = hl2bs(data.response[:10])

    return NIM


def __readStudentCourse(cardResquest):
    service = cardResquest.waitforcard()
    service.connection.connect()
    
    # Call MF 
    apdu = Card.SELECT + Person.MF_SC
    data = __transmit(service, apdu, Card.OPEN_SUCCESS)

    if (not data.isSuccess): return None # wrong card

    # Call DF
    apdu = Card.SELECT + Student.DF_SC
    data = __transmit(service, apdu, Card.OPEN_SUCCESS)
    if (not data.isSuccess): return None # not a lecture

    # Call EF
    apdu = Card.SELECT + Student.Course.EF_SC
    data = __transmit(service, apdu, Card.OPEN_SUCCESS)
    if (not data.isSuccess): return None # wrong card
    
    # Call READ
    apdu = Student.READ + Student.Course.LENGTH
    data = __transmit(service, apdu, Card.READ_SUCCESS)
    if (not data.isSuccess): return None # wrong card

    # DATA
    # NIM = hl2bs(data.response[:10])
    
    chunks = [ data.response [i*9 : i*9 + 9] for i in range(8)]
    courses = [__splitCourse(chunk) for chunk in chunks]

    return courses


def readLecture(cardResquest):
    service = cardResquest.waitforcard()
    service.connection.connect()
    
    # Call MF 
    apdu = Card.SELECT + Lecture.MF_SC
    data = __transmit(service, apdu, Card.OPEN_SUCCESS)

    if (not data.isSuccess): return None # wrong card

    # Call DF
    apdu = Card.SELECT + Lecture.DF_SC
    data = __transmit(service, apdu, Card.OPEN_SUCCESS)
    if (not data.isSuccess): return None # not a lecture

    # Call EF
    apdu = Card.SELECT + Lecture.EF_SC
    data = __transmit(service, apdu, Card.OPEN_SUCCESS)
    if (not data.isSuccess): return None # wrong card
    
    # Call READ
    apdu = Lecture.READ + Lecture.LENGTH
    data = __transmit(service, apdu, Card.READ_SUCCESS)
    if (not data.isSuccess): return None # wrong card


    # DATA
    NIP = hl2bs(data.response[:10]) 
    # [10:15] is empty
    NAMA = hl2bs(data.response[16:-14])         
    # [-14:48] is empty
    MATKUL = hl2bs(data.response[48:])

    return Lecture(NIP, NAMA, MATKUL)


def readStudent(cardrequest):
    nim = __readStudentId(cardrequest)
    courses = __readStudentCourse(cardrequest)

    return Student(nim, courses)


if __name__ == "__main__":
    cardtype1 = ATRCardType(Person.ATR)
    cardrequest1 = CardRequest(timeout=None, cardType=cardtype1)

    # lecture = readLecture(cardrequest1)
    # if (lecture != None):
    #     print lecture.id, lecture.name, lecture.subject
    # else:
    #     print "Bukan Dosen cuk"

    student = readStudent(cardrequest1)

    if (student.id != None and student.courses != None):
        print student.id, student.courses
    else:
        print "bukan mahasiswa cuk"