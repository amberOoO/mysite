from django.db import models


# Create your models here.


class AffairInfo(models.Model):
    affairId = models.BigAutoField(primary_key=True)
    affairProviderId = models.ForeignKey('login.AccountInfo', on_delete=models.CASCADE)
    affairName = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    tag = models.CharField(max_length=50, null=True, blank=True)
    affairDetail = models.CharField(max_length=400, null=True, blank=True)
    affairCreateTime = models.DateTimeField()
    rewardType = models.CharField(max_length=1, default='0')  # 0代表奖励为钱，1代表是物品
    rewardMoney = models.FloatField(default=0)
    rewardThing = models.CharField(max_length=30, default='nothing')
    NeedReceiverNum = models.IntegerField()
    receiverNum = models.IntegerField(default=0)


class AffairImg(models.Model):
    affair = models.ForeignKey('affair.AffairInfo', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='affairImg')
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
