import CardReader as cr
import time

def waitUntilLectureCome():
    pass

def isLecture():
    try:
        cardReq = cr.createCardReq(cr.Person.ATR)
        readResult = cr.readLecture(cardReq)    
        return isinstance(readResult, cr.Lecture), readResult
    except:
        print "card removed"
        return False, None


def isStudent():
    try:
        cardReq = cr.createCardReq(cr.Person.ATR)
        readResult = cr.readStudent(cardReq)

        return isinstance(readResult, cr.Student), readResult
    except:
        print "card removed"
        return False, None


def confirmCourseMatch(lecture, student):
    start = time.time()
    for idx, course in enumerate(student.courses):
        if lecture.subject == course.subject:
            return True, idx

    end = time.time()
    print 'confirmCourseMatch:time', (end-start)
    
    return False, -1 # not found


def addStudentAttendance(student, courseIndex):
    personCardReq = cr.createCardReq(cr.Person.ATR)
    samCardReq = cr.createCardReq(cr.Sam.ATR)

    isWriteSuccess = cr.writeStudentCourse(personCardReq, samCardReq, courseIndex, student.courses[courseIndex].attendance, 1)
    if isWriteSuccess:
        return True, student.courses[courseIndex].attendance + 1
    else:
        return False, student.courses[courseIndex].attendance


if __name__ == "__main__":
    isLec, lecture = isLecture() # blocking process

    student = None
    while student == None:
        isStu, student = isStudent() # blocking process

    found, idx = confirmCourseMatch(lecture, student)

    print cr.writeStudentCourse(cr.createCardReq(cr.Person.ATR), cr.createCardReq(cr.Sam.ATR), idx, student.courses[idx].attendance)