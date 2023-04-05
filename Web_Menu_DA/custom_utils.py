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
