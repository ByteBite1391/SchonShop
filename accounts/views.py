from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile


@login_required
def profile_view(request):
    # اگه پروفایل نباشه می‌سازیم
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        profile.save()
        
        messages.success(request, 'پروفایل شما به‌روزرسانی شد.')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/profile.html', {'profile': profile})