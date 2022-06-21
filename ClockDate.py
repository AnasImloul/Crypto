from datetime import datetime


def todayDate():
    today = datetime.now()
    
    today = today.strftime("%d/%m/%Y")
    return today

    
    
def clockTime():
    now = datetime.now()
    
    now = now.strftime("%H:%M:%S")
    return now
    
    
