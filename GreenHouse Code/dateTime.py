import datetime
from datetime import datetime

def get_current_time():
    current_time = datetime.now().time().isoformat('minutes') #HHMM
    print('Current time is ', current_time)
    return current_time
    

time = get_current_time()