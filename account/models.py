from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class RegKey(models.Model):
	user = models.OneToOneField(User)
	activation_key = models.CharField(max_length=40)
	
	def __str__(self):
		return self.user.email+" = "+self.activation_key
	
class ResetKey(models.Model):
	user = models.OneToOneField(User)
	activation_key = models.CharField(max_length=40)

	def __str__(self):
		return self.user.email+" = "+self.activation_key
