def deltaTimeTrue(past,present,period):
    delta = int(present) - int(past)
    if delta >= period:
        return 1
    else:
        return 0

def deltaTime(past,present):
    delta = int(present) - int(past)
    return delta

def timeParse(time):
    sec = time % 60
    time = time / 60
    mins = time % 60
    time = time / 60
    hours = time % 24
    time = time / 24
    string = "Hours "+str(hours)
    string += ", Minutes "+str(mins)
    string += ", Seconds "+str(sec)
    return string
