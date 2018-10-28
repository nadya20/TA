def isLecture():
    readResult = False

    # logic to get data
    return readResult

def readData(isDosen):
    # logic to read data

    name = "alif" # empty on student
    id = "1103132163"
    courses = [Course("CS0121", "90"), Course("CS0121", "90")] # only one on lecture

    return name, id, courses


def confirmCourseMatch(lectureCourse, studentCourses):
    for idx, course in enumerate(studentCourses):
        if lectureCourse.subject == course.subject:
            return idx
    
    return -1 # not found


def logCurrentCourse(course, attendanceCount):
    # logic to save it
    pass


