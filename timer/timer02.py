import datetime


now = datetime.datetime.now()
now_time = now.time()
#event_time_sleep = now.replace(hour=0, minute=0, microsecond=0)
#event_time_wakeup = now.replace(hour=6, minute=0, microsecond=0)
event_time_sleep = now.replace(hour=18, minute=10, microsecond=0)
event_time_wakeup = now.replace(hour=18, minute=20, microsecond=0)
DT=datetime.datetime(2019,10,10,20,45,0,0)
D=DT.time()

if now_time >= D :
    print('1')
else :
    print('0')