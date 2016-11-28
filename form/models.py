from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Form(models.Model):
	title = models.CharField(max_length = 70)
	author = models.CharField(max_length = 70)
	create_time = models.DateTimeField(auto_now_add = True)

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['-create_time']


class Key(models.Model):
	form = models.ForeignKey('Form',null = True,on_delete = models.CASCADE)
	keyLabel = models.CharField(max_length = 70)
	keyType = models.CharField(max_length = 10)

	create_time = models.DateTimeField(auto_now_add = True)

	def __unicode__(self):
		return self.keyLabel

	class Meta:
		ordering = ['-create_time']


class KeyContent(models.Model):
	key = models.ForeignKey('Key',null = True,on_delete = models.CASCADE)
	content = models.TextField()
	create_time = models.DateTimeField(auto_now_add = True)

	def __unicode__(self):
		return self.content

	class Meta:
		ordering = ['-create_time']



