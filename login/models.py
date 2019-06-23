from django.db import models
# Create your models here.


class AccountInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    phoneNumber = models.CharField(max_length=20)
    passwd = models.CharField(max_length=20)
    studentNo = models.CharField(max_length=20, default='')
    school = models.CharField(max_length=50, default='')
    nickName = models.CharField(max_length=50, default='newUser')
    mailAddress = models.CharField(max_length=30, null=True, blank=True, unique=True)
    credit = models.FloatField(default=10)
    jurisdiction = models.CharField(max_length=1, default='1')
    nowJurisdiction = models.CharField(max_length=1, null=True, blank=True)

    def __str__(self):
        return self.phoneNumber
