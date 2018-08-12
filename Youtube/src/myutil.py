import time

class pcolors:
    CYAN = '\033[36m' # cyan
    PID = '\033[33m' # yellow
    BLUE = '\033[34m' # blue
    EXPT = '\033[31m' # red
    WARNING = '\033[93m' # 진한 yellow
    CRUD = '\033[94m' # okblue

    END = '\033[0m'

class times:
    START = time.clock()

    @classmethod
    def getSpendTime(cls):
        END = time.clock()
        spendTime_sec = int(END - times.START)
        if spendTime_sec < 60:
            print('경과 시간 : ' + str(spendTime_sec) + '초')
        elif spendTime_sec >= 60:
            print('경과 시간 : ' + str(int(spendTime_sec/60)) + '분 ' + str(int(spendTime_sec%60)) + '초')
        elif spendTime_sec >= 3600:
            print('경과 시간 : ' + str(int(spendTime_sec/3600)) + '시간 ' + str(int((spendTime_sec%3600)/60)) + '분 ' + str(int((spendTime_sec%3600)%60)) + '초')

if __name__ == '__main__':
    print('execute the \"mainProcess.py\"!')
    exit()