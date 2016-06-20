def deltaTimeTrue(past,present,period):
    delta = int(present) - int(past)
    if delta >= period:
        return 1
    else:
        return 0
