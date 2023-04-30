from django.db import models


class Measures(models.IntegerChoices):    # or class Measures(IntEnum): from enum import IntEnum # activate 21 str
    milligrams = 0
    grams = 1
    pieces = 2
