from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    departement = models.CharField(max_length=50)
    occupation = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username



class Formmodel(models.Model):
    # Model for handling form data
    id = models.AutoField(primary_key=True)
    nama_form = models.CharField(max_length=100)
    no_form = models.CharField(max_length=51)
    category_form = models.CharField(max_length=100)
    file_upload = models.FileField(upload_to="uploads/")

    def model_name(self):
        return 'Formmodel'

    def __str__(self):
        return str(self.nama_form)

class ProsedurM(models.Model):
    # Model for handling procedure data
    id = models.AutoField(primary_key=True)
    nama_prosedur = models.CharField(max_length=100)
    category_prosedur = models.CharField(max_length=100)
    file_upload = models.FileField(upload_to="uploads/prosedur")

    def model_name(self):
        return 'ProsedurM'

    def __str__(self):
        return str(self.nama_prosedur)

class Aturan(models.Model):
    # Model for handling rules data
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    div_cat = models.CharField(max_length=30)
    description = models.TextField()
    pdf_file = models.FileField(upload_to="uploads/aturan_pdfs/")

    def model_name(self):
        return 'Aturan'

    def __str__(self):
        return str(self.title)


from django.db import models

class Pengumuman(models.Model):
    # Model for handling pengumuman data
    id = models.AutoField(primary_key=True)
    nama_pengumuman = models.CharField(max_length=355)
    tahun = models.CharField(max_length=5)
    file_pengumuman = models.FileField(upload_to="uploads/pengumuman")
    tanggal_upload = models.DateField()

    def model_name(self):
        return 'Pengumuman'

    def __str__(self):
        return str(self.nama_pengumuman)



class Visitor(models.Model):
    # Model for handling visitor data
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.ip_address} - {self.timestamp}"

class JadwalBusM(models.Model):
    # Model for handling bus schedule data
    id = models.AutoField(primary_key=True)
    titikStart = models.CharField(max_length=30)
    plant = models.CharField(max_length=2)
    via = models.TextField(max_length=255)
    seat = models.IntegerField()
    shift1 = models.CharField(max_length=5, null=True)
    shift2 = models.CharField(max_length=5, null=True)
    shift3 = models.CharField(max_length=5, null=True)

    def __str__(self):
        return str(self.titikStart)

class MenuKantinM(models.Model):
    # Model for handling canteen menu data
    id = models.AutoField(primary_key=True)
    nama_file = models.CharField(max_length=35)
    file = models.FileField(upload_to="uploads/menuKantin")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.nama_file)



class ActiveUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_activity = models.DateTimeField()

    def __str__(self):
        return self.user.username
    



class trainingSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    judulTraining = models.CharField(max_length=55, blank=True)
    trainingCat = models.CharField(max_length=55, blank=True)
    planPeserta1 = models.IntegerField(null=True, blank=True)
    planPeserta2 = models.IntegerField(null=True, blank=True)
    planPeserta3 = models.IntegerField(null=True, blank=True)
    planPeserta4 = models.IntegerField(null=True, blank=True)
    actPeserta1 = models.IntegerField(null=True, blank=True)
    actPeserta2 = models.IntegerField(null=True, blank=True)
    actPeserta3 = models.IntegerField(null=True, blank=True)
    actPeserta4 = models.IntegerField(null=True, blank=True)
    durasiJam = models.CharField(max_length=4, blank=True)
    durasiHari = models.CharField(max_length=4, blank=True)
    pesertaOP = models.CharField(max_length=1, null=True, blank=True)
    pesertaLDR = models.CharField(max_length=1, null=True, blank=True)
    pesertaFR = models.CharField(max_length=1, null=True, blank=True)
    pesertaGF = models.CharField(max_length=1, null=True, blank=True)
    pesertaSPV = models.CharField(max_length=1, null=True, blank=True)
    pesertaSTAFF = models.CharField(max_length=1, null=True, blank=True)
    pesertaMNG = models.CharField(max_length=1, null=True, blank=True)

    def __str__(self):
        return str(self.judulTraining)





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
