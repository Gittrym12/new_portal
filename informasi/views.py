from django.shortcuts import render, redirect, get_object_or_404
from .models import Kegiatan
from .forms import KegiatanForm  # Fixed capitalization

def kegiatanList(request):
    # Retrieve all 'Kegiatan' objects from the database
    kegiatans = Kegiatan.objects.all()
    context = {'kegiatans': kegiatans}
    # Render 'list.html' template with the context containing 'kegiatans'
    return render(request, 'list.html', context=context)

def kegiatanCreate(request):
    if request.method == 'POST':
        form = KegiatanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to the 'kegiatan' list view after successfully saving the form
            return redirect('kegiatan')
    else:
        form = KegiatanForm()

    context = {'form': form}
    # Render 'create.html' template with the context containing the form
    return render(request, 'create.html', context=context)

def kegiatanEdit(request, id):
    # Retrieve the specific 'Kegiatan' object by ID or return a 404 error if not found
    kegiatan_instance = get_object_or_404(Kegiatan, id=id)
    if request.method == 'POST':
        form = KegiatanForm(request.POST, request.FILES, instance=kegiatan_instance)
        if form.is_valid():
            form.save()
            # Redirect to the 'kegiatan' list view after successfully updating the form
            return redirect('kegiatan')
    else:
        form = KegiatanForm(instance=kegiatan_instance)

    context = {'form': form}
    # Render 'edit.html' template with the context containing the form
    return render(request, 'edit.html', context=context)

def kegiatanDelete(request, id):
    # Retrieve the specific 'Kegiatan' object by ID or return a 404 error if not found
    kegiatan_instance = get_object_or_404(Kegiatan, id=id)
    if request.method == 'POST':
        kegiatan_instance.delete()
        # Redirect to the 'kegiatan' list view after successfully deleting the record
        return redirect('kegiatan')
    # Render 'delete.html' template (typically contains a confirmation prompt)
    return render(request, 'delete.html', {'object': kegiatan_instance})
