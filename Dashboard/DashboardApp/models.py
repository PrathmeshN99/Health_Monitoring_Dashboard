from django.db import models

# Create your models here.
class Record(models.Model):
    User = models.CharField(max_length=50)
    Time_stamp = models.DateTimeField(max_length=100)
    Temp = models.IntegerField()

    def __str__(self):
        return str(self.User + ' at ' + str(self.Time_stamp))
