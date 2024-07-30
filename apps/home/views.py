import os
import glob
from django import forms
from django.conf import settings


from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, Http404
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
import pandas as pd
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse



from .models import (
    Formmodel,
    ProsedurM,
    Visitor,
    JadwalBusM,
    MenuKantinM,
    Pengumuman,
    Aturan,
    ActiveUser,
    trainingSchedule,
    Kegiatan
    
    
)

from .forms import (
    FormmodelForm,
    FormProsedur,
    JadwalBusF,
    MenuKantinF,
    PengumumanForm,
    AturanForm,
    SearchForm,
    ProsedurMSearchForm,
    TrainingScheduleForm,
    KegiatanForm
    
)



################################################################ TRAINING SCHEDULE #################################################################

from datetime import datetime

def get_month_name_in_bahasa(month):
    # Dictionary untuk mengonversi nama bulan dalam bahasa Indonesia
    month_names = {
        1: "Januari",
        2: "Februari",
        3: "Maret",
        4: "April",
        5: "Mei",
        6: "Juni",
        7: "Juli",
        8: "Agustus",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "Desember"
    }
    return month_names.get(month, "Bulan tidak valid")

def training_schedule_list(request):
    # Get all training schedules
    schedules = trainingSchedule.objects.all()

    # Calculate the sum of planPeserta1 to planPeserta4 values for each schedule
    for schedule in schedules:
        # Handle None values by providing a default value of 0
        planPeserta1 = schedule.planPeserta1 or 0
        planPeserta2 = schedule.planPeserta2 or 0
        planPeserta3 = schedule.planPeserta3 or 0
        planPeserta4 = schedule.planPeserta4 or 0

        schedule.total_plan_peserta = planPeserta1 + planPeserta2 + planPeserta3 + planPeserta4

    for schedule in schedules:
        # Handle None values by providing a default value of 0
        actPeserta1 = schedule.actPeserta1 or 0
        actPeserta2 = schedule.actPeserta2 or 0
        actPeserta3 = schedule.actPeserta3 or 0
        actPeserta4 = schedule.actPeserta4 or 0

        schedule.total_act_peserta = actPeserta1 + actPeserta2 + actPeserta3 + actPeserta4

    # Dapatkan objek datetime yang mewakili tanggal hari ini
    current_date = datetime.now()
    # Dapatkan nama bulan dalam bahasa Indonesia
    current_month_name = get_month_name_in_bahasa(current_date.month)

    # Pass schedules, current month name, and current date to the template
    return render(request, 'home/informasi/schedule_list.html', {'schedules': schedules, 'current_month_name': current_month_name, 'current_date': current_date})


@login_required(login_url="/login/")
def training_schedule_create(request):
    if request.method == 'POST':
        form = TrainingScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('schedule-list')
        else:
            # Print form errors for debugging
            print(form.errors)
    else:
        form = TrainingScheduleForm()
    return render(request, 'home/admin/schedule_form.html', {'form': form})

@login_required(login_url="/login/")
def training_schedule_update(request, pk):
    schedule = get_object_or_404(trainingSchedule, pk=pk)
    if request.method == 'POST':
        form = TrainingScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('schedule-list')
    else:
        form = TrainingScheduleForm(instance=schedule)
    return render(request, 'home/admin/schedule_edit.html', {'form': form, 'pk': pk, 'schedule': schedule})


@login_required(login_url="/login/")
def training_schedule_delete(request, pk):
    schedule = get_object_or_404(trainingSchedule, pk=pk)
    if request.method == 'POST':
        schedule.delete()
        return redirect('schedule-list')
    return render(request, 'home/admin/schedule_confirm_delete.html', {'schedule': schedule})


################################################################ TRAINING SCHEDULE #################################################################

def get_date_range():
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    this_month_start = datetime(today.year, today.month, 1).date()
    this_year_start = datetime(today.year, 1, 1).date()
    return today, yesterday, this_month_start, this_year_start


def index(request):
    today, yesterday, this_month_start, this_year_start = get_date_range()

    today_count = Visitor.objects.filter(timestamp__date=today).count()
    yesterday_count = Visitor.objects.filter(timestamp__date=yesterday).count()
    this_month_count = Visitor.objects.filter(
        timestamp__date__gte=this_month_start
    ).count()
    this_year_count = Visitor.objects.filter(
        timestamp__date__gte=this_year_start
    ).count()
    total_hits_count = Visitor.objects.all().count()

    online_users = Session.objects.filter(expire_date__gte=timezone.now()).count()

    # Record the current visitor
    current_visitor_ip = get_client_ip(request)
    Visitor.objects.create(ip_address=current_visitor_ip)

    context = {
        "segment": "index",
        "today_count": today_count,
        "yesterday_count": yesterday_count,
        "this_month_count": this_month_count,
        "this_year_count": this_year_count,
        "total_hits_count": total_hits_count,
        "online_users": online_users,
    }

    return render(request, "home/index.html", context)


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def formmodel_detail(request, pk, model_type):
    model_mapping = {
        'formmodel': Formmodel,
        'prosedur': ProsedurM,
        'pengumuman': Pengumuman,
        'aturan': Aturan,
    }

    model = model_mapping.get(model_type)
    if model:
        instance = get_object_or_404(model, pk=pk)
        return render(request, 'home/formmodel_detail.html', {'instance': instance, 'model_type': model_type})
    else:
        # Handle unknown model type gracefully, e.g., redirect to home or display a message
        return render(request, 'home/unknown_model.html')

def search(request):
    form = SearchForm(request.GET)
    results = []

    if form.is_valid():
        query = form.cleaned_data['q']

        if query:
            # Search across all models
            results += list(Formmodel.objects.filter(nama_form__icontains=query))
            results += list(ProsedurM.objects.filter(nama_prosedur__icontains=query))
            results += list(Pengumuman.objects.filter(nama_pengumuman__icontains=query))
            results += list(Aturan.objects.filter(title__icontains=query))

    context = {'form': form, 'results': results}

    # Check if the query is empty
    if not query:
        context['empty_query'] = True

    return render(request, 'home/search_result.html', context)



def pages(request):
    context = {}  # Membuat kamus kosong untuk menyimpan data konteks.

    try:
        load_template = request.path.split("/")[
            -1
        ]  # Mendapatkan bagian terakhir dari URL yang diminta.

        if load_template == "admin":
            # Jika bagian terakhir dari URL adalah "admin", alihkan pengguna ke halaman admin.
            return HttpResponseRedirect(reverse("admin:index"))

        context[
            "segment"
        ] = load_template  # Simpan bagian terakhir dari URL dalam konteks dengan kunci "segment".

        # Muat template yang sesuai berdasarkan bagian terakhir dari URL.
        html_template = loader.get_template("home/" + load_template)

        # Kembalikan hasil rendering template dengan menggunakan konteks yang telah disiapkan.
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        # Tangani jika template yang diminta tidak ditemukan. Kembalikan halaman 404.
        html_template = loader.get_template("home/page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:
        # Tangani kesalahan lain yang tidak terduga. Kembalikan halaman 500.
        html_template = loader.get_template("home/page-500.html")
        return HttpResponse(html_template.render(context, request))


##################################################### FORM METHODS #####################################################
# Fungsi untuk menampilkan daftar formulir
# views.py


def form_list(request):
    forms = Formmodel.objects.all()

    # Handle search query
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get("search_query")
        if search_query:
            forms = forms.filter(nama_form__icontains=search_query)

    return render(
        request, "home/form_list.html", {"forms": forms, "search_form": search_form}
    )


@login_required(login_url="/login/")
def form_create(request):
    if request.method == "POST":
        form = FormmodelForm(request.POST, request.FILES)
        if form.is_valid():
            instance = (
                form.save()
            )  # Menyimpan formulir untuk mendapatkan instance dengan file yang diunggah
            # Lakukan operasi tambahan jika diperlukan
            return redirect(
                "form_list"
            )  # Redirect ke URL 'form_list' menggunakan pola URL yang dinamai
    else:
        form = FormmodelForm()
    return render(request, "home/admin/form_create.html", {"form": form})


# Fungsi untuk mengunduh file yang terkait dengan formulir
def download_file(request, form_id):
    form_instance = Formmodel.objects.get(id=form_id)
    file_path = form_instance.file_upload.path
    with open(file_path, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/octet-stream")
        response["Content-Disposition"] = (
            "attachment; filename=" + form_instance.file_upload.name
        )
        return response


@login_required(login_url="/login/")
def form_update(request, pk):
    form = Formmodel.objects.get(pk=pk)
    if request.method == "POST":
        form = FormmodelForm(request.POST, request.FILES, instance=form)
        if form.is_valid():
            form.save()
            return redirect("form_list")
    else:
        form = FormmodelForm(instance=form)
    return render(request, "home/admin/form_update.html", {"form": form})


@login_required(login_url="/login/")
def form_delete(request, pk):
    form = Formmodel.objects.get(pk=pk)
    if request.method == "POST":
        form.delete()
        return redirect("form_list")
    return render(request, "home/admin/form_delete.html", {"form": form})


##################################################### END FORM METHODS #####################################################


##################################################### PROSEDUR METHODS #####################################################


def form_prosedur(request):
    forms = ProsedurM.objects.all()

    # Handle search query
    search_form = ProsedurMSearchForm(request.GET)
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get("search_query")
        if search_query:
            forms = forms.filter(nama_prosedur__icontains=search_query)

    return render(
        request,
        "home/form_list_prosedur.html",
        {"forms": forms, "search_form": search_form},
    )


def download_file_prosedur(request, form_id):
    form_instance = get_object_or_404(ProsedurM, id=form_id)
    file_path = form_instance.file_upload.path

    with open(file_path, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/octet-stream")
        response["Content-Disposition"] = (
            "attachment; filename=" + form_instance.file_upload.name
        )
        return response


@login_required(login_url="/login/")
def form_create_prosedur(request):
    if request.method == "POST":
        form = FormProsedur(request.POST, request.FILES)
        if form.is_valid():
            instance = (
                form.save()
            )  # Menyimpan formulir untuk mendapatkan instance dengan file yang diunggah
            # Lakukan operasi tambahan jika diperlukan
            return redirect(
                "form_list_prosedur"
            )  # Redirect ke URL 'form_list_prosedur' menggunakan pola URL yang dinamai
    else:
        form = FormProsedur()
    return render(request, "home/admin/form_create_prosedur.html", {"form": form})


@login_required(login_url="/login/")
def form_update_prosedur(request, pk):
    form = ProsedurM.objects.get(pk=pk)
    if request.method == "POST":
        form = FormProsedur(request.POST, request.FILES, instance=form)
        if form.is_valid():
            form.save()
            return redirect("form_list_prosedur")
    else:
        form = FormProsedur(instance=form)
    return render(request, "home/admin/form_update_prosedur.html", {"form": form})


@login_required(login_url="/login/")
def form_delete_prosedur(request, pk):
    form = ProsedurM.objects.get(pk=pk)
    if request.method == "POST":
        form.delete()
        return redirect("form_list_prosedur")
    return render(request, "home/admin/form_delete_prosedur.html", {"form": form})


##################################################### END PROSEDUR METHODS #####################################################


##################################################### DATA ULANG TAHUN #####################################################
def dataUlangTahun(request):
    # Path ke file CSV yang berisi data ulang tahun karyawan
    csv_file_path = "core/media/YPMIEmployee0124.csv"

    # Membaca data dari file CSV menggunakan pandas
    df = pd.read_csv(csv_file_path, delimiter=";")

    # Mendapatkan tanggal hari ini dalam format 'mm/dd'
    today_date = datetime.now().strftime("%m/%d")

    # Mengambil data yang cocok dengan tanggal ulang tahun hari ini
    filtered_data = df[df["Date"] == today_date]

    # Mengonversi data yang sesuai menjadi bentuk yang lebih mudah digunakan dalam template
    data = [
        {
            "NIK": row["NIK"],
            "Name": row["NAME"],
            "Section": row["SECTION"],
            "Occupation": row["OCCUPATION"],
        }
        for _, row in filtered_data.iterrows()
    ]

    # Merender template 'dataUlangTahun.html' dengan data yang telah disiapkan
    return render(request, "home/informasi/dataUlangTahunstyle4.html", {"data": data})


##################################################### END DATA UALNG TAHUN #####################################################


##################################################### MENU KANTIN #####################################################
@login_required(login_url="/login/")
def upload_csv(request):
    if request.method == "POST":
        form = MenuKantinF(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file
            instance = form.save()
            return redirect(
                "menuKantin"
            )  # Assuming 'menuKantin' is the URL pattern name for menuKantin view
    else:
        form = MenuKantinF()
    return render(request, "home/admin/create_menukantin.html", {"form": form})


def delete_csv(request, file_id):
    # Retrieve the MenuKantinM instance
    file_instance = MenuKantinM.objects.get(pk=file_id)

    # Get the file path
    file_path = file_instance.file.path

    # Delete the file from the storage
    if os.path.exists(file_path):
        os.remove(file_path)

    # Delete the MenuKantinM instance
    file_instance.delete()

    return redirect("menuKantin")


def menuKantin(request):
    csv_file_path = get_most_recent_csv_file()
    menus = MenuKantinM.objects.all()

    if csv_file_path:
        df = pd.read_csv(csv_file_path, delimiter=";")
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce", format="%d/%m/%Y")
        df["Date"].fillna(
            df["Date"].apply(
                lambda x: pd.to_datetime(x, errors="coerce", format="%d/%m")
            ),
            inplace=True,
        )

        today_date = datetime.now().strftime("%d/%m/%y")
        tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%y")

        today_data = df[df["Date"].dt.strftime("%d/%m/%y") == today_date]
        tomorrow_data = df[df["Date"].dt.strftime("%d/%m/%y") == tomorrow_date]

        today_data_list = []
        for _, row in today_data.iterrows():
            today_data_list.append(
                {
                    "Date": row["Date"].strftime("%d/%m/%Y"),
                    "Pilihan": row["PILIHAN"].replace(",", "<br>"),
                    "Breakfast": row["BREAKFAST"].replace(",", "<br>"),
                    "Shift3": row["SHIFT 3"].replace(",", "<br>"),
                    "Shift1": row["SHIFT 1"].replace(",", "<br>"),
                    "Shift2": row["SHIFT 2"].replace(",", "<br>"),
                }
            )

        tomorrow_data_list = []
        for _, row in tomorrow_data.iterrows():
            tomorrow_data_list.append(
                {
                    "Date": row["Date"].strftime("%d/%m/%Y"),
                    "Pilihan": row["PILIHAN"].replace(",", "<br>"),
                    "Breakfast": row["BREAKFAST"].replace(",", "<br>"),
                    "Shift3": row["SHIFT 3"].replace(",", "<br>"),
                    "Shift1": row["SHIFT 1"].replace(",", "<br>"),
                    "Shift2": row["SHIFT 2"].replace(",", "<br>"),
                }
            )

        return render(
            request,
            "home/informasi/menuKantin.html",
            {
                "today_data": today_data_list,
                "tomorrow_data": tomorrow_data_list,
                "menus": menus,
            },
        )
    else:
        return render(request, "home/admin/menu_nodata.html")


def get_most_recent_csv_file():
    # Get a list of CSV files in the 'media/uploads/menuKantin' directory and subdirectories
    csv_files = glob.glob(
        os.path.join(settings.MEDIA_ROOT, "uploads/menuKantin/**/*.csv"), recursive=True
    )

    # Sort the list of files by modification time (most recent first)
    csv_files.sort(key=os.path.getmtime, reverse=True)

    # Check if any CSV files were found
    if csv_files:
        # Return the path to the most recently modified CSV file
        return csv_files[0]
    else:
        return None


##################################################### END MENU KANTIN #####################################################


##################################################### CHART METHODS #####################################################


##################################################### END CHART METHHODS #####################################################


##################################################### JADWAL BUS   #####################################################
def jadwal_bus(request):
    forms = JadwalBusM.objects.all()
    return render(request, "home/informasi/jadwalBusJemputan.html", {"forms": forms})


@login_required(login_url="/login/")
def jadwal_bus_create(request):
    if request.method == "POST":
        form = JadwalBusF(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            # Perform any additional operations if needed
            return redirect("jadwal_bus_list")  # Use the correct URL name
    else:
        form = JadwalBusF()
    return render(request, "home/admin/jadwalBus_create.html", {"form": form})


@login_required(login_url="/login/")
def jadwal_bus_update(request, pk):
    instance = get_object_or_404(JadwalBusM, pk=pk)

    if request.method == "POST":
        form = JadwalBusF(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("jadwal_bus_list")  # Use the correct URL name
    else:
        form = JadwalBusF(instance=instance)

    return render(request, "home/admin/jadwalBus_update.html", {"form": form})


@login_required(login_url="/login/")
def jadwal_bus_delete(request, pk):
    form = get_object_or_404(JadwalBusM, pk=pk)
    if request.method == "POST":
        form.delete()
        return redirect("jadwal_bus_list")  # Use the correct URL name
    return render(request, "home/admin/jadwalBus_delete.html", {"form": form})


##################################################### END JADWAL BUS #####################################################


##################################################### PENGUMUMAN METHODS #####################################################



def pengumuman_list(request):
    pengumumans = Pengumuman.objects.all()

    # Handle search query
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get("search_query")
        if search_query:
            pengumumans = pengumumans.filter(nama_pengumuman__icontains=search_query)

    return render(
        request, "home/informasi/pengumumanList.html", {"pengumumans": pengumumans, "search_form": search_form}
    )

@login_required(login_url="/login/")
def pengumuman_create(request):
    if request.method == "POST":
        form = PengumumanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("pengumuman_list")
    else:
        form = PengumumanForm()
    return render(request, "home/admin/pengumuman_create.html", {"form": form})

@login_required(login_url="/login/")
def pengumuman_update(request, pk):
    pengumuman = get_object_or_404(Pengumuman, pk=pk)
    if request.method == "POST":
        form = PengumumanForm(request.POST, request.FILES, instance=pengumuman)
        if form.is_valid():
            form.save()
            return redirect("pengumuman_list")
    else:
        form = PengumumanForm(instance=pengumuman)
    return render(request, "home/admin/pengumuman_update.html", {"form": form})

@login_required(login_url="/login/")
def pengumuman_delete(request, pk):
    pengumuman = get_object_or_404(Pengumuman, pk=pk)
    if request.method == "POST":
        pengumuman.delete()
        return redirect("pengumuman_list")
    return render(request, "home/admin/pengumuman_delete.html", {"pengumuman": pengumuman})

def download_file_pengumuman(request, pengumuman_id):
    pengumuman_instance = get_object_or_404(Pengumuman, id=pengumuman_id)
    file_path = pengumuman_instance.file_pengumuman.path
    with open(file_path, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/octet-stream")
        response["Content-Disposition"] = (
            "attachment; filename=" + pengumuman_instance.file_pengumuman.name
        )
    return response


##################################################### CHART METHODS #####################################################







def logged_in_users(request):
    # Get a list of all active users
    active_users = ActiveUser.objects.all()

    return render(request, 'home/admin/logged_in_users.html', {'active_users': active_users})



def aturan_list_view(request):
    aturans = Aturan.objects.all()
    return render(request, "home/aturan_list.html", {"aturans": aturans})


def aturan_download_view(request, pk):
    aturan = get_object_or_404(Aturan, pk=pk)
    response = FileResponse(aturan.pdf_file, as_attachment=True)
    return response


@login_required(login_url="/login/")
def aturan_create_view(request):
    if request.method == "POST":
        form = AturanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("aturan_list")
    else:
        form = AturanForm()

    return render(request, "home/admin/aturan_create.html", {"form": form})


@login_required(login_url="/login/")
def aturan_update_view(request, pk):
    aturan = get_object_or_404(Aturan, pk=pk)

    if request.method == "POST":
        form = AturanForm(request.POST, request.FILES, instance=aturan)
        if form.is_valid():
            form.save()
            return redirect("aturan_list")
    else:
        form = AturanForm(instance=aturan)

    return render(request, "home/admin/aturan_update.html", {"form": form})


@login_required(login_url="/login/")
def aturan_delete_view(request, pk):
    aturan = get_object_or_404(Aturan, pk=pk)
    if request.method == "POST":
        aturan.delete()
        return redirect("aturan_list")

    return render(request, "home/admin/aturan_delete.html", {"aturan": aturan})


##################################################### END CHART METHHODS #####################################################



#####################################################  KEGIATAN METHODS #####################################################



def kegiatanList(request):
    # Retrieve all 'Kegiatan' objects from the database
    kegiatans = Kegiatan.objects.all().order_by('-created_at')
    latest_kegiatan = kegiatans.first() if kegiatans.exists() else None
    other_kegiatans = kegiatans[1:] if kegiatans.count() > 1 else []

    context = {
        'latest_kegiatan': latest_kegiatan,
        'other_kegiatans': other_kegiatans
    }
    # Render 'kegiatan-list.html' template with the context containing 'kegiatans'
    return render(request, 'home/admin/kegiatan-list.html', context=context)

def kegiatanCreate(request):
    if request.method == 'POST':
        form = KegiatanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to the 'kegiatan' list view after successfully saving the form
            return redirect('kegiatan-list')
    else:
        form = KegiatanForm()

    context = {'form': form}
    # Render 'kegiatan-create.html' template with the context containing the form
    return render(request, 'home/admin/kegiatan-create.html', context=context)

def kegiatanEdit(request, id):
    # Retrieve the specific 'Kegiatan' object by ID or return a 404 error if not found
    kegiatan_instance = get_object_or_404(Kegiatan, id=id)
    if request.method == 'POST':
        form = KegiatanForm(request.POST, request.FILES, instance=kegiatan_instance)
        if form.is_valid():
            form.save()
            # Redirect to the 'kegiatan' list view after successfully updating the form
            return redirect('kegiatan-list')
    else:
        form = KegiatanForm(instance=kegiatan_instance)

    context = {'form': form}
    # Render 'kegiatan-update.html' template with the context containing the form
    return render(request, 'home/admin/kegiatan-update.html', context=context)

def kegiatanDelete(request, id):
    # Retrieve the specific 'Kegiatan' object by ID or return a 404 error if not found
    kegiatan_instance = get_object_or_404(Kegiatan, id=id)
    if request.method == 'POST':
        kegiatan_instance.delete()
        # Redirect to the 'kegiatan' list view after successfully deleting the record
        return redirect('kegiatan-list')
    # Render 'kegiatan-delete.html' template (typically contains a confirmation prompt)
    return render(request, 'home/admin/kegiatan-delete.html', {'object': kegiatan_instance})



##################################################### END KEGIATAN METHODS #####################################################


def aturanViews(request):
    return render(request, "home/aturan.html")  

def sachooCup(request):
    return render(request, "home/informasi/sachoocup.html")


def data_tables(request):
    return render(request, "home/tables.html")


def icon_tables(request):
    return render(request, "home/icon.html")


def timKami(request):
    return render(request, "home/timKami.html")


def kontak(request):
    return render(request, "home/kontakv.html")


def visiYpmi(request):
    return render(request, "home/visiypmi.html")


def pengumumanHRD(request):
    return render(request, "home/informasi/pengumumanHRD.html")


def jadwalTraining(request):
    return render(request, "home/informasi/jadwalTraining.html")


def jadwalBusJemputan(request):
    return render(request, "home/informasi/jadwalBusJemputan.html")


def satgasPPKS(request):
    return render(request, "home/informasi/satgasPPKS.html")


def pkb(request):
    return render(request, "home/informasi/pkb.html")


def dataKehadiranTerbaik(request):
    return render(request, "home/informasi/dataKehadiranTerbaik.html")


def strukturOrganisasi(request):
    return render(request, "home/informasi/struktur-organisasi.html")


def indexskehadiran4(request):
    return render(request, "home/informasi/indexsKehadiran2.html")


def kegiatanfix(request):
    return render(request, "home/informasi/kegiatanfixs.html")