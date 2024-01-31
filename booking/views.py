from django.shortcuts import render
from home.models import Salons
from .models import SalonAndServices, Slots, UserLocation
from django.http import JsonResponse
from django.core.serializers import serialize
import json
from django.contrib.auth.models import User
from django.utils import timezone

# def slot_book(request, id):
#     is_canceled = False
#     salon = Salons.objects.get(pk=id)

#     if request.method == 'POST' and 'cancel' in request.POST:
#         slots = Slots.objects.filter(customer=request.user,salon=salon,active=True)
#         # print(f'sl:{slots}')
#         is_canceled = True
#         slots.update(active=False)

#     services = SalonAndServices.objects.filter(salon=id)
#     # Find the queue size and expected time
#     slots = Slots.objects.filter(salon=salon,active=True)
#     hrs, mins, queue_size = 0, 0, 0
#     for slot in slots:
#         queue_size += 1
#         time = slot.time
#         print(f'time:{time}')
#         time = time.split(':')
#         hrs += int(time[0]) + int(time[1])//60
#         mins += int(time[1])%60
#     hrs = mins//60
#     mins = mins%60
#     expected_time = str(hrs)+":"+str(mins)

#     context = {
#         'salon':salon,
#         'services':services,
#         'queue_size':queue_size,
#         'expected_time':expected_time,
#         'is_canceled':is_canceled
#         }
    
#     if request.method == 'POST':
#         hrs, mins, price = 0, 0, 0
#         selected_services = []
#         for service in services:
#             if str(service.service.id) in request.POST:
#                 selected_services.append(request.POST[str(service.service.id)])
#                 time = service.time
#                 time = time.split(':')
#                 hrs += int(time[0]) + int(time[1])//60
#                 mins += int(time[1])%60

#                 price += service.price
#         hrs = mins//60
#         mins = mins%60
#         time = str(hrs)+":"+str(mins)

#         slot_obj = Slots.objects.create(customer=request.user,salon=salon,services=str(selected_services),price=price,time=time,active=True)
#         # print(f'slotobj:{slot_obj}')
#         context['selected_services'] = selected_services
#         context['time'] = time
#         context['price'] = price
#         return render(request, template_name='booking/booking.html', context=context)
            
#         #     print(service.service.name, service.time, service.price)
    

#     return render(request, template_name='booking/booking.html', context=context)


def slot_book(request, id):
    is_canceled = False

    try:
        salon = Salons.objects.filter(pk=id).values()
    except Salons.DoesNotExist:
        return JsonResponse({'error': 'Salon not found'}, status=404)

    if request.method == 'POST' and 'cancel' in request.POST:
        slots = Slots.objects.filter(customer=request.user, salon_id=id, active=True)
        is_canceled = True
        slots.update(active=False)

    services = SalonAndServices.objects.filter(salon=id).values('id', 'time', 'price', 'service__name')

    # Find the queue size and expected time
    slots = Slots.objects.filter(salon_id=id, active=True)
    hrs, mins, queue_size = 0, 0, 0
    for slot in slots:
        queue_size += 1
        time = slot.time
        time = time.split(':')
        hrs += int(time[0]) + int(time[1]) // 60
        mins += int(time[1]) % 60
    hrs += mins // 60
    mins %= 60
    expected_time = f'{hrs:02d}:{mins:02d}'

    context = {
        'salon': list(salon)[0],
        'services': list(services),
        'queue_size': queue_size,
        'expected_time': expected_time,
        'is_canceled': is_canceled
    }

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user = User.objects.get(username=data['userName'])
        slot_obj = Slots.objects.create(
            customer=user,
            salon=Salons.objects.get(pk=id),
            services=data['selectedRows'],
            price=data['totalAmount'],
            time=data['totalExpectedTime'],
            active=True
        )

        print('slot_obj:', slot_obj)

        context['selected_services'] = data['selectedRows']
        context['time'] = data['totalExpectedTime']
        context['price'] = data['totalAmount']

        return JsonResponse(context)
    print(context)

    return JsonResponse(context, safe=False)

def slot_cancel(request, id):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        salon_id = data['salonId']
        user = User.objects.get(username=data['userName'])
        slots = Slots.objects.filter(customer=user, salon_id=salon_id, active=True)
        slots.update(active=False, canceled_by='customer', canceled_on=timezone.now())
        return JsonResponse({'status': 'success'})
    

def update_location(request):
    if request.method == 'POST':
        user = request.user  # Assuming you have user authentication
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Save location data to the database (optional)
        UserLocation.objects.create(user=user, latitude=latitude, longitude=longitude)

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})