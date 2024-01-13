from django.shortcuts import render, redirect
from .models import Salons
from booking.models import Slots
from django.http import JsonResponse


# def home_view(request):
#     if not request.user.is_authenticated:
#         return redirect('login/')
    
#     salons = Salons.objects.all()
#     return render(request, template_name='home/home.html', context={'salons':salons})



def home_view(request):
    print('request', request.body)
    salons = Salons.objects.all()
    username = request.GET.get('username')
    data = {'data': list(salons.values())}
    if username:
        slots = Slots.objects.filter(customer__username=username, active=True)
        if slots:
            data['slots'] = list(slots.values())
            print(data['slots'])
    return JsonResponse(data)
