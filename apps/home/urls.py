from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from apps.home import views

# Define URL patterns for your Django application

urlpatterns = [
    # Home page
    path("", views.index, name="home"),

    # Form related views
    path("home/form_list/", views.form_list, name="form_list"),
    path("home/create/", views.form_create, name="form_create"),
    path("download/<int:form_id>/", views.download_file, name="download_file"),
    path("home/update/<int:pk>/", views.form_update, name="form_update"),
    path("home/delete/<int:pk>/", views.form_delete, name="form_delete"),

    # Prosedur related views
    path("home/list_prosedur/", views.form_prosedur, name="form_list_prosedur"),
    path("home/create_prosedur/", views.form_create_prosedur, name="form_create_prosedur"),
    path("download/prosedur<int:form_id>/", views.download_file_prosedur, name="download_file_prosedur"),
    path("home/update_prosedur/<int:pk>/", views.form_update_prosedur, name="form_update_prosedur"),
    path("home/delete_prosedur/<int:pk>/", views.form_delete_prosedur, name="form_delete_prosedur"),


    # Jadwal Bus views
    path("home/jadwal_bus/", views.jadwal_bus, name="jadwal_bus_list"),
    path("home/jadwal_bus/create/", views.jadwal_bus_create, name="jadwal_bus_create"),
    path("home/jadwal_bus/update/<int:pk>/", views.jadwal_bus_update, name="jadwal_bus_update"),
    path("home/jadwal_bus/delete/<int:pk>/", views.jadwal_bus_delete, name="jadwal_bus_delete"),

    # Menu Kantin views
    path("home/menuKantin/", views.menuKantin, name="menuKantin"),
    path("home/create_menuKantin/", views.upload_csv, name="create_menuKantin"),
    path("home/delete_menuKantin/<int:file_id>/", views.delete_csv, name="delete_menuKantin"),

    # Pengumuman views
    path('pengumuman/list/', views.pengumuman_list, name='pengumuman_list'),    
    path('pengumuman/create/', views.pengumuman_create, name='pengumuman_create'),
    path('pengumuman/update/<int:pk>/', views.pengumuman_update, name='pengumuman_update'),
    path('pengumuman/delete/<int:pk>/', views.pengumuman_delete, name='pengumuman_delete'),
    path('pengumuman/download/<int:pengumuman_id>/', views.download_file_pengumuman, name='download_file_pengumuman'),

    # Aturan views
    path("home/aturan/", views.aturan_list_view, name="aturan_list"),
    path("home/aturan/create/", views.aturan_create_view, name="aturan_create"),
    path("home/aturan/<int:pk>/edit/", views.aturan_update_view, name="aturan_edit"),
    path("home/aturan/<int:pk>/delete/", views.aturan_delete_view, name="aturan_delete"),
    path("aturan/<int:pk>/download/", views.aturan_download_view, name="aturan_download"),


    # TRAINING SCHEDULE
    path('home/jadwal_training', views.training_schedule_list, name='schedule-list'),
    path('home/jadwal_training/create/', views.training_schedule_create, name='schedule-create'),
    path('home/jadwal_training/<int:pk>/update/', views.training_schedule_update, name='schedule-update'),
    path('home/jadwal_training/<int:pk>/delete/', views.training_schedule_delete, name='schedule-delete'),

    path('kegiatan/', views.kegiatanList, name='kegiatan-list'),
    path('kegiatan/create/', views.kegiatanCreate, name='kegiatan-create'),
    path('kegiatan/edit/<int:id>/', views.kegiatanEdit, name='kegiatan-edit'),
    path('kegiatan/delete/<int:id>/', views.kegiatanDelete, name='kegiatan-delete'),


    # Other views
    path('search/', views.search, name='search_results'),
    path('<str:model_type>/<int:pk>/', views.formmodel_detail, name='formmodel_detail'),

    path("home/aturan/", views.aturanViews, name="aturan"),
    path("home/sachoocup/", views.sachooCup, name="sachoocup"),
    path("home/kontak/", views.kontak, name="kontak"),
    path("home/timKami/", views.timKami, name="timKami"),
    path("home/visiYpmi/", views.visiYpmi, name="visiYpmi"),
    path("home/pengumumanHRD/", views.pengumumanHRD, name="pengumumanHRD"),
    path("home/jadwalTraining/", views.jadwalTraining, name="jadwalTraining"),
    path("home/jadwalBusJemputan/", views.jadwalBusJemputan, name="jadwalBusJemputan"),
    path("home/satgasPPKS/", views.satgasPPKS, name="satgasPPKS"),
    path("home/pkb/", views.pkb, name="pkb"),
    path("home/dataUlangTahun/", views.dataUlangTahun, name="dataUlangTahun"),
    path("home/dataKehadiranTerbaik/", views.dataKehadiranTerbaik, name="dataKehadiranTerbaik"),
    path("home/struktur_organisasi/", views.strukturOrganisasi, name="struktur_organisasi"),
    path("home/indeks_kehadiran/", views.indexskehadiran4, name="indeks_kehadiran"),
    path("home/kegiatan/", views.kegiatanfix, name="kegiatan"),
    path('logged-in-users/', views.logged_in_users, name='logged_in_users'),

    # Matches any html file
    re_path(r"^.*\.*", views.pages, name="pages"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
