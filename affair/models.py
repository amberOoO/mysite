from django.db import models
# Create your models here.

class AffairInfo(models.Model):
    affairId = models.BigIntegerField(primary_key=True)
    affairProviderId = models.ForeignKey('login.AccountInfo',on_delete=models.CASCADE)
    type = models.CharField(max_length=30)
    tag = models.CharField(max_length=30,null=True,blank=True)
    affairDetail = models.CharField(max_length=400,null=True,blank=True)
    affairCreateTime = models.DateTimeField()
    reward = models.FloatField()
    receiverNum = models.IntegerField()

class IMG(models.Model):
    img = models.ImageField(upload_to='img')
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name