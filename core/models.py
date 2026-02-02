from django.contrib.auth.models import User
from django.db import models


class BookUser(models.Model):
    # For authentification
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_user')
    name = models.CharField(max_length=100)
    email = models.EmailField()

    is_company = models.BooleanField(default=False)
