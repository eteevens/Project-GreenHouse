import datetime
from datetime import datetime
from datetime import timedelta

def get_current_time():
    current_time = datetime.now().time().isoformat('minutes') #HHMM
    current_day = datetime.now().date()
    print('Current time is ', current_time)
    print('Current date is ', current_day)
    return current_time
    
#get_current_time()

current_day = datetime.now().date()
print('Current date is ', current_day)
next_day = current_day + timedelta(days=1)
print('Next date is ', next_day)