# encoding=utf-8
import time


class Time_tools:
    def get_time(self):
        tim = time.strftime("%H")
        if (int(tim) % 2) == 0:
            return int(tim)
        else:
            return int(tim) + 1


if __name__ == '__main__':
    tim = Time_tools().get_time()
    print(str(tim) + ':00-' + str(tim + 2) + ':00')
