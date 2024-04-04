from datetime import datetime
import random

def numero_unico():
    current_date_time = datetime.now()
    day = current_date_time.day
    month = current_date_time.month
    year = current_date_time.year
    hour = current_date_time.hour
    minute = current_date_time.minute
    second = current_date_time.second


    total = day + month + year + hour + minute + second


    return int(total)