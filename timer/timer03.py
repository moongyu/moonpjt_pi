import datetime


now = datetime.datetime.now()
now_time = now.time()
#now_str = now.strftime('%Y %m %d %H %M %S')
now_str = now.strftime('%H %M %S')
#event_time_sleep = now.replace(hour=0, minute=0, microsecond=0)
#event_time_wakeup = now.replace(hour=6, minute=0, microsecond=0)
event_time_sleep = datetime.datetime(2019,10,3,9,6,0)
event_time_sleep = event_time_sleep.time()
event_time_sleep_str = event_time_sleep.strftime('%H %M %S')
event_time_wakeup = datetime.datetime(2019,10,3,9,18,0)
event_time_wakeup = event_time_wakeup.time()
event_time_wakeup_str = event_time_wakeup.strftime('%H %M %S')

now = datetime.datetime.now()
now_time = now.time()
now_str = now.strftime('%H %M %S')

def start_timer_500ms():
    global now
    global now_time
    global now_str
    global log_cnt
	
    if exit_th == 1 :
        timer_500ms=threading.Timer(0.5,start_timer_500ms)
        timer_500ms.start()

        now = datetime.datetime.now()
        now_time = now.time()
        now_str = now.strftime('%H %M %S')
        
        if now_str == event_time_sleep_str :
            file = open('log_mobile.txt','a')
            log_cnt = log_cnt + 1
            file.write(str(log_cnt) + ' : ' + 'sleep ' + now_str + '\n')
            file.close()
        if now_str == event_time_wakeup_str :
            file = open('log_mobile.txt','a')
            log_cnt = log_cnt + 1
            file.write(str(log_cnt) + ' : ' + 'wakeup ' + now_str + '\n')
            file.close()
            
if now_time >= event_time_wakeup :
    #file = open('log_mobile.txt','a')
    #log_cnt = log_cnt + 1
    #file.write(str(log_cnt) + ' : ' + 'sleep ' + now_str + '\n')
    #file.close()
    print('1')
if now_time < event_time_wakeup :
    #file = open('log_mobile.txt','a')
    #log_cnt = log_cnt + 1
    #file.write(str(log_cnt) + ' : ' + 'wakeup ' + now_str + '\n')
    #file.close()
    print('0')
            
