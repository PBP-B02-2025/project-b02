from django.shortcuts import render, redirect, get_object_or_404
from userMeasurement.forms import UserMeasurementForm
from userMeasurement.models import userMeasurement
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
@login_required(login_url='/login')
def show_measurement(request):
    user = request.user
    data = userMeasurement.objects.filter(user=user).first()

    if data is None:
        return render(request, 'recommended_size.html', {'data': None})

    return render(request, 'recommended_size.html', {'data': data})

@login_required(login_url='/login')
def update_measurement(request):
    user = request.user  # ganti User.objects.first() ke request.user
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



