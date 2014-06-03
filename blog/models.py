from datetime import datetime, timezone, timedelta

from django.db import models
from django.contrib.auth.models import User
import re

class Post(models.Model):
    author = models.ForeignKey(User)

    title = models.CharField(max_length=512)
    content = models.TextField()
    link = models.CharField(max_length=512)

    submission_date = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateTimeField(null=True,blank=True)
    modification_date = models.DateTimeField(auto_now=True)

    tags = models.CharField(blank=True,max_length=512)
    category = models.CharField(blank=True,max_length=512)

def title_to_link(title):
    #to lowercase
    title = title.lower()
    # strip quotes
    title = re.sub(r"['\"]+","",title)
    # convert all characters except aplhanum to dashes
    title = re.sub(r"[^a-z0-9]+","-",title)
    # remove dashes at beginning and end
    title = re.sub(r"^-+|-+$","",title)
    # remove double dashes
    title = re.sub(r"--+","-",title)
    # continuous whitespace to dash
    title = re.sub(r"\s+","-",title)
    return title

