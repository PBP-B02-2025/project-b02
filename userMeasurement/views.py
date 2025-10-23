from django.shortcuts import render, redirect, get_object_or_404
from userMeasurement.forms import UserMeasurementForm
from userMeasurement.models import userMeasurement
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.

def show_measurement(request):
    user = request.user
    data = userMeasurement.objects.filter(user=user).first()

    # Kalau user belum punya data size
    if data is None:
        return render(request, 'main.html', {
            'data': None
        })

    # Kalau sudah punya data
    return render(request, 'main.html', {
        'data': data
    })

def update_measurement(request):
    user = User.objects.first()
    data = userMeasurement.objects.filter(user=user).first()

    if request.method == 'POST':
        form = UserMeasurementForm(request.POST, instance=data)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.calculate_bmi()
            obj.save()
            return redirect('userMeasurement:show_measurement')
    else:
        form = UserMeasurementForm(instance=data)

    return render(request, 'form.html', {'form': form})



