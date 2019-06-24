from django.db import models

# Create your models here.
class Discuss(models.Model):
    id = models.BigAutoField(primary_key=True)
    affairId = models.ForeignKey('affair.AffairInfo', on_delete=models.CASCADE)
    createTime = models.DateTimeField()
    content = models.CharField(max_length=300)

    def __str__(self):
        return str(self.id)

class Discuss_Account(models.Model):
    id = models.BigAutoField(primary_key=True)
    createrId = models.BigIntegerField()
    discussId = models.ForeignKey('discuss.Discuss', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
