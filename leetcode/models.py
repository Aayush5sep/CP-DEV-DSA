from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PendingVerification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    leetusername = models.CharField(max_length=100)
    profile_name = models.CharField(max_length=100,null=True,blank=True)
    veri_code = models.CharField(max_length=25)
    req_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.leetusername