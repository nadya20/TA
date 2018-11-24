from smartcard.CardType import ATRCardType
from smartcard.CardConnection import CardConnection
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes, hl2bs, bs2hl
import time

class Data(object):
    def __init__(self, isSuccess = False, response = None, sw2 = None):
        self.isSuccess = isSuccess
        self.response = response
        self.sw2 = sw2

    def __repr__(self):
        return str(self.isSuccess) + " " + str(self.response) + " " + str(self.sw2)

class Course(object):
    def __init__(self, subject = "CS0121", attendace = 90):
        self.subject = subject
        self.attendance = attendace

    def __repr__(self):
        return str(self.subject) + " " + str(self.attendance)

class Card(object):
    SELECT = [0x00, 0xA4, 0x00, 0x00, 0x02]
    MF_SC = [0x3F, 0x00] 
    OPEN_SUCCESS = 0x61
    READ_SUCCESS = 0x90

    GR_SC = [0x00, 0xC0, 0x00, 0x00]
    GC_SC=	[0x00, 0x84, 0x00, 0x00, 0x01]
    GU_SC = [0x00, 0xCA, 0x00, 0x00, 0x07]

class Person(Card):
    ATR = toBytes("3B 13 96 13 09 17")

class Lecture(Person):
    DF_SC = [0x40, 0x00]
    EF_SC = [0x40, 0x01] 
    READ = [0x00, 0xB0, 0x00, 0x00]
    LENGTH= [0x36]

    def __init__(self, id, name, subject):
        self.id = id
        self.name = name
        self.subject = subject

    def __repr__(self):
        return self.id + " " + self.name + " " + self.subject

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
        LENGTH_WRITE = [0x03]

    def __repr__(self):
        return self.id + " " + str(self.courses)

class Sam(Card):
    ATR = toBytes("3B 10 96")
    MUA = [0x00, 0x82, 0x00, 0x00, 0x10]

    WRITE2 = [0x00, 0xD0] 
    ENCRIPT= [0x51, 0x33, 0x00, 0x00]
    LENGTH= [0x09]
    # byte = [0x00, 0x00]

    KODE1_PRESENSI= [0x45,0x4C,0x48,0x34,0x41,0x33,0x31,0x00,0x00] # XXXAAA100
    
    DF_SAM = [0x40, 0x00]
    EF_SAM = [0x40, 0x02]
    LK_SAM = [0x51, 0x36, 0x03, 0x83, 0x08]
    GC_SAM = [0x00, 0x84, 0x00, 0x00, 0x10]
    GR_SAM = [0x00, 0xC0, 0x00, 0x00]
    WK_SAM = [0x07]


def __transmit(cardService, apduSelect, expectedSw1):
    response, sw1, sw2 = cardService.connection.transmit(apduSelect)
    # print response, sw1, sw2
    # return isSucces and responce
    return Data(sw1 == expectedSw1, response, sw2)


def __splitCourse(chunk):
    course = hl2bs(chunk[:-3])
    temp_attendace = hl2bs(chunk[-3:])
    attendace = int(temp_attendace) if temp_attendace.isdigit() else 0
    return Course(course, attendace)

start=time.time()
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

    service.connection.disconnect()
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

    service.connection.disconnect()
    return courses
end=time.time()
print 'time',(end-start)

start=time.time()
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

    service.connection.disconnect()
    return Lecture(NIP, NAMA, MATKUL)
end=time.time()
print 'time',(end-start)

def readStudent(cardResquest):
    nim = __readStudentId(cardResquest)
    courses = __readStudentCourse(cardResquest)

    if nim is not None and courses is not None:
        return Student(nim, courses)
    else:
        return None

# try to write to student card
# add 10 as default value to current attendance
start=time.time()
def writeStudentCourse(cardResquestSc, cardResquestSam, courseIndex, currentAttendance, addedValue=10):
    serviceSc = cardResquestSc.waitforcard()
    serviceSc.connection.connect()

    serviceSam = cardResquestSam.waitforcard()
    serviceSam.connection.connect()
    # MF Sam call
    apdu = Card.SELECT + Card.MF_SC
    data = __transmit(serviceSam, apdu, Card.OPEN_SUCCESS)

    if (not data.isSuccess): return False # wrong card

    # DF Sam call
    apdu = Card.SELECT + Sam.DF_SAM
    data = __transmit(serviceSam, apdu, Card.OPEN_SUCCESS)

    if (not data.isSuccess): return False # wrong card

    # EF Sam call
    apdu = Card.SELECT + Sam.EF_SAM
    data = __transmit(serviceSam, apdu, Card.OPEN_SUCCESS)

    if (not data.isSuccess): return False # wrong card

    # GU Sc call
    apdu = Sam.GU_SC
    data = __transmit(serviceSc, apdu, Card.READ_SUCCESS)

    if (not data.isSuccess): return False # wrong card

    # LK and WK call
    apdu = Sam.LK_SAM + data.response + Sam.WK_SAM
    data = __transmit(serviceSam, apdu, Card.READ_SUCCESS)

    if (not data.isSuccess): return False # wrong card

    # MF sc call
    apdu = Card.SELECT + Card.MF_SC
    data = __transmit(serviceSc, apdu, Card.OPEN_SUCCESS)

    if (not data.isSuccess): return False # wrong card
    
    # DF sc call
    apdu = Card.SELECT + Student.DF_SC
    data = __transmit(serviceSc, apdu, Card.OPEN_SUCCESS)

    if (not data.isSuccess): return False # wrong card

    # GC sc call
    apdu = Card.GC_SC + Sam.WK_SAM
    data = __transmit(serviceSc, apdu, Card.OPEN_SUCCESS)

    if (not data.isSuccess): return False # wrong card

    # GR sc call
    apdu = Card.GR_SC + [data.sw2]
    data = __transmit(serviceSc, apdu, Card.READ_SUCCESS)

    if (not data.isSuccess): return False # wrong card

    # GC sam call
    apdu = Sam.GC_SAM + data.response
    data = __transmit(serviceSam, apdu, Card.OPEN_SUCCESS)

    if (not data.isSuccess): return False # wrong card

    # GR sam call
    apdu = Sam.GR_SAM + [data.sw2]
    data = __transmit(serviceSam, apdu, Card.READ_SUCCESS)

    if (not data.isSuccess): return False # wrong card

    # MUA SC call
    apdu = Sam.MUA + data.response
    data = __transmit(serviceSc, apdu, Card.OPEN_SUCCESS)

    if (not data.isSuccess): return False # wrong card

    # GR SC call
    apdu = Card.GR_SC + [data.sw2]
    data = __transmit(serviceSc, apdu, Card.READ_SUCCESS)

    if (not data.isSuccess): return False # wrong card

    # MUA sam call
    apdu = Sam.MUA + data.response
    data = __transmit(serviceSam, apdu, Card.READ_SUCCESS)

    if (not data.isSuccess): return False # wrong card

    # EF Sc call
    apdu = Card.SELECT + Student.Course.EF_SC
    data = __transmit(serviceSc, apdu, Card.OPEN_SUCCESS)

    if (not data.isSuccess): return False # wrong card

    # Write to card BEGIN HERE
    # SAM encript
    attendanceInHex = bs2hl(str(currentAttendance + addedValue))
    attendanceInHex = [0x30]*(3-len(attendanceInHex)) + attendanceInHex # make sure 3 digit to write

    apdu = Sam.ENCRIPT + Student.Course.LENGTH_WRITE + attendanceInHex  ####### TO DO
    data = __transmit(serviceSam, apdu, Card.OPEN_SUCCESS)

    if (not data.isSuccess): return False # wrong card

    # GR sam
    lengthu = data.sw2
    apdu = Sam.GR_SAM + [data.sw2]
    data = __transmit(serviceSam, apdu, Card.READ_SUCCESS)

    if (not data.isSuccess): return False # wrong card

    apdu = Sam.WRITE2 + [0x00, courseIndex * 9 + 6] + [lengthu+1] + Student.Course.LENGTH_WRITE + data.response
    data = __transmit(serviceSc, apdu, Card.READ_SUCCESS)

    serviceSc.connection.disconnect()
    serviceSam.connection.disconnect()
    return data.isSuccess
end=time.time()
print 'time',(end-start)

def createCardReq(cardAtrType):    
    cardtype = ATRCardType(cardAtrType)
    cardrequest = CardRequest(timeout=None, cardType=cardtype)
    return cardrequest


if __name__ == "__main__":
    cardrequestSc = createCardReq(Person.ATR)

    # lecture = readLecture(cardrequestSc)
    # if (lecture != None):
    #     print lecture.id, lecture.name, lecture.subject
    # else:
    #     print "Bukan Dosen cuk"

    student = readStudent(cardrequestSc)

    if (student != None and student.id != None and student.courses != None):
        print student.id, student.courses
    else:
        print "bukan mahasiswa cuk"

    # cardrequestSam = createCardReq(Sam.ATR)

    # print writeStudentCourse(cardrequestSc, cardrequestSam, 2, 10)