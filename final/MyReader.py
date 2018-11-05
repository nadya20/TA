import CardReader as cr

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
    for idx, course in enumerate(student.courses):
        if lecture.subject == course.subject:
            return True, idx
    
    return False, -1 # not found


def logCurrentCourse(course, attendanceCount):
    # logic to save it
    pass


if __name__ == "__main__":
    print isStudent()