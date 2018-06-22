from time import sleep
import random

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


def randmized_sleep(average = 1):
    _min, _max = average * 1/2, average * 3/2
    sleep(random.uniform(_min, _max))


def validate_posts(dict_posts):
    '''
        The validator is to verify if the posts are fetched wrong.
        Ex. the content got messed up or duplicated.
    '''
    posts = dict_posts.values()
    contents = [post['content'] for post in posts]
    assert len(set(contents)) == len(contents)
    print('These post data should be correct.')
