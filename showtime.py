
from datetime import datetime
def show_time():
    n = datetime.now()
    time1=n.strftime('%Y-%m-%d %H:%M:%S')
    time2=n.strftime('%A,%B %d,%Y')
    return f"{time1}\n{time2}"