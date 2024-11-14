from django.db import models


class Category(models.Model):
    """Item category model"""
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name

class Warranty(models.Model):
    """Item warranty model"""
    name = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Гарантія"
        verbose_name_plural = "Гарантії"
    def __str__(self):
        return self.name


class Status(models.Model):
    """Item status model"""
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статуси"
    def __str__(self):
        return self.name


class Item(models.Model):
    """Item model"""
    title = models.CharField(max_length=200, blank=False)
    article = models.CharField(max_length=40, unique=True, blank=False)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='startup_logos/',
        #validators=[ImageValidator(max_size=5242880, max_width=1200, max_height=800)],
        blank=True,
        null=True)
    partner_price = models.DecimalField(max_digits=10, decimal_places=2)
    rrp_price = models.DecimalField(max_digits=10, decimal_places=2)
    warranty = models.ForeignKey(Warranty, on_delete=models.CASCADE)
    ean = models.CharField(max_length=50, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"
    def __str__(self):
        return self.article