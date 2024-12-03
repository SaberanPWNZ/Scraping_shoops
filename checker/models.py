from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now


class Partner(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)
    web_site = models.URLField(max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to='partner_logos/', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнери"

    def __str__(self):
        return self.name


class ScrapedItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    article = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Товар партнера"
        verbose_name_plural = "Товари партнера"

    def __str__(self):
        return self.name


class ScrapedData(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name="scraped_data", default=None)
    items = models.ManyToManyField(ScrapedItem, related_name="scraped_data")
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(default=now)

    class Meta:
        verbose_name = "Інформація"
        verbose_name_plural = "Інформація"

    def __str__(self):
        return f"Data for {self.partner.name} - {self.created_at}"

