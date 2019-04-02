from django.db import models

class Question(models.Model):
	FFMC = models.FloatField(default=0)
	DMC = models.FloatField(default=0)
	DC =models.FloatField(default=0)
	ISI =models.FloatField(default=0)
	RH =  models.FloatField(default=0)
	temp = models.FloatField(default=0)
	wind =  models.FloatField(default=0)
	fwi = models.FloatField(default=0)
	area =  models.FloatField(default=0)
