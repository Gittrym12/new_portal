import os
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, FileField
from django.contrib.auth.models import User

from .models import (
    Formmodel,
    ProsedurM,
    JadwalBusM,
    MenuKantinM,
    Pengumuman,
    Aturan,
    trainingSchedule,
    Kegiatan
    
)



class TrainingScheduleForm(forms.ModelForm):
    class Meta:
        model = trainingSchedule
        fields = '__all__'


class FormmodelForm(forms.ModelForm):
    """Form untuk model Formmodel."""

    class Meta:
        model = Formmodel
        fields = "__all__"


class FormProsedur(forms.ModelForm):
    """Form untuk model ProsedurM."""

    class Meta:
        model = ProsedurM
        fields = "__all__"


class JadwalBusF(forms.ModelForm):
    """Form untuk model JadwalBusM."""

    class Meta:
        model = JadwalBusM
        fields = "__all__"


def validate_file_extension(value):
    """Validasi ekstensi file untuk menuKantinF."""
    allowed_extensions = [".xlsx", ".csv"]
    file_extension = os.path.splitext(value.name)[1]

    if file_extension not in allowed_extensions:
        raise ValidationError("Only XLSX or CSV files are allowed.")


class MenuKantinF(ModelForm):
    """Form untuk model MenuKantinM."""

    file = FileField(validators=[validate_file_extension])

    class Meta:
        model = MenuKantinM
        fields = "__all__"


class PengumumanForm(forms.ModelForm):
    class Meta:
        model = Pengumuman
        fields = "__all__"
        widgets = {
            'tanggal_upload': forms.TextInput(attrs={'type': 'date'}),
        }





class AturanForm(forms.ModelForm):
    """Form untuk model Aturan."""

    class Meta:
        model = Aturan
        fields = ["title", "description", "pdf_file"]


class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False)


class ProsedurMSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False)


class SearchFormAll(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search..."}),
    )

class SearchForm(forms.Form):
    q = forms.CharField(label='Search', max_length=100, required=False)





class KegiatanForm(forms.ModelForm):  # Fixed capitalization
    class Meta:
        model = Kegiatan
        fields = ['judul', 'tanggal', 'deskripsi', 'image_thumb']
    
    def __init__(self, *args, **kwargs):
        super(KegiatanForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
