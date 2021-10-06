import time
import math
import random

PX = 37.7952755906
# 1 centimeter = 37.7952755906 pixels

def cm2px(cm):
    """
    Convert from centimeter to pixels

    Parameters
    cm: length(s) in centimeters, whether single value, tuple or list

    Return
    length(s) in pixels, whether single value, tuple or list
    """
    if type(cm) is float or type(cm) is int:
        return round(cm * PX)
    elif type(cm) is tuple:
        return tuple([round(item * PX) for item in cm])
    elif type(cm) is list:
        return [round(item * PX) for item in cm]
    raise ValueError('\'cm\' type should be float, int, tuple or list!')

def random_color():
    """
    Randomize a bright RGB color

    Return
    tuple of 3 random numbers representing red, green and blue values
    """

    def gen():
        return round(10 * math.sqrt(random.randint(100, 255)))

    return (gen(), gen(), gen())

def get_current_time():
    """
    Local time getter function

    Return
    time formatted like: 'Fri Aug 16 14:13:41 2019'
    """
    return time.asctime(time.localtime(time.time()))

def info_log(message):
    """
    Logging function for information
    """
    print('info: %s] %s' % (get_current_time(), message))

def warning_log(message):
    """
    Logging function for warnings
    """
    print('warning: %s] %s' % (get_current_time(), message))

def error_log(message, is_exit):
    """
    Logging function for errors

    Raise
    raises a 'SystemExit' error if 'is_exit' is True
    """
    print('error: %s] %s' % (get_current_time(), message), file=sys.stderr)
    if is_exit:
        raise SystemExit(message)
