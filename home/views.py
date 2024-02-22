from django.shortcuts import render, redirect
from .models import Salons
from booking.models import Slots
from django.http import JsonResponse
from .utils import calculate_distance
from django.forms.models import model_to_dict


# def home_view(request):
#     if not request.user.is_authenticated:
#         return redirect('login/')
    
#     salons = Salons.objects.all()
#     return render(request, template_name='home/home.html', context={'salons':salons})

def find_nearest_shops(request):
    user_latitude = float(request.GET.get('location[latitude]'))
    user_longitude = float(request.GET.get('location[longitude]'))

    # Find nearest shops
    shops = Salons.objects.all()
    nearest_shops = []

    for shop in shops:
        distance = calculate_distance(user_latitude, user_longitude, shop.latitude, shop.longitude)
        shop.distance_to_user = distance
        nearest_shops.append(shop)

    # Sort the shops by distance
    nearest_shops = sorted(nearest_shops, key=lambda x: x.distance_to_user)
    return nearest_shops


def home_view(request):
    location = request.GET.get('location[latitude]', None)
    if location is not None:
        salons = find_nearest_shops(request)
        salons_data = [
            {
                **model_to_dict(salon),
                'image': str(salon.image),
                'city_id': salon.city.id,
                'distance_to_user': salon.distance_to_user
            }
            for salon in salons
        ]
        data = {'data': salons_data}
    else:
        salons = Salons.objects.all()
        data = {'data': list(salons.values())}
    username = request.GET.get('username')
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
