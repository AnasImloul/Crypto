from ClockDate import todayDate,clockTime



def getLastDate(lines):
    #return the last date value in the text file
    for i in range(len(lines)-1,-1,-1):
        line = lines[i]
        
        if len(line.split("/"))==3: #line containing date format : "dd/mm/yyyy"
            
            return line
    return

def getLastPrice(lines):
    #return the last price value in the text file
    for i in range(len(lines)-1,-1,-1):
        line = lines[i].split()
        if len(line)==2: # line containing price format : "clock price"
            try:
                float(line[-1])
                return float(line[-1])
            except:
                continue
    return
   
