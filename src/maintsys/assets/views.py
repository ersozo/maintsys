from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Asset
from plants.models import Plant


@login_required
def asset_list(request):
    assets = Asset.objects.filter(is_active=True).select_related('plant')
    plants = Plant.objects.filter(is_active=True)
    
    # Filter by plant if provided
    plant_id = request.GET.get('plant')
    if plant_id:
        assets = assets.filter(plant_id=plant_id)
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        assets = assets.filter(status=status)
    
    context = {
        'assets': assets,
        'plants': plants,
        'selected_plant': plant_id,
        'selected_status': status,
    }
    
    if request.htmx:
        return render(request, "assets/partials/asset_table.html", context)
    
    return render(request, "assets/asset_list.html", context)


@login_required
def asset_create(request):
    plants = Plant.objects.filter(is_active=True)
    preselected_plant = request.GET.get('plant')
    
    if request.method == "POST":
        asset = Asset.objects.create(
            plant_id=request.POST.get("plant"),
            name=request.POST.get("name"),
            code=request.POST.get("code"),
            location=request.POST.get("location", ""),
            description=request.POST.get("description", ""),
            manufacturer=request.POST.get("manufacturer", ""),
            model=request.POST.get("model", ""),
            serial_number=request.POST.get("serial_number", ""),
            status=request.POST.get("status", "active"),
        )
        
        if request.htmx:
            assets = Asset.objects.filter(is_active=True).select_related('plant')
            response = render(request, "assets/partials/asset_table.html", {"assets": assets, "plants": plants})
            response['HX-Trigger'] = 'closeModal'
            return response
        
        return redirect('assets:asset_list')
    
    context = {
        'plants': plants,
        'preselected_plant': preselected_plant,
    }
    
    if request.htmx:
        return render(request, "assets/partials/asset_form.html", context)
    
    return render(request, "assets/asset_form.html", context)


@login_required
def asset_detail(request, pk):
    asset = get_object_or_404(Asset.objects.select_related('plant'), pk=pk)
    return render(request, "assets/asset_detail.html", {"asset": asset})


@login_required
def asset_edit(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    plants = Plant.objects.filter(is_active=True)
    
    if request.method == "POST":
        asset.plant_id = request.POST.get("plant")
        asset.name = request.POST.get("name")
        asset.code = request.POST.get("code")
        asset.location = request.POST.get("location", "")
        asset.description = request.POST.get("description", "")
        asset.manufacturer = request.POST.get("manufacturer", "")
        asset.model = request.POST.get("model", "")
        asset.serial_number = request.POST.get("serial_number", "")
        asset.status = request.POST.get("status", "active")
        asset.save()
        
        if request.htmx:
            assets = Asset.objects.filter(is_active=True).select_related('plant')
            response = render(request, "assets/partials/asset_table.html", {"assets": assets, "plants": plants})
            response['HX-Trigger'] = 'closeModal'
            return response
        
        return redirect('assets:asset_list')
    
    context = {
        'asset': asset,
        'plants': plants,
    }
    
    if request.htmx:
        return render(request, "assets/partials/asset_form.html", context)
    
    return render(request, "assets/asset_form.html", context)


@login_required
def asset_delete(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    plants = Plant.objects.filter(is_active=True)
    
    if request.method == "POST":
        asset.is_active = False
        asset.save()
        
        if request.htmx:
            assets = Asset.objects.filter(is_active=True).select_related('plant')
            response = render(request, "assets/partials/asset_table.html", {"assets": assets, "plants": plants})
            response['HX-Trigger'] = 'closeModal'
            return response
        
        return redirect('assets:asset_list')
    
    if request.htmx:
        return render(request, "assets/partials/asset_delete_confirm.html", {"asset": asset})
    
    return render(request, "assets/asset_delete_confirm.html", {"asset": asset})
