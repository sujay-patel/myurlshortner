from django.db import models

# Create your models here.
class Urls(models.Model):
    short_id = models.SlugField(max_length=8,primary_key=True)
    httpurl = models.URLField()
    pub_date = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)

def __str__(self):
    return self.httpurl
