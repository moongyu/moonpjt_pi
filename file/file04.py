import time
import datetime

log_cnt = 0;

now = datetime.datetime.now()
now_time = now.time()
now_str = now.strftime('%H %M %S')

event_time_sleep = datetime.datetime(2019,10,3,21,3,30,30)
event_time_sleep = event_time_sleep.time()
event_time_sleep_str = event_time_sleep.strftime('%H %M %S')
event_time_wakeup = datetime.datetime(2019,11,3,22,57,0,0)
event_time_wakeup = event_time_wakeup.time()
event_time_wakeup_str = event_time_wakeup.strftime('%H %M %S')

#file = open('text01.txt','a')

#for i in range(1,6):
#    data = '%d\n'%i

    #file.write(data)
    #file.write(now_str + '\n')
    #log_cnt = log_cnt + 1
    #file.write(str(log_cnt) + ' hello ' + ' : ' + now_str + '\n')

try:
    while True:
        now = datetime.datetime.now()
        now_str = now.strftime('%H %M %S')

        if now_str == event_time_wakeup_str :
            file = open('text01.txt','a')
            #log_cnt = log_cnt + 1
            file.write('wakeup ' + now_str + '\n')
            file.close()
            #print(1)
        #else :
            #print(2)

#print(now_time)
#print(event_time_wakeup)
except KeyboardInterrupt:
    print(3)
#    exit_th = 0