from django.urls import path, include
from . import views

app_name = 'booking'

urlpatterns = [
    path('book/<int:id>', views.slot_book, name='slot_book_view'),
    path('cancel/<int:id>', views.slot_cancel, name='slot_cancel_view'),
]
