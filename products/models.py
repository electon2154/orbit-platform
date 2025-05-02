from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="اسم الفئة")
    description = models.TextField(blank=True, null=True, verbose_name="وصف الفئة")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "فئة المنتجات"
        verbose_name_plural = "فئات المنتجات"
        ordering = ['name']

    def __str__(self):
        return self.name

# Create your models here.
