from django.db import models


class Partner(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)
    web_site = models.URLField(max_length=100, null=True)
    logo = models.ImageField()

    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнери"

    def __str__(self):
        return self.name


class ScrapedData(models.Model):
    partner_name = models.ForeignKey(Partner, on_delete=models.CASCADE)
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_created=True, blank=True, null=True)

    class Meta:
        verbose_name = "Інформація"
        verbose_name_plural = "Інформація"

    def __str__(self):
        return self.partner_name
