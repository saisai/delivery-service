import pytz
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from django.utils import timezone


class SQCount(models.Subquery):
    template = '(SELECT count(*) FROM (%(subquery)s) _count)'
    output_field = models.IntegerField()


class ArraySubquery(models.Subquery):
    template = 'ARRAY(%(subquery)s)'


class StringArraySubquery(ArraySubquery):
    output_field = ArrayField(base_field=models.CharField(max_length=255))


class TimeZoneProvider:
    def __init__(self):
        self.tz = pytz.timezone('Asia/Bishkek')

    def get_date_according_to_timezone(self):
        current_date = timezone.now().astimezone(self.tz)
        return current_date

    def get_date_in_local_timezone(self, filter_by_time):
        return self.tz.localize(filter_by_time)
