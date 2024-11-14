from django.db import models


class ScrapedData(models.Model):
    partner_name = models.CharField(max_length=100)
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)