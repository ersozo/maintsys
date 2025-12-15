from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Plant


@login_required
def plant_list(request):
    plants = Plant.objects.filter(is_active=True)
    
    if request.htmx:
        return render(request, "plants/partials/plant_table.html", {"plants": plants})
    
    return render(request, "plants/plant_list.html", {"plants": plants})


@login_required
def plant_create(request):
    if request.method == "POST":
        plant = Plant.objects.create(
            name=request.POST.get("name"),
            code=request.POST.get("code"),
            address=request.POST.get("address", ""),
            city=request.POST.get("city", ""),
            phone=request.POST.get("phone", ""),
            email=request.POST.get("email", ""),
        )
        
        if request.htmx:
            plants = Plant.objects.filter(is_active=True)
            response = render(request, "plants/partials/plant_table.html", {"plants": plants})
            response['HX-Trigger'] = 'closeModal'
            return response
        
        return redirect('plants:plant_list')
    
    if request.htmx:
        return render(request, "plants/partials/plant_form.html")
    
    return render(request, "plants/plant_form.html")


@login_required
def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    assets = plant.assets.filter(is_active=True)
    return render(request, "plants/plant_detail.html", {
        "plant": plant,
        "assets": assets
    })


@login_required
def plant_edit(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    
    if request.method == "POST":
        plant.name = request.POST.get("name")
        plant.code = request.POST.get("code")
        plant.address = request.POST.get("address", "")
        plant.city = request.POST.get("city", "")
        plant.phone = request.POST.get("phone", "")
        plant.email = request.POST.get("email", "")
        plant.save()
        
        if request.htmx:
            plants = Plant.objects.filter(is_active=True)
            response = render(request, "plants/partials/plant_table.html", {"plants": plants})
            response['HX-Trigger'] = 'closeModal'
            return response
        
        return redirect('plants:plant_list')
    
    if request.htmx:
        return render(request, "plants/partials/plant_form.html", {"plant": plant})
    
    return render(request, "plants/plant_form.html", {"plant": plant})


@login_required
def plant_delete(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    
    if request.method == "POST":
        plant.is_active = False
        plant.save()
        
        if request.htmx:
            plants = Plant.objects.filter(is_active=True)
            response = render(request, "plants/partials/plant_table.html", {"plants": plants})
            response['HX-Trigger'] = 'closeModal'
            return response
        
        return redirect('plants:plant_list')
    
    if request.htmx:
        return render(request, "plants/partials/plant_delete_confirm.html", {"plant": plant})
    
    return render(request, "plants/plant_delete_confirm.html", {"plant": plant})


@login_required
def plant_archive(request):
    """Show archived (soft-deleted) plants"""
    plants = Plant.objects.filter(is_active=False)
    
    if request.htmx:
        return render(request, "plants/partials/plant_archive_table.html", {"plants": plants})
    
    return render(request, "plants/plant_archive.html", {"plants": plants})


@login_required
def plant_restore(request, pk):
    """Restore a soft-deleted plant"""
    plant = get_object_or_404(Plant, pk=pk, is_active=False)
    
    if request.method == "POST":
        plant.is_active = True
        plant.save()
        
        if request.htmx:
            plants = Plant.objects.filter(is_active=False)
            response = render(request, "plants/partials/plant_archive_table.html", {"plants": plants})
            response['HX-Trigger'] = 'closeModal'
            return response
        
        return redirect('plants:plant_archive')
    
    if request.htmx:
        return render(request, "plants/partials/plant_restore_confirm.html", {"plant": plant})
    
    return render(request, "plants/plant_restore_confirm.html", {"plant": plant})
