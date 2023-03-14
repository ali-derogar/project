from calendar import month
from . import jalali
from django.utils import timezone
from .num_changer import number_changer
from .mon_changer import month_changer

def time_convertor(time):
    time_real = timezone.localtime(time)
    time_now = ','.join([str(i) for i in [time_real.year ,time_real.month ,time_real.day]])
    per_time = jalali.Gregorian(time_now).persian_tuple()
    year = number_changer(str(per_time[0]))
    month = month_changer(per_time[1])
    day = number_changer(str(per_time[2]))
    hour = time_real.hour
    minute = time_real.minute
    second = time_real.second
    time_main = "{}:{}:{}".format(hour,minute,second)
    time_main = number_changer(time_main)
    

    return "{}/{}/{} <==> {}".format(year,month,day,time_main)

