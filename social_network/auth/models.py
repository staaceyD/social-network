from django.contrib.auth.models import User
from django.db import models

class UserLastRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_request_at = models.DateTimeField(auto_now=True)