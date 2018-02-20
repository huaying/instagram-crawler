from time import sleep


def instagram_int(string):
    return int(string.replace(',', ''))


def retry(attempt=10, wait=0.3):
    def wrap(func):
        def wrapped_f(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                if attempt > 0:
                    sleep(wait)
                    retry(attempt - 1, wait)(func)(*args, **kwargs)
        return wrapped_f
    return wrap