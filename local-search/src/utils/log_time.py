from time import time

def log_time( function: callable, *args, **kwargs):
    def wrapper(*args, **kwargs):
        print("Starting run of %s ... " % function.__name__)
        start = time()
        ret = function(*args, **kwargs)
        end = time()
        elapsed = end - start
        print("Finished run of %s in %d seconds." % (function.__name__, elapsed))
        return ret

    return wrapper
