from django.conf import settings
from django.db import models


class SocialClient(models.Model):
    client_id = models.CharField(max_length=255, blank=True, null=True)
    client_secret = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    redirect_url = models.CharField(max_length=255, blank=True, null=True)
    client_type = models.CharField(max_length=255, blank=True, null=True, default='confidential')
    authorization_grant_type = models.CharField(max_length=255, blank=True, null=True, default='Resource owner password-based')
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"client id {self.client_id}"


