from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
	class Types(models.TextChoices):
		SuperAdmin='SuperAdmin'
		Admin='Admin'
		Man='Man'

	type=models.CharField(max_length=50,default=Types.Man,choices=Types.choices)

	name=models.CharField(max_length=50)


class SuperAdminManager(models.Manager):
	def get_queryset(self,*args,**kwargs):
		return super().get_queryset(*args,**kwargs).filter(type=User.Types.SuperAdmin)

class AdminManager(models.Manager):
	def get_queryset(self,*args,**kwargs):
		return super().get_queryset(*args,**kwargs).filter(type=User.Types.Admin)

class ManManager(models.Manager):
	def get_queryset(self,*args,**kwargs):
		return super().get_queryset(*args,**kwargs).filter(type=User.Types.Man)



class SuperAdmin(User):
	objects=SuperAdminManager()
	class Meta:
		proxy=True


class Admin(User):
	objects=AdminManager()
	class Meta:
		proxy=True


class Man(User):
	objects=ManManager()
	class Meta:
		proxy=True