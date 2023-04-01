from django.db import models
"""
Use if the number of QuerySets to the model database is very large (exceeds 3000 - 5000).
A custom model that breaks the received data into parts after a QuerySet to the database.
The number of records in one part is indicated in the attribute - chunksize.
Called by Image.objects..chunk_iterator(2000)
"""
class ChunkIteratorManager(models.query.QuerySet):

    def chunk_iterator(self, chunksize=1000):
        current = 0
        total = self.count()

        while current < total:
            yield self[current: current + chunksize]
            current += chunksize


class CustomChunkIteratorModel(models.Model):   # if we need imitation only from models.Model
    objects = ChunkIteratorManager.as_manager()     # redefine the attribute objects


class CustomChunkIteratorModelMixin():  # if we need to make imitation from different models
    objects = ChunkIteratorManager.as_manager()
