from django.db import models


# Create your models here.
class Links(models.Model):
    name = models.CharField(max_length=250)
    link = models.CharField(max_length=250)
    status = models.CharField(max_length=10, default='New')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'


class Articles(models.Model):
    name = models.CharField(max_length=250)
    url = models.CharField(max_length=250)
    photo = models.CharField(max_length=150, blank=True, null=True)
    published = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'



