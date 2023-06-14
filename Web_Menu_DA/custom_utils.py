from functools import wraps

"""
Use if the number of QuerySets to the model database is very large (exceeds 3000 - 5000)
A custom model that breaks the received data into parts after a QuerySet to the database.
The number of records in one part is indicated in the attribute - chunksize
"""

def custom_queryset_iterator(queryset, chunksize=1000):
    current = 0
    total = queryset.count()

    while current < total:
        yield queryset[current: current + chunksize]
        current += chunksize


def http_methods_for_2fa(request_method_list):
    """
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            for arg in args:
                if arg.method not in request_method_list:
                    # arg.__setattr__('mark', True)
                    setattr(arg, 'mark', True)
            return func(request, *args, **kwargs)

        return inner

    return decorator
