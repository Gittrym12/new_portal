from django.db import models
from django.utils import timezone



# Create your models here.
class Kegiatan(models.Model):
    judul = models.CharField(max_length=100)
    tanggal = models.CharField(max_length=100)
    deskripsi = models.CharField(max_length=355)
    image_thumb = models.ImageField(upload_to='images/thumb')
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.judul
