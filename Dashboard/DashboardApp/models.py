from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Record(models.Model):
    User = models.CharField(max_length=50)
    Time_stamp = models.DateTimeField(auto_now_add=True, blank=True)
    Temperature = models.FloatField(default=0,null=True)
    Humidity = models.FloatField(default=0,null=True)
    AQI = models.FloatField(default=0,null=True)
    Body_Temperature = models.FloatField(default=0,null=True)

    def __str__(self):
        return str(self.User + ' at ' + str(self.Time_stamp))

class Profile(models.Model):
    username = models.CharField(max_length=50,default="Null")
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    sex = models.CharField(max_length=10,null=True)
    age = models.IntegerField(null=True)
    weight = models.FloatField(null=True)
    height = models.FloatField(null=True)
    blood_group = models.CharField(null=True,max_length=10)

    def __str__(self):
            return f'{self.user.username} Profile' #show how we want it to be displayed

