from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.timezone import now
from django.db.models.signals import pre_save


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


class PartnerItem(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name="partner_items")
    article = models.CharField(max_length=50, blank=False, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, db_index=True)
    status = models.CharField(max_length=50, blank=True)
    availability = models.CharField(max_length=50)
    last_updated = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        verbose_name = "Товар партнера"
        verbose_name_plural = "Товары партнеров"

    def __str__(self):
        return f"{self.partner.name} - {self.article}"


class PriceHistory(models.Model):
    partner_item = models.ForeignKey(
        PartnerItem,
        on_delete=models.CASCADE,
        related_name="price_history"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "История цен"
        verbose_name_plural = "Истории цен"
