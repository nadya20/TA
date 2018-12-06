from datetime import datetime
import os.path
import time

class Recorder(object):
    def __init__(self, cur_dir):
        self.filename = cur_dir + "/logs/" + str(datetime.now()) + ".csv"
        _file = open(self.filename, "a")
        head = "time;lecturer;total attendance\n"
        _file.writelines(head)
        _file.close()

    def storeCurrentData(self, lecture, total_student):
        start = time.time()
        
        _file = open(self.filename, "a")
        line = str(datetime.now())+ ";" + str(lecture) + ";" + str(total_student) + "\n"
        _file.writelines(line)
        _file.close()

        end = time.time()
        print 'storeCurrentData:time,', (end-start)

if __name__ == "__main__":
    file_dir = os.path.dirname(os.path.abspath(__file__))
    recorder = Recorder(file_dir)

    recorder.storeCurrentData("alif", 10)