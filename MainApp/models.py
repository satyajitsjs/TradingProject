from django.db import models

# Create your models here.

class Candle:
    def __init__(self, id, open, high, low, close, date):
        self.id = id
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.date = date