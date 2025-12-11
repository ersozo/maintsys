from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from plants.models import Plant
from assets.models import Asset


@login_required
def dashboard(request):
    # Dashboard stats
    context = {
        'total_plants': Plant.objects.filter(is_active=True).count(),
        'total_assets': Asset.objects.filter(is_active=True).count(),
        'active_assets': Asset.objects.filter(is_active=True, status='active').count(),
        'maintenance_assets': Asset.objects.filter(is_active=True, status='maintenance').count(),
        'recent_plants': Plant.objects.filter(is_active=True).order_by('-created_at')[:5],
        'recent_assets': Asset.objects.filter(is_active=True).order_by('-created_at')[:5],
    }
    return render(request, 'core/dashboard.html', context)


def login_view(request):
    error = None
    
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'core:dashboard')
            return redirect(next_url)
        else:
            error = 'Kullanıcı adı veya şifre hatalı.'
    
    return render(request, 'core/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('core:login')
