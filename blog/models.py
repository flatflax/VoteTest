from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Blog
class Blog(models.Model):
	blog_id = models.IntegerField(default=1,primary_key=True)
	blog_address = models.CharField(max_length=200)
	blog_name = models.CharField(max_length=200)
	username = models.CharField(max_length=200)
	time = models.DateTimeField('date published')
	tags = models.CharField(max_length=200)

	def __str__(self):
		return self.blog_id

class BlogId(models.Model):
	b_id = models.IntegerField(default=1)