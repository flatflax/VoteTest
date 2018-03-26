from django.db import models


# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=100)
    user_password = models.CharField(max_length=30)
    email = models.CharField(max_length=100, default='')
    user_right = models.IntegerField(default=0)
    # 0:投票用户
    # 1:新建投票用户

    def __str__(self):
        return self.user_name