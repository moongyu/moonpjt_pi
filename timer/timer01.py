import datetime

now = datetime.datetime.now()
print(now)

Date = now.strftime('%Y-%m-%d')
print(Date)

Time = now.strftime('%H:%M:%S')
print(Time)


#################################
Time = now.strftime('%H:%M')
print(Time)

event_time=now.replace(hour=0, minute=0, microsecond=0)
event_time_01=now.replace(hour=23,minute=0,microsecond=0)

if now > event_time :
    print('ture')
else :
    print('false')
    
if event_time > event_time_01 :
    print('ture01')
else :
    print('false01')
    
test_time = now.time()