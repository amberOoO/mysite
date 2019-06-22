from django.db import models

# Create your models here.

class CommentInfo(models.Model):
    commentId = models.BigAutoField(primary_key=True)
    Order_Account_id = models.ForeignKey('order.Order_Account', models.CASCADE)
    commentTime = models.DateTimeField()
    commentContent = models.CharField(max_length=500)

    def __str__(self):
        return self.commentId