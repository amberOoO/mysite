# Create your models here.

from django.db import models


class OrderInfo(models.Model):
    orderId = models.BigAutoField(primary_key=True)
    affairId = models.BigIntegerField(null=True)
    affairProviderId = models.ForeignKey('login.AccountInfo', on_delete=models.CASCADE)
    orderCreateTime = models.DateTimeField()
    orderStatus = models.CharField(max_length=1, default='0')  # '0'为未完成，'1'为完成
    refundFlag = models.CharField(max_length=1, default='0')  # '0'为未申请，'1'为申请状态，'2'为退款中，'3'为完成

    def __str__(self):
        return str(self.orderId)

class Order_Account(models.Model):
    id = models.BigAutoField(primary_key=True)
    orderId = models.ForeignKey('order.OrderInfo', models.CASCADE)
    affairProviderId = models.ForeignKey('login.AccountInfo', on_delete=models.CASCADE, related_name='affairProviderId')
    affairReceiverId = models.ForeignKey('login.AccountInfo', on_delete=models.CASCADE, related_name='affairReceiverId')

    def __str__(self):
        return str(self.id)

