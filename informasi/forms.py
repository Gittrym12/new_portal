from django import forms
from .models import Kegiatan

class KegiatanForm(forms.ModelForm):  # Fixed capitalization
    class Meta:
        model = Kegiatan
        fields = ['judul', 'tanggal', 'deskripsi', 'image_thumb']
    
    def __init__(self, *args, **kwargs):
        super(KegiatanForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
