from pymongo.errors import BulkWriteError


def ignore_dups(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BulkWriteError:
            pass

    return wrapper
