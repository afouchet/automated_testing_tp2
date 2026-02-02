from django.contrib.auth.models import User
from django.db import models


class BookUser(models.Model):
    # For authentification
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_company = models.BooleanField(default=False)

    @property
    def name(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email
