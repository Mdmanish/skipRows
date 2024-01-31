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
            created_on = slots.first().created_on
            salon_id = slots.first().salon_id
            queue_size = Slots.objects.filter(created_on__lt=created_on,salon_id=salon_id,active=True)
            hrs, mins = 0, 0
            for slot in queue_size:
                time = slot.time
                time = time.split(':')
                hrs += int(time[0]) + int(time[1]) // 60
                mins += int(time[1]) % 60
            hrs += mins // 60
            mins %= 60
            data['queue_size'] = len(list(queue_size))
            data['waiting_time'] = f'{hrs:02d}:{mins:02d}'
            data['salon_id'] = salon_id
            print(data)
    return JsonResponse(data)
