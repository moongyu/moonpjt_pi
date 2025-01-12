import time
import datetime

log_cnt = 0;

now = datetime.datetime.now()
now_time = now.time()
now_str = now.strftime('%Y %m %d %H %M %S')

event_time_wakeup = datetime.datetime(2019,10,3,21,0,0,0)
event_time_wakeup = event_time_wakeup.time()

file = open('text01.txt','a')

for i in range(1,6):
    data = '%d\n'%i

    #file.write(data)
    #file.write(now_str + '\n')
    log_cnt = log_cnt + 1
    file.write(str(log_cnt) + ' hello ' + ' : ' + now_str + '\n')

file.close()

