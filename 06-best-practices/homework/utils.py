from datetime import datetime

def dt(hour, minute, second=0):
    '''
    converts hour and minute input as datetime format
    '''
    return datetime(2023, 1, 1, hour, minute, second)
