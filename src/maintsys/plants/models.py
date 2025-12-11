from django.db import models


class Plant(models.Model):
    """Tesis/Fabrika modeli"""
    name = models.CharField("Tesis Adı", max_length=200)
    code = models.CharField("Tesis Kodu", max_length=50, unique=True)
    address = models.TextField("Adres", blank=True)
    city = models.CharField("Şehir", max_length=100, blank=True)
    phone = models.CharField("Telefon", max_length=20, blank=True)
    email = models.EmailField("E-posta", blank=True)
    is_active = models.BooleanField("Aktif", default=True)
    created_at = models.DateTimeField("Oluşturulma Tarihi", auto_now_add=True)
    updated_at = models.DateTimeField("Güncellenme Tarihi", auto_now=True)

    class Meta:
        verbose_name = "Tesis"
        verbose_name_plural = "Tesisler"
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"
    
    @property
    def asset_count(self):
        return self.assets.count()
