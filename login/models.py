from django.db import models
# Create your models here.


class AccountInfo(models.Model):
    id = models.AutoField(primary_key=True)
    passwd = models.CharField(max_length=20)
    school = models.CharField(max_length=50, null=True, blank=True)
    nickName = models.CharField(max_length=50, default='newUser')
    mailAddress = models.CharField(max_length=30, null=True, blank=True, unique=True)
    phoneNumber = models.CharField(max_length=20)
    credit = models.FloatField(default=10)
    jurisdiction = models.CharField(max_length=1, default='1')
    nowJurisdiction = models.CharField(max_length=1, null=True, blank=True)

    def __str__(self):
        return self.phoneNumber
