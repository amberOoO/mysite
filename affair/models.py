from django.db import models


# Create your models here.


class AffairInfo(models.Model):
    affairId = models.BigAutoField(primary_key=True)
    affairProviderId = models.ForeignKey('login.AccountInfo', on_delete=models.CASCADE)
    affairName = models.CharField(max_length=50, default='null')
    type = models.CharField(max_length=50)
    tag = models.CharField(max_length=50, null=True, blank=True)
    affairDetail = models.CharField(max_length=500, null=True, blank=True)
    affairCreateTime = models.DateTimeField()
    lastUpdateTime = models.DateTimeField()
    rewardType = models.CharField(max_length=1, default='0')  # 0代表奖励为钱，1代表是物品
    rewardMoney = models.FloatField(default=0)
    rewardThing = models.CharField(max_length=30, default='nothing')
    needReceiverNum = models.IntegerField()
    receiverNum = models.IntegerField(default=0)
    statusFlag = models.CharField(max_length=1, default='0')

    def __str__(self):
        return self.affairName


class AffairImg(models.Model):
    affair = models.ForeignKey('affair.AffairInfo', on_delete=models.DO_NOTHING)
    img = models.ImageField(upload_to='affairImg', max_length=80)
    name = models.CharField(max_length=80)

    def __str__(self):
        return str(self.id)


class Affair_AffairReceiver(models.Model):
    id = models.BigAutoField(primary_key=True)
    affairId = models.ForeignKey("affair.AffairInfo", on_delete=models.CASCADE)
    affairReceiverId = models.ForeignKey("login.AccountInfo", on_delete=models.CASCADE)

    def __str__(self):
        return self.id
