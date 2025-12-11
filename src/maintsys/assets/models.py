from django.db import models
from plants.models import Plant


class Asset(models.Model):
    """Ekipman/Makine modeli"""
    STATUS_CHOICES = [
        ('active', 'Aktif'),
        ('inactive', 'Pasif'),
        ('maintenance', 'Bakımda'),
        ('broken', 'Arızalı'),
    ]
    
    plant = models.ForeignKey(
        Plant, 
        on_delete=models.CASCADE, 
        related_name='assets',
        verbose_name="Tesis"
    )
    name = models.CharField("Ekipman Adı", max_length=200)
    code = models.CharField("Ekipman Kodu", max_length=50)
    location = models.CharField("Lokasyon", max_length=200, blank=True)
    description = models.TextField("Açıklama", blank=True)
    manufacturer = models.CharField("Üretici", max_length=200, blank=True)
    model = models.CharField("Model", max_length=200, blank=True)
    serial_number = models.CharField("Seri No", max_length=100, blank=True)
    purchase_date = models.DateField("Satın Alma Tarihi", null=True, blank=True)
    warranty_expiry = models.DateField("Garanti Bitiş", null=True, blank=True)
    status = models.CharField(
        "Durum", 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='active'
    )
    is_active = models.BooleanField("Aktif", default=True)
    created_at = models.DateTimeField("Oluşturulma Tarihi", auto_now_add=True)
    updated_at = models.DateTimeField("Güncellenme Tarihi", auto_now=True)

    class Meta:
        verbose_name = "Ekipman"
        verbose_name_plural = "Ekipmanlar"
        ordering = ['plant', 'name']
        unique_together = ['plant', 'code']

    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def get_status_color(self):
        colors = {
            'active': 'emerald',
            'inactive': 'gray',
            'maintenance': 'amber',
            'broken': 'red',
        }
        return colors.get(self.status, 'gray')
